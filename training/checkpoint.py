"""Save and load ANKIT 0.1 training checkpoints.

A checkpoint holds everything needed to resume training exactly:
    - model weights
    - optimizer state
    - scheduler state (current lr + step count)
    - current training step
    - the config (so we can rebuild the model)
    - tokenizer version
    - random seed / RNG state

We use ``safetensors`` for the model *weights* (safe, fast, no pickle issues)
and a JSON sidecar for the optimizer/scheduler/step metadata.

The model weights are always our OWN randomly-initialised-then-trained ANKIT
model. Loading a checkpoint never introduces a pretrained model.
"""

from __future__ import annotations

import json
from pathlib import Path

import torch
from safetensors.torch import load_file, save_file

from model.config import Config
from training.provenance import ANKIT_CHECKPOINT_FORMAT_VERSION, verify_ankit_checkpoint

# Architecture-defining fields. If ANY of these differ between the current
# config and a checkpoint's meta.json, the saved weights cannot be loaded
# correctly and resume must be refused (shapes or semantics would change).
_ARCH_COMPAT_KEYS = (
    "vocab_size",
    "d_model",
    "n_layers",
    "n_heads",
    "context_length",
    "ffn_dim",
    "activation",
    "tie_embedding",
    "use_bias",
)


def save_checkpoint(
    ckpt_dir: str | Path,
    model: torch.nn.Module,
    optimizer: torch.optim.Optimizer,
    scheduler: torch.optim.lr_scheduler.LRScheduler | None,
    step: int,
    config: Config,
    tokenizer_version: str,
    seed: int,
    *,
    tag: str | None = None,
    tokenizer_vocab_size: int | None = None,
) -> Path:
    """Save a training checkpoint. Returns the checkpoint directory path."""
    ckpt_dir = Path(ckpt_dir)
    name = f"step_{step}" if tag is None else f"{tag}_step_{step}"
    out_dir = ckpt_dir / name
    out_dir.mkdir(parents=True, exist_ok=True)

    # 1. Model weights -> safetensors
    # .clone() breaks storage sharing (e.g. a tied lm_head/token-embedding
    # weight), which safetensors refuses to serialize.
    weights_path = out_dir / "model.safetensors"
    save_file(
        {k: v.detach().to("cpu").clone() for k, v in model.state_dict().items()},
        str(weights_path),
    )

    # 2. Optimizer + scheduler state -> .pt (pickle is fine here; it's our own).
    opt_path = out_dir / "optimizer.pt"
    torch.save(optimizer.state_dict(), str(opt_path))
    sched_state = scheduler.state_dict() if scheduler is not None else None
    sched_path = out_dir / "scheduler.pt"
    if sched_state is not None:
        torch.save(sched_state, str(sched_path))

    # 3. Metadata -> JSON
    meta = {
        "step": int(step),
        "model_config": config.model.__dict__,
        "training_config": config.training.__dict__,
        "name": config.name,
        "tokenizer_version": tokenizer_version,
        "tokenizer_vocab_size": (
            int(tokenizer_vocab_size)
            if tokenizer_vocab_size is not None
            else int(config.model.vocab_size)
        ),
        "seed": int(seed),
        "checkpoint_format_version": ANKIT_CHECKPOINT_FORMAT_VERSION,
    }
    meta_path = out_dir / "meta.json"
    meta_path.write_text(json.dumps(meta, indent=2), encoding="utf-8")

    return out_dir


def validate_resume_checkpoint(
    ckpt_dir: str | Path,
    config: Config,
    tokenizer_vocab_size: int,
) -> dict:
    """Validate that ``ckpt_dir`` can safely resume into the CURRENT run.

    Called BEFORE any weights are loaded. Confirms:

      1. it is a native ANKIT checkpoint (our own format — never foreign);
      2. every architecture-defining model field (vocab size, layers, heads,
         context length, ...) matches the current config exactly, so the
         saved weights actually fit the model we are about to build;
      3. the tokenizer vocabulary size recorded in the checkpoint matches
         the tokenizer we are training with now;
      4. the step counter and the required state files are sane.

    Returns the checkpoint's meta dict. Raises ValueError/ RuntimeError with
    an actionable message on any incompatibility.
    """
    ckpt_dir = Path(ckpt_dir)
    meta = verify_ankit_checkpoint(ckpt_dir)

    meta_model = meta["model_config"]
    current_model = config.model.__dict__
    mismatches = {
        key: (meta_model.get(key), current_model.get(key))
        for key in _ARCH_COMPAT_KEYS
        if meta_model.get(key) != current_model.get(key)
    }
    if mismatches:
        details = "\n".join(
            f"  {key}: checkpoint={old!r} != config={new!r}"
            for key, (old, new) in mismatches.items()
        )
        raise ValueError(
            "Cannot resume: checkpoint architecture does not match the "
            f"current config ({ckpt_dir}).\n{details}\n"
            "Restore the original model section in the config, or point "
            "training.output_dir at a fresh directory to start from random "
            "weights."
        )

    ckpt_vocab = int(
        meta.get("tokenizer_vocab_size", meta_model.get("vocab_size", -1))
    )
    if ckpt_vocab != int(tokenizer_vocab_size):
        raise ValueError(
            "Cannot resume: tokenizer vocabulary changed since this "
            f"checkpoint was written ({ckpt_dir}). Checkpoint vocab "
            f"{ckpt_vocab:,} != current tokenizer vocab "
            f"{int(tokenizer_vocab_size):,}. Restore the original tokenizer, "
            "or start a fresh run in a new output_dir."
        )

    step = int(meta["step"])
    if step < 0:
        raise ValueError(
            f"Corrupt ANKIT checkpoint: negative step {step} in {ckpt_dir}."
        )
    if not (ckpt_dir / "optimizer.pt").is_file():
        raise RuntimeError(
            f"Broken ANKIT checkpoint: {ckpt_dir} has no optimizer.pt — "
            "optimizer state is required to resume training."
        )
    return meta


def latest_checkpoint(ckpt_dir: str | Path) -> Path | None:
    """Return the path to the most recent ``step_*`` checkpoint, or None."""
    ckpt_dir = Path(ckpt_dir)
    if not ckpt_dir.exists():
        return None
    candidates = [
        p
        for p in ckpt_dir.iterdir()
        if p.is_dir() and p.name.startswith("step_")
    ]
    if not candidates:
        return None
    # Sort by the numeric step embedded in the name.
    def step_key(p: Path):
        try:
            return int(p.name.split("_")[-1])
        except ValueError:
            return -1

    return max(candidates, key=step_key)


def load_checkpoint_model(ckpt_dir: str | Path, device: str = "cpu") -> tuple[object, Config]:
    """Rebuild a model from a checkpoint's config, then load its weights.

    Returns (model, config). The config is read from meta.json so the exact
    architecture is reconstructed.
    """
    ckpt_dir = Path(ckpt_dir)
    # Accept either a single checkpoint dir (containing meta.json) or a root
    # dir with one or more step_* subdirs (in which case use the latest).
    meta_path = ckpt_dir / "meta.json"
    if not meta_path.exists():
        latest = latest_checkpoint(ckpt_dir)
        if latest is None:
            raise FileNotFoundError(
                f"No meta.json in {ckpt_dir} and no step_* checkpoint found."
            )
        ckpt_dir = latest
        meta_path = latest / "meta.json"
    # Prove this is one of OUR native checkpoints before touching the weights.
    meta = verify_ankit_checkpoint(ckpt_dir)

    from model import AnkitModel, Config as ConfigType  # local import

    config = Config.from_dict(
        {
            "name": meta.get("name", "ankit-0-1"),
            "model": meta["model_config"],
            "training": meta["training_config"],
        }
    )
    model = AnkitModel(config.model).to(device)
    weights_path = ckpt_dir / "model.safetensors"
    if not weights_path.exists():
        # Fallback: some checkpoints may store a plain .pt if safetensors absent.
        raise FileNotFoundError(f"No model.safetensors in {ckpt_dir}")
    state = load_file(str(weights_path), device=device)
    model.load_state_dict(state)
    return model, config
