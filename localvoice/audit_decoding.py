"""Verify final weights against the baseline's pinned decoding configuration."""
import json
import os
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from types import SimpleNamespace
from .core import ROOT, experiment_config, write_json
from .prompts import canonical_generation


def run():
    cfg = experiment_config("E8")
    state = {"status": "running", "pid": os.getpid(), "project": cfg,
             "started_at": datetime.now(timezone.utc).isoformat(), "experiment": "E8",
             "action": "matched decoding validation audit", "steps": []}
    job = ROOT / "runs/finish.json"
    write_json(job, state)
    archive = ROOT / "archives/decoding-audit/20261031-2253"
    try:
        source = ROOT / cfg["local_model_path"]
        model = SimpleNamespace(config=SimpleNamespace())
        digest = canonical_generation(model, cfg, source)
        model.generation_config.save_pretrained(ROOT / "runs/E8/checkpoint")
        for experiment in ("E7", "E8"):
            state.update(experiment=experiment, action="matched decoding validation audit")
            write_json(job, state)
            folder = ROOT / "runs" / experiment
            for name in ("metrics.json", "metrics-validation.json", "predictions-validation.json"):
                if (folder / name).exists():
                    shutil.copy2(folder / name, archive / f"{experiment}-{name}")
            with (ROOT / "runs" / f"{experiment}-canonical-validation.log").open("w", encoding="utf-8") as output:
                result = subprocess.run([sys.executable, "-u", "-m", "localvoice.cli", "evaluate", experiment],
                    cwd=ROOT, env={**os.environ, "PYTHONUTF8": "1"}, stdout=output, stderr=subprocess.STDOUT)
            if result.returncode:
                raise RuntimeError(f"{experiment} validation audit failed; inspect its log")
            measured = json.loads((folder / "metrics-validation.json").read_text(encoding="utf-8"))
            if measured.get("generation_config_sha256") != digest:
                raise RuntimeError("Matched decoding configuration verification failed")
            state["steps"].append({"experiment": experiment, "wer": measured["wer"], "generation_config_sha256": digest})
        state.update(status="completed", weights_changed=False, affected_special_tokens=[50358, 50359],
                     test_results_consulted=False, updated_at=datetime.now(timezone.utc).isoformat())
        write_json(ROOT / "runs/generation-audit.json", state)
    except BaseException as exc:
        state.update(status="failed", error=str(exc))
        write_json(job, state)
        raise
    from .finish import run as finish
    finish()


if __name__ == "__main__":
    run()
