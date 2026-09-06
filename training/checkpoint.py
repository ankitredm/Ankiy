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
from dataclasses import asdict
from pathlib import Path

import torch
from safetensors.torch import load_file, save_file

from model.config import Config


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
) -> Path:
    """Save a training checkpoint. Returns the checkpoint directory path."""
    ckpt_dir = Path(ckpt_dir)
    name = f"step_{step}" if tag is None else f"{tag}_step_{step}"
    out_dir = ckpt_dir / name
    out_dir.mkdir(parents=True, exist_ok=True)

    # 1. Model weights -> safetensors
    weights_path = out_dir / "model.safetensors"
    save_file({k: v.to("cpu") for k, v in model.state_dict().items()}, str(weights_path))

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
        "seed": int(seed),
        "checkpoint_format_version": 1,
    }
    meta_path = out_dir / "meta.json"
    meta_path.write_text(json.dumps(meta, indent=2), encoding="utf-8")

    return out_dir


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
    meta = json.loads(meta_path.read_text(encoding="utf-8"))

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
