#!/usr/bin/env bash
# ═══════════════════════════════════════════════════════════════════════════
# ANKIT 0.1 — FULL Class 1–4 foundation training driver.
#
# Chains the six curriculum stages (configs/curriculum/full_stage{1..6}.yaml)
# in order. Each stage resumes the SAME output_dir (checkpoints/ankit_full),
# so the chain is fully RESUMABLE: re-running this script skips stages whose
# target step is already reached and continues an interrupted stage.
#
# Between stages it runs the held-out generation quiz (evaluation/
# curriculum_eval.py, greedy) to watch for output collapse.
#
# Checkpoint hygiene: after a stage finishes, older step_* checkpoints are
# stripped to model-only (optimizer.pt deleted) — only the newest keeps full
# optimizer state for the next stage's resume. best_step_* (model-only) is
# always preserved.
#
# Usage:  bash scripts/run_full_training.sh
# ═══════════════════════════════════════════════════════════════════════════
set -u
cd "$(dirname "$0")/.."

export OMP_NUM_THREADS=2
export MKL_NUM_THREADS=2
export PYTHONHASHSEED=1337

OUT=checkpoints/ankit_full
mkdir -p "$OUT" evaluation/results/stage_evals
MASTER_LOG="$OUT/full_run.log"

log() {
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" | tee -a "$MASTER_LOG"
}

prune_old_checkpoints() {
  .venv/bin/python - <<'PY'
from pathlib import Path
import json
out = Path("checkpoints/ankit_full")
steps = sorted(
    (p for p in out.glob("step_*") if p.is_dir()),
    key=lambda p: int(p.name.split("_")[-1]),
)
if len(steps) > 1:
    for d in steps[:-1]:
        for f in ("optimizer.pt", "scheduler.pt"):
            fp = d / f
            if fp.exists():
                fp.unlink()
        print(f"[prune] {d.name}: stripped optimizer state (model-only kept)")
PY
}

latest_step() {
  .venv/bin/python - <<'PY'
from pathlib import Path
from training.checkpoint import latest_checkpoint
ck = latest_checkpoint(Path("checkpoints/ankit_full"))
print(int(ck.name.split("_")[-1]) if ck else 0)
PY
}

log "=== FULL CURRICULUM TRAINING START ==="
RUN_START=$(date +%s)

for n in 1 2 3 4 5 6; do
  CFG="configs/curriculum/full_stage${n}.yaml"
  TARGET=$(.venv/bin/python -c "import yaml;print(yaml.safe_load(open('$CFG'))['training']['total_steps'])")
  CUR=$(latest_step)
  if [ "$CUR" -ge "$TARGET" ]; then
    log "stage $n: already complete (step $CUR >= $TARGET) — skipping"
    continue
  fi
  log "=== STAGE $n START (resuming at step $CUR, target $TARGET) ==="
  STAGE_START=$(date +%s)
  .venv/bin/python training/train.py --config "$CFG" 2>&1 | tee "$OUT/train_stage${n}.log" | tee -a "$MASTER_LOG"
  RC=${PIPESTATUS[0]}
  STAGE_END=$(date +%s)
  if [ "$RC" -ne 0 ]; then
    log "!!! stage $n FAILED (rc=$RC) after $((STAGE_END - STAGE_START))s — stopping the chain"
    exit "$RC"
  fi
  log "=== STAGE $n DONE in $((STAGE_END - STAGE_START))s ==="

  # Held-out quiz between stages (greedy generation on 102 fixed tasks).
  QUIZ_OUT="evaluation/results/stage_evals/stage${n}_quiz.json"
  log "stage $n: running held-out generation quiz..."
  .venv/bin/python evaluation/curriculum_eval.py \
    --ckpt "$OUT" --mode generate --save "$QUIZ_OUT" \
    > "$OUT/quiz_stage${n}.log" 2>&1
  if [ -f "$QUIZ_OUT" ]; then
    .venv/bin/python -c "
import json
r = json.load(open('$QUIZ_OUT'))
g = r.get('generate', {})
print('[quiz] correct', g.get('correct'), '/', g.get('total'), '| accuracy', g.get('accuracy'))" \
      | tee -a "$MASTER_LOG"
  fi

  # Trim optimizer state from superseded checkpoints.
  prune_old_checkpoints | tee -a "$MASTER_LOG"
done

# Final: held-out TEST split loss (never seen in training).
log "=== running final held-out TEST-split loss evaluation ==="
.venv/bin/python evaluation/curriculum_eval.py \
  --ckpt "$OUT" --mode loss \
  --test data/curriculum/test.jsonl \
  --save evaluation/results/stage_evals/final_test_loss.json \
  > "$OUT/final_test_eval.log" 2>&1
log "=== FULL CURRICULUM TRAINING COMPLETE in $(( $(date +%s) - RUN_START ))s ==="
