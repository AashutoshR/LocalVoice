"""Freeze validation choices, then run the reserved independent test exactly once."""
import hashlib
import json
import os
import subprocess
import sys
import time
from datetime import datetime, timezone
from .core import ROOT, experiments, write_json
from .reporting import compatible_metrics


def choose(runs, baseline_id, candidates):
    baseline = next(r for r in runs if r["id"] == baseline_id)
    eligible = [r for r in runs if r["id"] in candidates and
                compatible_metrics(r.get("metrics"), baseline.get("metrics"))]
    if len(eligible) != len(candidates):
        raise ValueError("Every planned candidate needs a completed compatible validation evaluation")
    return min(eligible, key=lambda r: r["metrics"]["wer"])


def run():
    state = dict(status="queued", action="waiting for acoustic adaptation", experiment="",
                 started_at=datetime.now(timezone.utc).isoformat(), pid=os.getpid(), steps=[])
    path = ROOT / "runs/independent-evaluation.json"
    write_json(path, state)
    try:
        while True:
            jobs = [json.loads((ROOT / "runs" / name).read_text(encoding="utf-8"))
                    for name in ("adaptation.json", "refinement.json")]
            if any(job["status"] in {"failed", "interrupted"} for job in jobs):
                raise RuntimeError("Resolve failed training before independent testing")
            if all(job["status"] == "completed" for job in jobs):
                break
            time.sleep(10)
        runs = experiments()
        small = choose(runs, "E7", {"E8", "E10"})
        tiny = choose(runs, "E0", {"E9", "E11"})
        selected = [tiny["id"], small["id"]]
        order = list(dict.fromkeys(["E0", "E9", tiny["id"], "E7", "E8", small["id"]]))
        hashes = {}
        for experiment in order:
            weights = ROOT / "runs" / experiment / "checkpoint/model.safetensors"
            if weights.exists():
                with weights.open("rb") as stream:
                    hashes[experiment] = hashlib.file_digest(stream, "sha256").hexdigest()
        selection_path = ROOT / "runs/selection-acoustic.json"
        if selection_path.exists():
            raise FileExistsError("Do not replace a frozen selection")
        write_json(selection_path, dict(selected_experiments=selected,
            validation_wer={r["id"]: r["metrics"]["wer"] for r in (tiny, small)},
            candidates={"tiny": ["E9", "E11"], "small": ["E8", "E10"]},
            evaluation_order=order, checkpoint_sha256=hashes,
            criterion="lowest FLEURS validation WER within each backbone; prior candidate retained if better",
            independent_sample=json.loads((ROOT / "data/independent-mls/sample.json").read_text(encoding="utf-8"))["dataset_fingerprint"],
            frozen_at=datetime.now(timezone.utc).isoformat(), independent_results_read=False))
        state.update(status="running", action="independent MLS test")
        for experiment in order:
            state["experiment"] = experiment
            write_json(path, state)
            command = [sys.executable, "-u", "-m", "localvoice.independent", "evaluate", experiment]
            with (ROOT / "runs" / f"{experiment}-independent.log").open("w", encoding="utf-8") as log:
                result = subprocess.run(command, cwd=ROOT, env={**os.environ, "PYTHONUTF8": "1"}, stdout=log, stderr=subprocess.STDOUT)
            state["steps"].append(dict(experiment=experiment, exit_code=result.returncode))
            if result.returncode:
                raise RuntimeError(f"{experiment} independent evaluation failed")
        from .diagnostics import compare_predictions
        for experiment, baseline in ((tiny["id"], "E0"), (small["id"], "E7")):
            compare_predictions(experiment, split="mls-test", baseline_id=baseline, cluster_field="speaker_id")
        from .reporting import write_results
        write_results()
        state["status"] = "completed"
    except BaseException as exc:
        state.update(status="failed", error=str(exc))
        raise
    finally:
        state["updated_at"] = datetime.now(timezone.utc).isoformat()
        write_json(path, state)


if __name__ == "__main__":
    run()
