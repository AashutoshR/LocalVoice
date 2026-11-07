"""Freeze validation-only selection, then evaluate baseline and winner on test."""
import hashlib
import json
import os
import subprocess
import sys
import time
from datetime import datetime, timezone
from .core import ROOT, config, experiment_config, experiments, write_json
from .reporting import MATCH, compatible_metrics, write_results


def choose(runs, baseline_id="E0"):
    baseline = next(r["metrics"] for r in runs if r["id"] == baseline_id)
    candidates = [r for r in runs if r["id"] != baseline_id and r.get("strategy") != "baseline" and r["metrics"] and
                  r["metrics"].get("split") == "validation" and
                  compatible_metrics(r["metrics"], baseline)]
    if not candidates:
        raise ValueError("No compatible validation candidates")
    return min(candidates, key=lambda r: r["metrics"]["wer"])


def run(wait=False, baseline_id="E0", tag=None):
    small = baseline_id == "E7"
    prior = ROOT / ("runs/accuracy.json" if small else "runs/improvement.json")
    deadline = time.monotonic() + 7200
    while wait and prior.exists() and json.loads(prior.read_text(encoding="utf-8")).get("status") == "running":
        if time.monotonic() > deadline:
            raise TimeoutError("Improvement series did not finish within two hours")
        time.sleep(2)
    if prior.exists() and json.loads(prior.read_text(encoding="utf-8")).get("status") != "completed":
        raise RuntimeError("Finish the improvement series before freezing selection")
    winner = choose(experiments(), baseline_id)
    from .diagnostics import compare_predictions
    for run_info in experiments():
        if run_info.get("strategy") != "baseline" and run_info.get("baseline_id", "E0") == baseline_id and (ROOT / "runs" / run_info["id"] / "predictions-validation.json").exists():
            compare_predictions(run_info["id"], baseline_id=baseline_id)
    folder = ROOT / "runs" / winner["id"] / "checkpoint"
    hashes = {str(p.relative_to(folder)): hashlib.sha256(p.read_bytes()).hexdigest()
              for p in sorted(folder.rglob("*")) if p.is_file()}
    selection = {"selected_experiment": winner["id"], "selection_split": "validation",
                 "validation_wer": winner["metrics"]["wer"], "project": experiment_config(winner["id"]), "baseline_id": baseline_id,
                 "dataset_fingerprint": winner["metrics"]["dataset_fingerprint"],
                 "generation_config_sha256": winner["metrics"].get("generation_config_sha256"),
                 "checkpoint_sha256": hashes, "frozen_at": datetime.now(timezone.utc).isoformat(),
                 "policy": "No further tuning or selection based on the held-out test results"}
    suffix = "-" + tag if tag else "-small" if small else ""
    selection_path = ROOT / f"runs/selection{suffix}.json"
    if selection_path.exists():
        previous = json.loads(selection_path.read_text(encoding="utf-8"))
        if any(previous[k] != selection[k] for k in ("selected_experiment", "checkpoint_sha256", "project")):
            raise RuntimeError("Selection is already frozen to a different checkpoint")
    else:
        write_json(selection_path, selection)
    state = {"status": "running", "pid": os.getpid(), "project": experiment_config(winner["id"]),
             "started_at": datetime.now(timezone.utc).isoformat(), "steps": []}
    path = ROOT / f"runs/finalization{suffix}.json"
    try:
        for experiment in (baseline_id, winner["id"]):
            state.update(experiment=experiment, action="held-out test evaluation")
            write_json(path, state)
            metrics_path = ROOT / "runs" / experiment / "metrics-test.json"
            if metrics_path.exists():
                state["steps"].append({"experiment": experiment, "reused": True})
                continue
            with (ROOT / "runs" / f"{experiment}-test.log").open("w", encoding="utf-8") as log:
                result = subprocess.run([sys.executable, "-u", "-m", "localvoice.cli", "evaluate", experiment,
                                         "--split", "test", "--final-test"], cwd=ROOT,
                                        env={**os.environ, "PYTHONUTF8": "1"}, stdout=log, stderr=subprocess.STDOUT)
            state["steps"].append({"experiment": experiment, "exit_code": result.returncode})
            if result.returncode:
                raise RuntimeError(f"{experiment} test evaluation failed; inspect its log")
        compare_predictions(winner["id"], "test", baseline_id=baseline_id)
        write_results()
        state["status"] = "completed"
    except BaseException as exc:
        state.update(status="failed", error=str(exc))
        raise
    finally:
        state["updated_at"] = datetime.now(timezone.utc).isoformat()
        write_json(path, state)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--wait", action="store_true", help="Wait for the improvement series to finish first")
    parser.add_argument("--baseline", choices=["E0", "E7"], default="E0")
    parser.add_argument("--tag", choices=["aligned-tiny"], default=None)
    args = parser.parse_args()
    run(args.wait, args.baseline, args.tag)
