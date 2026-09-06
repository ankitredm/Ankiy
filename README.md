# ANKIT 0.1 ✦

**A language model we build ourselves — trained completely from scratch.**

ANKIT 0.1 is not a wrapper around an existing model. It is not Qwen, Llama,
Gemma, Mistral, Phi, GPT, Falcon, or BLOOM. There are **no pretrained weights**
and **no pretrained tokenizer**. Everything — the architecture, the weights,
the tokenizer, the vocabulary, the dataset pipeline, the training loop, the
checkpoint format, and the inference system — is our own, built from randomly
initialized weights using only standard libraries (PyTorch, NumPy, Hugging Face
Tokenizers, safetensors).

Think of it like building a car from parts instead of rebranding someone else's
car. We start with raw metal (random weights) and build up, step by step.

> **This is a learning project.** A tiny model trained on a small dataset will
> not magically equal ChatGPT. We will be honest about what it can and cannot
> do at every stage.

---

## Why "from scratch" matters

The absolute rule of this project:

> **Never** switch to a pretrained model because training is "too expensive."

If a step is too big, we shrink it (smaller model, smaller dataset, shorter
context, fewer steps, cheaper GPU). We never quietly swap in Llama or Qwen.

---

## The plan

We follow phases in order. We do not skip ahead.

| Phase | What we build |
| --- | --- |
| **1** | Verify the cloud GPU environment (this phase) |
| 2 | Project structure |
| 3 | Dataset strategy |
| 4 | Train our own tokenizer |
| 5 | Transformer architecture |
| 6 | Tiny smoke-test model |
| 7 | Train tiny model from random init |
| 8 | Save & reload checkpoint |
| 9 | Generate text |
| 10 | Scale up ANKIT 0.1 |
| 11 | Instruction training on our own model |
| 12 | Personality config |
| 13 | Memory system |
| 14 | RAG |
| 15 | API |
| 16 | Frontend / mobile |

**We are currently at Phase 1.**

---

## Phase 1 — cloud GPU environment

### 1. Cloud GPU options (easy → cheapest)

Prices move often; treat the numbers below as a rough guide, not a quote.
Always check the provider's live page.

| Option | What you get | Rough cost | Best for |
| --- | --- | --- | --- |
| **Google Colab (free)** | 1× T4 (16 GB), ~12h sessions, resets often | Free | Trying things, learning |
| **Colab Pro** | Better GPUs, fewer interruptions | ~$10/mo | Light training |
| **Kaggle (free)** | T4 / P100, 30 h/week | Free | Batch-able jobs |
| **RunPod** | RTX 3090/4090, per-second billing | ~$0.17–0.70/hr | Reliable, easy |
| **Vast.ai** | any GPU, marketplace, per-second | ~$0.07–0.45/hr | Cheapest |

### 2. Recommendation for a beginner

**Start on a free Google Colab GPU (T4).** Why:

- Zero cost to begin — perfect for the smoke test.
- `nvidia-smi`, Python, and PyTorch are already set up; you just pick "GPU".
- You can verify the whole pipeline, then decide whether to pay for more.

**When you are ready to actually train for a while**, move to a paid per-second
provider (RunPod is the easiest; Vast.ai is the cheapest). The T4's 16 GB is
plenty for our first target (~10M–100M parameters), and you can come back to
Colab for the next phase.

### 3. Minimum environment setup

Navigate to the project folder in your terminal, then create an isolated Python
environment and install the dependencies. The commands are the same on Linux,
Mac, and Colab (Colab just runs them in a notebook cell).

```bash
python3 -m venv .venv
source .venv/bin/activate        # Windows PowerShell: .venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r requirements.txt
```

Install PyTorch to match your machine:

- **CPU only:** `pip install torch --index-url https://download.pytorch.org/whl/cpu`
- **NVIDIA GPU (recommended):** `pip install torch --index-url https://download.pytorch.org/whl/cu121`

### 4. Verify the GPU and PyTorch/CUDA

Run the environment checker:

```bash
python scripts/verify_environment.py
```

- On a cloud GPU machine, this should print **PASS** for GPU and CUDA.
- On a CPU-only box, it prints **WARN** for GPU and tells you to pick a GPU
  runtime. That is expected — it is not a bug.

On Colab specifically, before running the above, make sure a GPU is selected:
**Runtime → Change runtime type → Hardware accelerator → "GPU"**.

**Our environment checker never downloads or loads a pretrained model or
tokenizer.** It only reports what your machine has.

---

## Project layout

```text
configs/                  # YAML config (model size, training hyperparams)
  ankit_0_1.yaml          # the target ~13M model
  smoke.yaml              # tiny model for quick pipeline checks
dataprep/                 # dataset pipeline: clean, filter, dedup, split, stats
data/
  raw/                    # raw public-domain text (sample/ is committed; big dl's are not)
  processed/              # cleaned/normalized splits (.jsonl)
  tokenized/              # token IDs ready for training
model/                    # our own Transformer implementation
  config.py               # config dataclasses + YAML loader
  embeddings.py           # token + positional embedding
  attention.py            # causal multi-head self-attention
  transformer.py          # one decoder block + feed-forward
  ankit_model.py          # the full decoder-only AnkitModel
tokenizer/                # train_tokenizer.py + tokenizer.py (our own BPE)
training/                 # train.py, dataset.py, checkpoint.py (from-scratch loop)
generate.py               # generate text from an ANKIT checkpoint
evaluation/               # evaluate.py + benchmarks
scripts/                  # count_parameters.py, prepare_dataset.py, verify_environment.py
tests/                    # pytest suite (config + model)
checkpoints/              # model checkpoints (git-ignored)
logs/                     # training logs (git-ignored)
```

### What's built so far

**Phase 5 — training pipeline** (`training/`, `scripts/tokenize_dataset.py`,
`generate.py`). The complete from-scratch training loop:

```bash
python scripts/tokenize_dataset.py          # cleaned text -> token-id .bin files
python training/train.py --config configs/smoke.yaml   # tiny smoke run (CPU)
python generate.py --prompt "The capital of" --ckpt checkpoints/step_20
```

`training/train.py` builds a model from random weights, runs causal next-token
prediction with AdamW + warmup/cosine LR schedule, mixed precision, gradient
clipping/accumulation, validation, checkpointing (safetensors), and resume. It
**never** loads a pretrained model.

**Phase 4 — our own tokenizer** (`tokenizer/`, `configs/tokenizer.yaml`). A
freshly trained **byte-level BPE** tokenizer on our own corpus — not a copy of
Qwen/Llama/GPT:

```bash
python tokenizer/train_tokenizer.py   # train tokenizer + write vocab + report
```

It supports `text -> token ids` and `token ids -> text`, with proper BOS/EOS/PAD/UNK
special tokens. Use it from code:

```python
from tokenizer.tokenizer import AnkitTokenizer
tok = AnkitTokenizer.load()
ids = tok.encode("The capital of France is Paris", add_bos=True, add_eos=True)
text = tok.decode(ids)
```

**Phase 3 — dataset pipeline** (`dataprep/`, `configs/data.yaml`). A fully
reproducible, CPU-only pipeline that turns legal raw text into training-ready
documents:

```bash
python scripts/download_gutenberg.py   # (requires internet) pull public-domain text
python scripts/prepare_dataset.py       # clean -> filter -> dedup -> split -> stats
python scripts/data_stats.py            # show the saved statistics again
```

It cleans + normalises text, drops low-quality documents, removes exact and
(near-)duplicate documents, and splits into train/val/test `.jsonl` — all
driven by `configs/data.yaml`, all deterministic for a given seed. Stats are
saved to `data/stats/stats.json`.

**Phase 2 — the model architecture.** A **decoder-only Transformer** (the same
family as modern LLMs), but implemented by us from randomly initialised
weights:

- token embeddings + learned positional embeddings
- causal multi-head self-attention (with a triangular mask so a token can only
  see itself and earlier tokens)
- pre-norm feed-forward blocks with residual connections
- final layer-norm + language-model output head
- `forward()` for next-token prediction, `generate()` for sampling

Everything is driven by YAML config. Change a number in `configs/ankit_0_1.yaml`
and the model changes shape — **no source code edits needed**.

Count the parameters of a real build (no hard-coded guess):

```bash
python scripts/count_parameters.py                  # prints the ~13.18M count
python scripts/count_parameters.py --config configs/smoke.yaml
```

Run the test suite (forward pass, causal mask, loss, checkpoint, generation):

```bash
python -m pytest tests/ -v
```

---

## Anti-shortcut reminders

- If something is too expensive, **shrink** — never swap in a pretrained model.
- Never claim "ChatGPT-level" without strong evidence.
- Never claim "trained from scratch" if any pretrained weights were used.
- We keep a clear record of: model origin, dataset origin, tokenizer origin,
  training method, and checkpoints.

---

## Dataset: what we use and why it's legal

We train on **public-domain and openly licensed text only**. No copyrighted
books, no scraped private data, no synthetic/model-generated text.

| Source | Licence | Used for |
| --- | --- | --- |
| **Project Gutenberg** | Public domain | Real text (books) — the bulk corpus |
| **Committed sample** (`data/raw/sample/`) | Public domain / CC0 | Offline validation of the pipeline |

Run the Gutenberg downloader **on a machine with internet** (your cloud GPU or
laptop) to fetch public-domain books into `data/raw/gutenberg/`, then prepare
the dataset. The sample in the repo is committed so the pipeline is fully
testable here without internet.

The pipeline never introduces model-derived text and never downloads a
pretrained anything.

## How to get help

If something errors, copy the **entire** error message and paste it to us.
We will diagnose it together, one step at a time.
