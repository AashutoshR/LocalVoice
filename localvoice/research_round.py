"""Prespecified matched partial-freezing and EWC ablations; validation only."""
import hashlib
import json
import os
from datetime import datetime, timezone
from .core import ROOT, experiment_config, experiments, write_json


def run():
    path = ROOT / "runs/research-round.json"
    if path.exists():
        raise FileExistsError("Research round already exists; preserve its first execution")
    ids = ["E18", "E19", "E20", "E21", "E22"]
    recipes = {i: f"configs/research-{i.lower()}.json" for i in ids}
    state = dict(status="running", experiment=ids[0], action="matched ablation",
        project=experiment_config(ids[0]), pid=os.getpid(), started_at=datetime.now(timezone.utc).isoformat(),
        order=ids, recipe_sha256={i: hashlib.sha256((ROOT / p).read_bytes()).hexdigest() for i, p in recipes.items()},
        policy="Original FLEURS validation only for selection. No existing test or Latin holdout used for tuning.")
    write_json(path, state)
    try:
        from .train_stage import run as stage
        for identifier in ids:
            state.update(experiment=identifier, action="train and reload for validation", project=experiment_config(identifier))
            write_json(path, state)
            if identifier == "E21":
                from .fisher import prepare
                state["action"] = "estimate training-only Fisher at E11"
                write_json(path, state)
                prepare()
            if hashlib.sha256((ROOT / recipes[identifier]).read_bytes()).hexdigest() != state["recipe_sha256"][identifier]:
                raise ValueError("Prespecified recipe changed during the round")
            stage(identifier, recipes[identifier])
        runs = {r["id"]: r for r in experiments()}
        from .reporting import compatible_metrics, write_results
        groups = {"small": ["E8", "E10", "E15", "E16", "E18", "E19", "E20"],
                  "tiny": ["E9", "E11", "E13", "E14", "E17", "E21", "E22"]}
        selected = {}
        hashes = {}
        for model, candidates in groups.items():
            reference = runs["E7" if model == "small" else "E0"]["metrics"]
            if any(not compatible_metrics(reference, runs[i]["metrics"]) for i in candidates):
                raise ValueError("Mismatched validation protocol")
            winner = min(candidates, key=lambda i: runs[i]["metrics"]["wer"])
            selected[model] = dict(experiment=winner, validation_wer=runs[winner]["metrics"]["wer"],
                candidates={i:runs[i]["metrics"]["wer"] for i in candidates})
        for identifier in ids:
            hashes[identifier] = {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                                 for p in (ROOT / "runs" / identifier / "checkpoint").iterdir() if p.is_file()}
        write_json(ROOT / "runs/selection-research.json", dict(selected=selected, checkpoint_files=hashes,
            frozen_at=datetime.now(timezone.utc).isoformat(), policy=state["policy"]))
        from .diagnostics import compare_predictions
        for identifier in ("E19", "E20"):
            compare_predictions(identifier, baseline_id="E18", primary=False)
        compare_predictions("E22", baseline_id="E21", primary=False)
        write_results()
        state.update(status="completed", selected=selected)
    except BaseException as error:
        state.update(status="failed", error=str(error))
        raise
    finally:
        state["updated_at"] = datetime.now(timezone.utc).isoformat()
        write_json(path, state)


if __name__ == "__main__":
    run()
