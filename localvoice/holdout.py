"""Evaluate a frozen local holdout without replacing primary validation metrics."""
import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from .core import ROOT, dataset_fingerprint, experiment_config, read_manifest, write_json


def evaluate(experiment, selection_file, split="latin-holdout"):
    from .inference import load_model
    from .training import evaluate_rows
    selection = json.loads((ROOT/selection_file).read_text(encoding="utf-8"))
    if split=="latin-holdout":
        from .latin_spanish import audit_partition
        audit_partition()
    if experiment not in selection["evaluation_order"]:
        raise ValueError("Model not prespecified for this holdout")
    if split != selection["split"]:
        raise ValueError("Holdout split does not match frozen selection")
    rows = read_manifest(ROOT/selection["manifest"])
    if any(r["split"] != "test" for r in rows) or dataset_fingerprint(rows) != selection["dataset_fingerprint"]:
        raise ValueError("Holdout changed after freezing")
    for name, expected in selection.get("checkpoint_files",{}).get(experiment,{}).items():
        if Path(name).name != name:
            raise ValueError("Invalid checkpoint filename")
        with (ROOT/"runs"/experiment/"checkpoint"/name).open("rb") as stream:
            if hashlib.file_digest(stream,"sha256").hexdigest()!=expected:
                raise ValueError("Checkpoint changed after selection")
    folder=ROOT/"runs"/experiment
    if (folder/f"metrics-{split}.json").exists():
        raise FileExistsError("Preserve the first holdout evaluation")
    cfg=experiment_config(experiment)
    processor,model,device=load_model(experiment)
    evaluate_rows(model,processor,rows[:1],device)
    metrics,predictions=evaluate_rows(model,processor,rows,device,
        progress_path=folder/"holdout-progress.json",context=dict(split=split,evaluation_batch_size=4))
    metrics.update(split=split,dataset="OpenSLR 61",dataset_fingerprint=selection["dataset_fingerprint"],
        model=cfg["model"],model_revision=cfg["model_revision"],language="spanish",normalization=cfg["normalization"],
        evaluation_protocol=dict(batch_size=4,precision="float32",num_beams=1,max_new_tokens=225),
        generation_config_sha256=getattr(model,"_localvoice_generation_sha256",None),
        inference_parameters=sum(p.numel() for p in model.parameters()),
        selection_file=selection_file,device=device,license="CC-BY-SA-4.0",
        evaluation_context="New locally held-out, text-disjoint clips. Speaker IDs unavailable; no speaker-independence claim. Pretraining overlap unknown.",
        evaluated_at=datetime.now(timezone.utc).isoformat())
    write_json(folder/f"predictions-{split}.json",predictions)
    write_json(folder/f"metrics-{split}.json",metrics)
    print(json.dumps(metrics,ensure_ascii=False),flush=True)


if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("experiment")
    parser.add_argument("--selection",required=True)
    args=parser.parse_args()
    evaluate(args.experiment,args.selection)
