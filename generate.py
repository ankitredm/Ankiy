#!/usr/bin/env python3
"""Generate text using an ANKIT 0.1 checkpoint.

It loads ONLY:
    - our own trained ANKIT model weights (a .safetensors checkpoint)
    - our own trained tokenizer (from Phase 4)
    - the model config (from the checkpoint's meta.json)

It NEVER loads a pretrained model. The checkpoint is our from-scratch ANKIT.

Usage:
    python generate.py --prompt "The capital of" --ckpt checkpoints/step_10
    python generate.py --prompt "Hello" --ckpt checkpoints/step_20 --top_k 40 --temperature 0.8

If --ckpt is omitted, it uses the latest checkpoint under the default output dir.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import torch

from tokenizer.tokenizer import AnkitTokenizer
from training.checkpoint import latest_checkpoint, load_checkpoint_model

DEFAULT_TOK_PATH = "tokenizer/ankit_tokenizer.json"


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate text with ANKIT 0.1.")
    parser.add_argument("--prompt", default="", help="Text to start generation from.")
    parser.add_argument(
        "--ckpt",
        default=None,
        help="Path to a checkpoint dir containing model.safetensors (default: latest).",
    )
    parser.add_argument("--tokenizer", default=DEFAULT_TOK_PATH, help="Path to our tokenizer JSON.")
    parser.add_argument("--max-new-tokens", type=int, default=40)
    parser.add_argument("--temperature", type=float, default=1.0)
    parser.add_argument("--top-k", type=int, default=None)
    parser.add_argument("--top-p", type=float, default=None)
    parser.add_argument("--repetition-penalty", type=float, default=1.0)
    parser.add_argument("--seed", type=int, default=None)
    args = parser.parse_args()

    # Resolve checkpoint path.
    ckpt_path = Path(args.ckpt) if args.ckpt else latest_checkpoint("checkpoints")
    if ckpt_path is None:
        raise SystemExit("No checkpoint found. Run training first.")
    if not (ckpt_path / "model.safetensors").exists():
        raise SystemExit(f"No model.safetensors in {ckpt_path}")

    print(f"Loading ANKIT model from {ckpt_path}")
    model, config = load_checkpoint_model(ckpt_path, device="cpu")
    model.eval()

    tokenizer = AnkitTokenizer.load(args.tokenizer)
    print(f"Tokenizer vocab: {tokenizer.vocab_size} | model params: {model.num_parameters():,}")

    # Encode the prompt.
    device = "cpu"
    ids = tokenizer.encode(args.prompt, add_bos=True, add_eos=False)
    if not ids:
        print("[warn] empty prompt; generating from BOS only.")
        ids = [tokenizer.bos_id] if tokenizer.bos_id is not None else [0]
    input_ids = torch.tensor([ids], dtype=torch.long, device=device)

    # Generate.
    out = model.generate(
        input_ids,
        max_new_tokens=args.max_new_tokens,
        temperature=args.temperature,
        top_k=args.top_k,
        top_p=args.top_p,
        repetition_penalty=args.repetition_penalty,
        seed=args.seed,
    )
    generated_ids = out[0].tolist()
    text = tokenizer.decode(generated_ids)
    print("\n--- Generated text ---")
    print(text.strip())
    print("----------------------")


if __name__ == "__main__":
    main()
