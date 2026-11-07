"""Publish measured comparisons into documentation after each evaluation."""
from datetime import datetime, timezone
from .core import ROOT, config, experiments

MATCH = ("split", "dataset_fingerprint", "model", "model_revision", "language", "normalization")


def compatible_metrics(a, b):
    legacy = {"batch_size": 1, "precision": "float32", "num_beams": 1, "max_new_tokens": 225}
    return bool(a and b and all(a.get(k) is not None and a[k] == b.get(k) for k in MATCH)
                and a.get("evaluation_protocol", legacy) == b.get("evaluation_protocol", legacy)
                and (not a.get("generation_config_sha256") or not b.get("generation_config_sha256")
                     or a["generation_config_sha256"] == b["generation_config_sha256"]))


def comparison_markdown():
    runs = experiments()
    baseline = runs[0]["metrics"]
    lines = ["## Measured Spanish results", "",
             "Validation findings are provisional. Held-out test evaluation remains separate. Negative reductions are regressions; missing runs are pending.", "",
             "| Run | WER | CER | WER reduction vs matched baseline | Trainable weights | Training time |", "| --- | --- | --- | --- | --- | --- |"]
    for run in runs:
        m = run["metrics"]
        if not m:
            lines.append(f"| {run['id']} · {run['name']} | Pending | Pending | — | — | — |")
            continue
        reference_id = run.get("baseline_id", "E0")
        reference = next((r["metrics"] for r in runs if r["id"] == reference_id), None)
        compatible = compatible_metrics(m, reference)
        delta = f"{reference['wer'] - m['wer']:+.2f} pp vs {reference_id}" if compatible and run["id"] != reference_id else "—"
        lines.append(f"| {run['id']} · {run['name']} | {m['wer']:.2f}% | {m['cer']:.2f}% | {delta} | {m['trainable_parameters']:,} | {m['training_seconds'] / 60:.1f} min |")
    if baseline:
        lines += ["", f"Base model: `{config()['model']}`. Language: Spanish. Baseline evaluation: {baseline['samples']} clips, `{baseline['split']}` split. Each comparison also requires the same dataset fingerprint and normalization."]
        candidates = [r for r in runs if r["id"] != "E0" and r["metrics"] and
                      all(r["metrics"].get(k) is not None and r["metrics"][k] == baseline.get(k) for k in MATCH)]
        if candidates:
            best = min(candidates, key=lambda r: r["metrics"]["wer"])
            m = best["metrics"]
            reduction = baseline["wer"] - m["wer"]
            relative = 100 * reduction / baseline["wer"] if baseline["wer"] else 0
            lines += ["", f"Lowest measured Tiny tuned WER: **{best['id']} · {m['wer']:.2f}%**. "
                      f"Versus E0: **{reduction:+.2f} percentage points** WER reduction "
                      f"(**{relative:+.2f}% relative**), and **{baseline['cer'] - m['cer']:+.2f} points** CER reduction."]
    if any(r["id"] in {"E5", "E6"} for r in runs):
        lines += ["", "E5/E6 are follow-up recipe experiments, not replacements for E1–E4. "
                  "They use lower learning rates, effective batch 32, restored training punctuation/casing, "
                  "and weight decay 0.05. See `docs/FINE_TUNING_IMPROVEMENTS.md` for exact settings. "
                  "Several settings changed together; gains cannot be attributed to one change alone."]
    if any(r.get("known_issues") for r in runs):
        lines += ["", "E1–E6 preserve measurements from a superseded tokenizer-prompt setup. "
                  "The fast tokenizer omitted Spanish/task tokens from training labels; E9 explicitly aligns and verifies them. "
                  "See `docs/TRAINING_PREFIX_FIX.md`. The original pretrained generation baselines are unaffected."]
    small = [r for r in runs if r.get("baseline_id") == "E7"]
    if small:
        lines += ["", "### Whisper Small accuracy track", "",
                  "E7 is the original Whisper Small checkpoint; E8 tunes its decoder while freezing its audio encoder. E10 also adapts the encoder. "
                  "E8 versus E7 measures fine-tuning. Small versus Tiny also changes the base model and is not a pure tuning gain. "
                  "Small runs use batch-four float32 greedy evaluation, with amortized generation time per clip. "
                  "Tiny timings use single-clip generation."]
        reference = next((r["metrics"] for r in small if r["id"] == "E7"), None)
        for r in small:
            m = r["metrics"]
            if r["id"] != "E7" and compatible_metrics(m, reference):
                delta = reference["wer"] - m["wer"]
                lines += ["", f"**{r['id']} fine-tuning gain versus E7: {delta:+.2f} pp WER "
                          f"({100 * delta / reference['wer']:+.2f}% relative)**. "
                          f"CER reduction: {reference['cer'] - m['cer']:+.2f} pp."]
    tested = [r for r in runs if r.get("test_metrics")]
    if tested:
        lines += ["", "### Original FLEURS test after the earlier frozen selection", "",
                  "These checkpoints were chosen using validation scores before the original test evaluation. "
                  "That test has already been reported and is not fresh evidence for the later E10/E11 development round.", "",
                  "| Run | Test WER | Test CER | Test clips |", "| --- | --- | --- | --- |"]
        for r in tested:
            m = r["test_metrics"]
            lines.append(f"| {r['id']} · {r['name']} | {m['wer']:.2f}% | {m['cer']:.2f}% | {m['samples']} |")
        for r in tested:
            m = r["test_metrics"]
            reference_id = r.get("baseline_id", "E0")
            test_base = next((other["test_metrics"] for other in tested if other["id"] == reference_id), None)
            if r["id"] != reference_id and compatible_metrics(m, test_base):
                delta = test_base["wer"] - m["wer"]
                relative = 100 * delta / test_base["wer"] if test_base["wer"] else 0
                lines += ["", f"{r['id']} held-out WER reduction versus {reference_id}: **{delta:+.2f} pp ({relative:+.2f}% relative)**."]
    independent = [r for r in runs if r.get("independent_metrics")]
    if independent:
        lines += ["", "### Spanish MLS: historical test and reused diagnostic", "",
                  "Fixed 300-clip sample from 20 speakers; 1.276 hours. Selection is frozen in `runs/selection-acoustic.json` "
                  "using FLEURS validation only. All models use the same batch-four float32 greedy decoding. "
                  "MLS is a separate audiobook domain. These scores belong to the frozen E10/E11 round; "
                  "later recipes are exploratory and do not inherit this holdout's independence. Pretraining overlap is unknown.", "",
                  "| Run | MLS WER | MLS CER | Clips |", "| --- | --- | --- | --- |"]
        for r in independent:
            m = r["independent_metrics"]
            lines.append(f"| {r['id']} · {r['name']} | {m['wer']:.2f}% | {m['cer']:.2f}% | {m['samples']} |")
        for r in independent:
            m = r["independent_metrics"]
            reference_id = r.get("baseline_id", "E0")
            reference = next((b["independent_metrics"] for b in independent if b["id"] == reference_id), None)
            if r["id"] != reference_id and compatible_metrics(m, reference):
                delta = reference["wer"] - m["wer"]
                lines += ["", f"{r['id']} MLS WER reduction versus {reference_id}: **{delta:+.2f} pp "
                          f"({100 * delta / reference['wer']:+.2f}% relative)**."]
    followup = [r for r in runs if r.get("followup_metrics")]
    if followup:
        lines += ["", "### New-clip MLS dev follow-up (exploratory)", "",
                  "A fixed seed-43 sample of 300 previously unused dev clips. The earlier MLS test was already read before this data-focused round, "
                  "so this is an exploratory follow-up, not a fully blind study. The listed checkpoints were frozen before these scores; later rounds are reported separately. "
                  "All Tiny checkpoints use the same batch-four float32 greedy decoding.", "",
                  "| Run | MLS dev WER | MLS dev CER | Clips |", "| --- | --- | --- | --- |"]
        reference = next((r["followup_metrics"] for r in followup if r["id"] == "E0"), None)
        for r in followup:
            m = r["followup_metrics"]
            lines.append(f"| {r['id']} · {r['name']} | {m['wer']:.2f}% | {m['cer']:.2f}% | {m['samples']} |")
        for r in followup:
            m = r["followup_metrics"]
            if r["id"] != "E0" and compatible_metrics(m, reference):
                delta = reference["wer"] - m["wer"]
                lines += ["", f"{r['id']} MLS dev WER reduction versus E0: **{delta:+.2f} pp "
                          f"({100 * delta / reference['wer']:+.2f}% relative)**.", ""]
    latin = [r for r in runs if r.get("latin_metrics")]
    if latin:
        lines += ["", "### Latin American text-disjoint holdout", "",
                  "300 locally untrained recordings reserved before E17 training; no exact transcript overlap with FLEURS or added training. Speaker IDs are unavailable; pretraining overlap is unknown.", "",
                  "| Tiny checkpoint | WER | CER | Clips |", "| --- | --- | --- | --- |"]
        for r in latin:
            m = r["latin_metrics"]
            lines.append(f"| {r['id']} · {r['name']} | {m['wer']:.2f}% | {m['cer']:.2f}% | {m['samples']} |")
    lines += ["", "Recipes: `docs/ACOUSTIC_ADAPTATION.md`, `docs/TEACHER_REGULARIZED_TUNING.md`, `docs/DIVERSE_DATA_TUNING.md`. Training time includes the parent stage for warm-started runs.", "",
              "Exact errors, memory, latency, hyperparameters, checkpoint selection, and epoch history are available in the website and `runs/E*/` artifacts.", "",
              f"Generated from local artifacts at {datetime.now(timezone.utc).isoformat()}."]
    return "\n".join(lines)


def write_results():
    # Integration smoke fixtures intentionally have no project documentation.
    if not (ROOT / "README.md").exists():
        return
    section = comparison_markdown()
    (ROOT / "docs/RESULTS.md").write_text("# Spanish fine-tuning results\n\n" + section + "\n", encoding="utf-8")
    path = ROOT / "README.md"
    text = path.read_text(encoding="utf-8")
    start, end = "<!-- MEASURED_RESULTS_START -->", "<!-- MEASURED_RESULTS_END -->"
    block = f"{start}\n{section}\n{end}"
    if start in text and end in text:
        before, rest = text.split(start, 1)
        _, after = rest.split(end, 1)
        text = before + block + after
    else:
        text += "\n\n" + block + "\n"
    path.write_text(text, encoding="utf-8")
