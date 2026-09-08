"""Provenance guards for ANKIT 0.1 — proof that we train from scratch.

The project has one absolute rule: **never load a pretrained model**. Until now
the training loop "enforced" this with a function that only printed a message.
This module makes the rule *checkable*:

    :func:`verify_fresh_initialization`
        Proves that a model in memory is EXACTLY the fresh random
        initialisation for its (config, seed) — i.e. no weights were loaded
        from anywhere before training started. It rebuilds a reference model
        from the same seed and compares every parameter bit-for-bit.

    :func:`verify_ankit_checkpoint`
        Proves that a checkpoint directory is a NATIVE ANKIT checkpoint (our
        own meta.json + safetensors format, written by
        ``training/checkpoint.save_checkpoint``). Used before any resume so we
        only ever continue from our own weights — never from an external or
        foreign checkpoint file.

    :func:`state_dict_fingerprint`
        A stable SHA-256 fingerprint of a state dict (names + shapes + raw
        tensor bytes), used by the checks above and useful in tests.

No pretrained weights or tokenizers are referenced anywhere in this module —
it exists precisely to guarantee that.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Mapping

import torch

from model import AnkitModel
from model.config import ModelConfig

# Bumped only when the on-disk checkpoint layout changes incompatibly.
ANKIT_CHECKPOINT_FORMAT_VERSION = 1

# Keys every native ANKIT checkpoint's meta.json must contain.
_REQUIRED_META_KEYS = ("step", "model_config", "training_config", "tokenizer_version")


# ---------------------------------------------------------------------------
# Fingerprints
# ---------------------------------------------------------------------------
def state_dict_fingerprint(state_dict: Mapping[str, torch.Tensor]) -> str:
    """SHA-256 over parameter names, shapes, dtypes and raw tensor bytes.

    Deterministic for a given set of weights regardless of device or key
    insertion order (keys are hashed in sorted order).
    """
    digest = hashlib.sha256()
    for name in sorted(state_dict):
        tensor = state_dict[name].detach().cpu().contiguous()
        digest.update(name.encode("utf-8"))
        digest.update(str(tuple(tensor.shape)).encode("utf-8"))
        digest.update(str(tensor.dtype).encode("utf-8"))
        # Reinterpret as raw bytes so even exotic dtypes hash deterministically.
        digest.update(tensor.flatten().view(torch.uint8).numpy().tobytes())
    return digest.hexdigest()


def fresh_model_fingerprint(config: ModelConfig, seed: int) -> str:
    """Fingerprint of a freshly initialised AnkitModel for (config, seed).

    Builds a throwaway reference model. The global RNG state is saved and
    restored, so calling this never perturbs the caller's reproducibility.
    """
    rng_state = torch.get_rng_state()
    try:
        torch.manual_seed(seed)
        reference = AnkitModel(config)  # always built on CPU, like train.py
        return state_dict_fingerprint(reference.state_dict())
    finally:
        torch.set_rng_state(rng_state)


# ---------------------------------------------------------------------------
# Check 1 — training really starts from fresh random weights
# ---------------------------------------------------------------------------
def verify_fresh_initialization(
    model: torch.nn.Module, config: ModelConfig, seed: int
) -> None:
    """Raise RuntimeError unless ``model`` is EXACTLY a fresh random init.

    A reference model is rebuilt from (config, seed) and every state-dict
    entry is compared bit-for-bit against ``model``. Any difference means
    weights were modified or loaded between construction and this check —
    which the from-scratch rule forbids before training starts.
    """
    rng_state = torch.get_rng_state()
    try:
        torch.manual_seed(seed)
        reference = AnkitModel(config)
    finally:
        torch.set_rng_state(rng_state)

    ref_state = reference.state_dict()
    cur_state = model.state_dict()

    if set(cur_state) != set(ref_state):
        only_current = sorted(set(cur_state) - set(ref_state))
        only_reference = sorted(set(ref_state) - set(cur_state))
        raise RuntimeError(
            "Fresh-initialization check FAILED: state dict keys differ from a "
            f"fresh AnkitModel (unexpected keys: {only_current[:5]}, "
            f"missing keys: {only_reference[:5]}). Refusing to train."
        )

    mismatched = [
        name
        for name in sorted(ref_state)
        if cur_state[name].detach().cpu().shape != ref_state[name].shape
        or not torch.equal(cur_state[name].detach().cpu(), ref_state[name])
    ]
    if mismatched:
        raise RuntimeError(
            "Fresh-initialization check FAILED: parameters differ from a "
            f"freshly initialised model (first mismatches: {mismatched[:5]}). "
            "Weights must come from a fresh random init (or an explicit ANKIT "
            "checkpoint resume) — refusing to train."
        )


# ---------------------------------------------------------------------------
# Check 2 — a checkpoint really is one of OUR native ANKIT checkpoints
# ---------------------------------------------------------------------------
def verify_ankit_checkpoint(ckpt_dir: str | Path) -> dict[str, Any]:
    """Verify ``ckpt_dir`` is a native ANKIT checkpoint. Returns its meta dict.

    Raises RuntimeError if the directory is missing required files or its
    metadata is absent/foreign/unknown. This is what keeps resume and
    inference pointed at OUR from-scratch checkpoints only.
    """
    ckpt_dir = Path(ckpt_dir)
    meta_path = ckpt_dir / "meta.json"
    if not meta_path.is_file():
        raise RuntimeError(
            f"Not an ANKIT checkpoint: {ckpt_dir} has no meta.json. Only "
            "checkpoints written by training/checkpoint.save_checkpoint "
            "(our own format) can be used — external/foreign model files are "
            "never loaded."
        )
    try:
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise RuntimeError(
            f"Corrupt ANKIT checkpoint metadata: {meta_path} ({exc})."
        ) from exc
    if not isinstance(meta, dict):
        raise RuntimeError(f"Corrupt ANKIT checkpoint metadata: {meta_path}.")

    version = meta.get("checkpoint_format_version")
    if not isinstance(version, int) or version != ANKIT_CHECKPOINT_FORMAT_VERSION:
        raise RuntimeError(
            f"Unknown checkpoint format in {ckpt_dir}: "
            f"checkpoint_format_version={version!r}, expected "
            f"{ANKIT_CHECKPOINT_FORMAT_VERSION}. This is not a recognisable "
            "ANKIT checkpoint."
        )

    missing = [key for key in _REQUIRED_META_KEYS if key not in meta]
    if missing:
        raise RuntimeError(
            f"Incomplete ANKIT checkpoint metadata in {ckpt_dir}: "
            f"missing keys {missing}."
        )
    if not isinstance(meta["model_config"], dict):
        raise RuntimeError(
            f"Corrupt ANKIT checkpoint metadata in {ckpt_dir}: 'model_config' "
            "must be a mapping."
        )

    if not (ckpt_dir / "model.safetensors").is_file():
        raise RuntimeError(
            f"Broken ANKIT checkpoint: {ckpt_dir} has no model.safetensors."
        )
    return meta
