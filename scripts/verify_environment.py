#!/usr/bin/env python3
"""ANKIT 0.1 — Environment verifier.

Run this on your cloud GPU BEFORE training anything. It answers three questions:

    1.  Is our Python in a good state?
    2.  Do we have a working NVIDIA GPU + CUDA?
    3.  Are the required Python packages installed?

It NEVER downloads a pretrained model. It NEVER trains anything. It only
reports what it finds and prints the exact command to fix a missing piece.
"""

from __future__ import annotations

import importlib
import platform
import shutil
import subprocess
import sys

# ---------------------------------------------------------------------------
# Colours (so a beginner can read PASS / FAIL at a glance)
# ---------------------------------------------------------------------------
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BOLD = "\033[1m"
DIM = "\033[2m"
RESET = "\033[0m"


def ok(text: str) -> str:
    return f"{GREEN}PASS{RESET}  {text}"


def bad(text: str) -> str:
    return f"{RED}FAIL{RESET}  {text}"


def warn(text: str) -> str:
    return f"{YELLOW}WARN{RESET}  {text}"


def heading(text: str) -> None:
    print(f"\n{BOLD}── {text} {RESET}")


def _run(command: list[str]) -> tuple[int, str]:
    """Run a shell command, return (exit_code, stdout)."""
    try:
        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            timeout=30,
        )
        return result.returncode, result.stdout.strip()
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return 1, ""


def check_module(module_name: str) -> str | None:
    """Return the installed version if importable, else None."""
    try:
        mod = importlib.import_module(module_name)
        return getattr(mod, "__version__", "installed")
    except Exception:  # noqa: BLE001 - any import failure means "missing"
        return None


def gpu_from_nvidia_smi() -> str | None:
    """Read GPU name / VRAM / driver via nvidia-smi, avoiding torch dependency."""
    code, out = _run([
        "nvidia-smi",
        "--query-gpu=name,memory.total,driver_version",
        "--format=csv,noheader",
    ])
    if code != 0 or not out:
        return None
    lines = [ln.strip() for ln in out.splitlines() if ln.strip()]
    return "\n".join(f"        {ln}" for ln in lines)


def recommend_install() -> list[str]:
    """Build the friendliest install command based on what's missing."""
    steps: list[str] = []
    torch_missing = check_module("torch") is None
    if torch_missing:
        steps.append(
            "pip install torch --index-url https://download.pytorch.org/whl/cu121"
        )
    return steps


def main() -> int:
    failures = 0
    print(f"{BOLD}ANKIT 0.1 — Environment Check{RESET}\n")

    # 1. System / Python --------------------------------------------------
    heading("1. System")
    print(f"    Python     : {platform.python_version()}")
    print(f"    Platform   : {platform.platform()}")
    print(f"    Machine    : {platform.machine()}")
    py_ok = sys.version_info >= (3, 10)
    print(ok("Python 3.10 or newer") if py_ok else bad("Python must be 3.10+"))
    if not py_ok:
        failures += 1

    pip = check_module("pip")
    print(f"    pip        : {pip or 'not found'}")

    # 2. GPU ---------------------------------------------------------------
    heading("2. GPU (NVIDIA)")
    gpu_info = gpu_from_nvidia_smi()
    if gpu_info:
        print(f"    GPU device (nvidia-smi):\n{gpu_info}")
        print(ok("NVIDIA GPU detected"))
    else:
        print(warn("No NVIDIA GPU detected via `nvidia-smi`."))
        print("        If you are running training on a cloud GPU, make sure you")
        print("        selected a GPU runtime (e.g. Colab: Runtime > Change runtime")
        print("        type > T4 GPU). This step is NOT an error on a CPU-only box.")

    # 3. PyTorch / CUDA ----------------------------------------------------
    heading("3. PyTorch + CUDA")
    torch_ver = check_module("torch")
    if torch_ver is None:
        print(bad("PyTorch is NOT installed."))
        print("        Run:  pip install torch --index-url https://download.pytorch.org/whl/cu121")
        failures += 1
    else:
        print(f"    torch      : {torch_ver}")
        try:
            import torch  # noqa: PLC0415 - intentional late import

            cuda_available = torch.cuda.is_available()
            print(f"    cuda avail : {cuda_available}")
            print(f"    cuda ver   : {torch.version.cuda}")
            print(f"    device(s)  : {torch.cuda.device_count()}")
            if torch.cuda.is_available():
                for i in range(torch.cuda.device_count()):
                    name = torch.cuda.get_device_name(i)
                    cap = torch.cuda.get_device_capability(i)
                    print(f"        [{i}] {name} (compute {cap[0]}.{cap[1]})")
                print(ok("CUDA works — model can be trained on GPU."))
            else:
                print(warn("torch is installed but CUDA is NOT available."))
                print("        You are likely on a CPU-only torch build or a CPU box.")
                print("        On the GPU cloud machine use the cu121/cu126 wheel.")
                failures += 1
        except Exception as exc:  # noqa: BLE001
            print(bad(f"PyTorch import raised: {exc}"))
            failures += 1

    # 4. Required packages ------------------------------------------------
    heading("4. From-scratch packages")
    required = [
        ("numpy", "NumPy"),
        ("tokenizers", "HuggingFace Tokenizers"),
        ("safetensors", "safetensors"),
        ("yaml", "PyYAML"),
        ("tqdm", "tqdm"),
        ("datasets", "datasets (optional)"),
    ]
    for mod, label in required:
        ver = check_module(mod)
        if ver:
            print(ok(f"{label:<28} {ver}"))
        else:
            print(warn(f"{label:<28} not installed"))

    # 5. Summary ----------------------------------------------------------
    heading("Summary")
    if failures:
        print(f"{RED}Some checks failed ({failures}). See messages above.{RESET}")
    else:
        print(f"{GREEN}All critical checks passed — environment is ready.{RESET}")

    recs = recommend_install()
    if recs:
        print(warn("Suggested next command(s):"))
        for r in recs:
            print(f"        {r}")

    print(f"\n{BOLD}IMPORTANT:{RESET} ANKIT 0.1 is trained FROM SCRATCH. This script")
    print(f"never downloads or loads any pretrained model or tokenizer.")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
