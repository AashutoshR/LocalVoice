"""Write an honest, same-backbone before/after report from completed artifacts."""
import json
from datetime import datetime, timezone
from localvoice.core import ROOT, experiments, write_json
from localvoice.reporting import compatible_metrics


def errors(metrics):
    return sum(metrics[key] for key in ("substitutions", "deletions", "insertions"))


def main():
    runs = {r["id"]: r for r in experiments()}
    ids = ["E0", "E9", "E11", "E12", "E13", "E14", "E17"]
    if any(not runs[i]["metrics"] for i in ids):
        raise ValueError("Finish all planned Tiny validation evaluations before publishing")
    base = runs["E0"]["metrics"]
    if any(not compatible_metrics(base, runs[i]["metrics"]) for i in ids):
        raise ValueError("Before/after comparison protocol differs")
    chosen = min((runs[i] for i in ids if i != "E0"), key=lambda r: r["metrics"]["wer"])
    m = chosen["metrics"]
    relative = 100 * (base["wer"] - m["wer"]) / base["wer"]
    lines = ["# Fine-tuning the existing Spanish models", "",
        "Updated 1 November 2026. This round retains the existing Tiny and Small architectures. "
        "Run IDs identify training recipes/checkpoints, not additional backbones.", "",
        f"**Best Tiny FLEURS validation result: {chosen['id']} · {m['wer']:.2f}% WER, {m['cer']:.2f}% CER.** "
        f"The matching pretrained Tiny baseline is {base['wer']:.2f}% WER and {base['cer']:.2f}% CER: "
        f"{base['wer']-m['wer']:.2f} percentage points, or {relative:.1f}% relative WER reduction.", "",
        "## Same Tiny model, before and after", "",
        "All rows use the same original 407 FLEURS validation clips, normalization, "
        "pinned Tiny revision, float32 single-clip greedy decoding and token limit. "
        "Training data can differ; evaluation data does not.", "",
        "| Recipe | WER ↓ | CER ↓ | Word errors | Cumulative training time |",
        "| --- | --- | --- | --- | --- |"]
    for i in ids:
        r, value = runs[i], runs[i]["metrics"]
        lines.append(f"| {i} · {r['name']} | {value['wer']:.2f}% | {value['cer']:.2f}% | {errors(value):,} | {value['training_seconds']/60:.1f} min |")
    mixed, followup_base = runs["E13"].get("followup_metrics"), runs["E0"].get("followup_metrics")
    if mixed and followup_base:
        gain = 100 * (followup_base["wer"] - mixed["wer"]) / followup_base["wer"]
        lines[4:4] = [f"**Data-focused Tiny E13 improves the new audiobook sample from {followup_base['wer']:.2f}% to "
            f"{mixed['wer']:.2f}% WER ({gain:.1f}% relative reduction), with the same Tiny architecture.** "
            f"Its FLEURS validation WER is {runs['E13']['metrics']['wer']:.2f}%, versus pretrained {base['wer']:.2f}% "
            f"and previous best E11 {runs['E11']['metrics']['wer']:.2f}%. This is a domain tradeoff, not a claim that every metric or clip improves.", ""]
    prior = runs["E11"]["metrics"]
    change = prior["wer"] - m["wer"]
    lines += ["", f"Compared with the previous best E11 ({prior['wer']:.2f}% WER), the selected "
              f"checkpoint removes {change:.2f} pp WER. " +
              ("The newer recipes did not beat E11 on this split." if chosen["id"] == "E11" else
               f"That is {100*change/prior['wer']:.1f}% fewer word errors relative to E11."), "",
              "## Which errors changed", "",
              "| Error type | Pretrained Tiny | Selected Tiny | Fewer errors |", "| --- | --- | --- | --- |"]
    for key in ("substitutions", "deletions", "insertions"):
        lines.append(f"| {key.capitalize()} | {base[key]:,} | {m[key]:,} | {base[key]-m[key]:+,} |")
    paired = chosen.get("paired")
    lines += ["", f"Total word errors: {errors(base):,} → {errors(m):,}, "
              f"**{errors(base)-errors(m):,} fewer errors across {base['reference_words']:,} reference words**. "
              f"CER changes by {base['cer']-m['cer']:+.2f} percentage points."]
    if paired:
        lo, hi = paired["wer_reduction_95_interval_pp"]
        lines += ["", f"{paired['utterances_improved']} validation clips improve and {paired['utterances_worsened']} worsen. "
                  f"Paired utterance-bootstrap WER-reduction interval: {lo:.2f} to {hi:.2f} pp. "
                  "This interval is exploratory after validation selection; FLEURS speaker IDs are unavailable."]
    lines += ["", "## What changed in training", "",
        "- E11 increases Tiny's learning rate from 2e-6 to 1e-5, reduces effective batch 32 to 16, and adds light time masking. Validation exposes overfitting after epoch 2.",
        "- E12 tests a frozen pretrained Small teacher penalty on training clips. It worsens validation WER and is retained as a negative result, not promoted.",
        "- E13 expands unique training speech from 8.81 to 21.28 hours: 2,796 FLEURS clips plus 3,000 official Spanish MLS train clips from 21 speakers. Validation/test clips remain excluded.",
        "- E14 starts from E13 and briefly refines on FLEURS training at 2e-6, with augmentation disabled. Prior checkpoints remain available if refinement regresses.",
        "- Checkpoints are selected by full validation WER; saved weights are reloaded for final scoring. Multiple recipe settings change together, so one-factor causal attribution is not established.", "",
        f"The selected Tiny model still has **{chosen['training']['total_parameters']:,} total parameters** "
        f"and {chosen['training']['trainable_parameters']:,} trainable during fine-tuning. "
        "The teacher is not part of the deployed Tiny checkpoint. Training time includes parent stages and validation checks, but not dataset download/preparation. "
        "Measured latency is a local single-run benchmark, not evidence of a reliable speed improvement."]
    followup = [runs[i] for i in ("E0", "E11", "E13", "E14") if runs[i].get("followup_metrics")]
    if len(followup) != 4:
        raise ValueError("Complete the frozen new-clip follow-up before publishing the final report")
    reference = runs["E0"]["followup_metrics"]
    lines += ["", "## New audiobook clips: exploratory follow-up", "",
        "Fixed seed-43 sample of 300 previously unused MLS dev clips from 20 speakers; these speakers do not occur in the added training sample. "
        "All four Tiny checkpoints use the same batch-four float32 greedy protocol. The earlier MLS test was already read before choosing this data-focused recipe, "
        "so this is an exploratory follow-up, not a fully blind study. Those checkpoints were frozen before these scores; later rounds are reported separately.", "",
        "| Tiny recipe | MLS dev WER ↓ | MLS dev CER ↓ | Relative WER reduction vs pretrained |",
        "| --- | --- | --- | --- |"]
    for r in followup:
        value = r["followup_metrics"]
        if not compatible_metrics(reference, value):
            raise ValueError("Follow-up comparisons must match")
        gain = 100 * (reference["wer"] - value["wer"]) / reference["wer"]
        lines.append(f"| {r['id']} · {r['name']} | {value['wer']:.2f}% | {value['cer']:.2f}% | {gain:+.1f}% |")
    improved, old = runs["E13"]["followup_metrics"], runs["E11"]["followup_metrics"]
    paired_followup = json.loads((ROOT / "runs/E13/paired-mls-dev.json").read_text(encoding="utf-8"))
    lo, hi = paired_followup["wer_reduction_95_interval_pp"]
    lines += ["", f"E13 removes **{errors(reference)-errors(improved):,} word errors versus pretrained Tiny** "
        f"across {reference['reference_words']:,} reference words: "
        f"{reference['substitutions']-improved['substitutions']:,} fewer substitutions, "
        f"{reference['deletions']-improved['deletions']:,} fewer deletions, and "
        f"{reference['insertions']-improved['insertions']:,} fewer insertions. "
        f"Compared with E11, it removes {errors(old)-errors(improved):,} errors "
        f"({100*(old['wer']-improved['wer'])/old['wer']:.1f}% relative WER reduction).", "",
        f"{paired_followup['utterances_improved']} clips improve and {paired_followup['utterances_worsened']} worsen versus pretrained. "
        f"The paired speaker-cluster bootstrap interval for WER reduction is {lo:.2f} to {hi:.2f} percentage points "
        f"({paired_followup['sampling_units']} speaker clusters; 5,000 resamples). This describes uncertainty on this exploratory sample."]
    lines += ["", "FLEURS validation and MLS dev are different corpora and must not be combined into one score. "
        "A domain-specific gain does not establish improvement for every Spanish speaker, recording condition, or utterance. "
        "The original MLS test regressions remain in `docs/RESULTS.md`; its artifacts are unchanged. Whisper pretraining overlap with these public corpora is unknown.", "",
        "## Fine-tuning the existing Small decoder", ""]
    b, previous, acoustic = [runs[i]["metrics"] for i in ("E7", "E8", "E10")]
    if not runs["E15"]["metrics"]:
        raise ValueError("Finish Small refinement before publishing the final report")
    small = min((runs[i] for i in ("E8", "E10", "E15", "E16")), key=lambda r: r["metrics"]["wer"])
    lines += [f"The acoustic continuation only moved validation WER from {previous['wer']:.2f}% to "
        f"{acoustic['wer']:.2f}%, removing {errors(previous)-errors(acoustic)} additional errors. That step is marginal.", "",
        "E15 keeps E8's existing Small decoder and frozen encoder, raises learning rate from 2e-6 to 1e-5, "
        "and selects by validation with early stopping. It retains the same training clips, target text, effective batch 16 and model architecture.", "",
        "| Small recipe | Validation WER | Validation CER |", "| --- | --- | --- |"]
    for i in ("E7", "E8", "E10", "E15", "E16"):
        value = runs[i]["metrics"]
        if not compatible_metrics(value, b):
            raise ValueError("Small comparisons must use the matched Small baseline")
        lines.append(f"| {i} · {runs[i]['name']} | {value['wer']:.2f}% | {value['cer']:.2f}% |")
    value = small["metrics"]
    lines += ["", f"Selected Small checkpoint: **{small['id']}**, {value['wer']:.2f}% WER; "
        f"{100*(b['wer']-value['wer'])/b['wer']:.1f}% relative WER reduction versus pretrained Small. "
        "This comparison does not change backbone size."]
    if runs["E15"]["metrics"]["wer"] >= min(previous["wer"], acoustic["wer"]):
        lines += ["", "The higher-rate Small decoder recipe regressed and is not selected."]
    if small.get("test_metrics"):
        test, control = small["test_metrics"], runs["E7"]["test_metrics"]
        if not compatible_metrics(test, control):
            raise ValueError("Small test protocols differ")
        lines += ["", f"Reused 907-clip FLEURS test diagnostic: {control['wer']:.2f}% → {test['wer']:.2f}% WER "
            f"({100*(control['wer']-test['wer'])/control['wer']:.1f}% relative reduction); "
            f"{control['cer']:.2f}% → {test['cer']:.2f}% CER. "
            "The project had already examined this corpus in earlier rounds. The checkpoint choice was frozen using validation before this diagnostic; it is not a fresh blind study."]
        older = runs["E8"].get("test_metrics")
        if older and compatible_metrics(test, older):
            lines += ["", f"The original E8 decoder test WER was {older['wer']:.2f}%, versus {test['wer']:.2f}% for "
                f"{small['id']}. The later Small trials did not establish a meaningful improvement over E8."]
    lines += ["",
        "## Reproducible evidence", "",
        "- `runs/E*/training.json`, `history.json`, `metrics-validation.json`, `predictions-validation.json`: training, selection and exact recognition outputs.",
        "- `runs/E*/weight-audit.json`: actual saved encoder/decoder changes against each initial checkpoint.",
        "- `runs/selection-diverse.json`: hashes and validation choices frozen before follow-up evaluation.",
        "- `runs/E*/metrics-mls-dev.json`, `predictions-mls-dev.json`, `paired-mls-dev.json`: complete follow-up evidence and speaker-cluster bootstrap analysis.",
        "- `docs/DIVERSE_DATA_TUNING.md` and `docs/TEACHER_REGULARIZED_TUNING.md`: methods, data provenance, limitations and failed recipe.", ""]
    from scripts.report_latest_round import latest_section
    lines[4:4] = latest_section(runs)
    (ROOT / "docs/FINE_TUNING_COMPARISON.md").write_text("\n".join(lines), encoding="utf-8")
    write_json(ROOT / "runs/fine-tuning-summary.json", dict(selected_tiny=chosen["id"], selected_small=small["id"],
        baseline_wer=base["wer"], tuned_wer=m["wer"], relative_wer_reduction=relative,
        errors_removed=errors(base)-errors(m), generated_at=datetime.now(timezone.utc).isoformat()))
    print("Wrote docs/FINE_TUNING_COMPARISON.md")


if __name__ == "__main__":
    main()
