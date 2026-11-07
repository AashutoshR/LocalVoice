"""Execute one preserved fine-tuning recipe, then audit the saved checkpoint."""
import argparse
import json
import os
import subprocess
import sys
import time
from datetime import datetime, timezone
from .core import ROOT, EXPERIMENTS, experiment_config, write_json


def run(experiment, recipe):
    state = dict(status="running", experiment=experiment, action="train",
                 project=experiment_config(experiment), pid=os.getpid(),
                 started_at=datetime.now(timezone.utc).isoformat(), steps=[])
    path = ROOT / "runs/current-training.json"
    hp = json.loads((ROOT / recipe).read_text(encoding="utf-8"))
    write_json(path, state)
    try:
        for action in ("train", "evaluate"):
            state["action"] = action
            write_json(path, state)
            command = [sys.executable, "-u", "-m", "localvoice.cli", action, experiment]
            if action == "train":
                command += ["--config", recipe]
            with (ROOT / "runs" / f"{experiment}-{action}.log").open("w", encoding="utf-8") as log:
                result = subprocess.run(command, cwd=ROOT, env={**os.environ, "PYTHONUTF8": "1"}, stdout=log, stderr=subprocess.STDOUT)
            state["steps"].append(dict(action=action, exit_code=result.returncode))
            if result.returncode:
                raise RuntimeError(f"{experiment} {action} failed; inspect its log")
        from .diagnostics import compare_predictions
        spec = next(r for r in EXPERIMENTS if r["id"] == experiment)
        compare_predictions(experiment, baseline_id=spec.get("baseline_id", "E0"))
        from .weight_audit import audit, audit_adapter
        if spec["strategy"] == "lora":
            audit_adapter(experiment)
        elif hp.get("initialize_from"):
            audit(experiment, hp["initialize_from"])
        state["status"] = "completed"
    except BaseException as exc:
        state.update(status="failed", error=str(exc))
        raise
    finally:
        state["updated_at"] = datetime.now(timezone.utc).isoformat()
        write_json(path, state)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("experiment")
    parser.add_argument("recipe")
    parser.add_argument("--wait-for", default=None)
    parser.add_argument("--wait-source", default=None)
    args = parser.parse_args()
    if args.wait_for:
        while True:
            current = json.loads((ROOT / "runs/current-training.json").read_text(encoding="utf-8"))
            if current["experiment"] != args.wait_for:
                raise ValueError("Unexpected training stage while waiting")
            if current["status"] in {"failed", "interrupted"}:
                raise ValueError("Resolve the preceding training stage first")
            if current["status"] == "completed":
                break
            time.sleep(10)
    if args.wait_source:
        while not (ROOT / args.wait_source).is_file():
            time.sleep(10)
    run(args.experiment, args.recipe)
