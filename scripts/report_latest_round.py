"""Measured E16/E17 results; no synthetic scores or cross-backbone credit."""
from localvoice.public_evidence import write_public_snapshot
import json
from localvoice.core import ROOT, write_json
from localvoice.reporting import compatible_metrics


def latest_section(runs):
    small, old, base = (runs[i] for i in ("E16", "E10", "E7"))
    m, previous, control = (r["independent_metrics"] for r in (small, old, base))
    if not compatible_metrics(m, previous) or not compatible_metrics(m, control):
        raise ValueError("MLS comparison protocols differ")
    paired = json.loads((ROOT / "runs/E16/paired-mls-test-vs-E10.json").read_text(encoding="utf-8"))
    lo, hi = paired["wer_reduction_95_interval_pp"]
    v, ov = small["metrics"], old["metrics"]
    memory, old_memory = (r["training"]["peak_gpu_memory_mb"] for r in (small, old))
    lines = ["## Latest completed fine-tuning round: E16 and E17", "",
        "These are new training recipes on the two existing backbones. **Neither new recipe beats the retained FLEURS validation record.** "
        "Small LoRA reduces the audiobook regression and training memory; the separate Tiny replay result is below.", "",
        "| Existing Small checkpoint | FLEURS validation WER | Reused MLS WER | Reused MLS CER | Training peak allocated GPU memory |",
        "| --- | --- | --- | --- | --- |"]
    for r in (base, old, small):
        vm, tm, tr = r["metrics"], r["independent_metrics"], r.get("training")
        ram = f"{tr['peak_gpu_memory_mb']:.0f} MB" if tr and tr.get("peak_gpu_memory_mb") else "—"
        lines.append(f"| {r['id']} · {r['name']} | {vm['wer']:.2f}% | {tm['wer']:.2f}% | {tm['cer']:.2f}% | {ram} |")
    lines += ["", f"E16 removes **{paired['errors_removed']} word errors** versus full-tuned E10 across the same 300 MLS recordings: "
        f"{previous['wer']:.2f}% → {m['wer']:.2f}% WER (**{100*(previous['wer']-m['wer'])/previous['wer']:.1f}% relative reduction**). "
        f"CER improves {previous['cer']:.2f}% → {m['cer']:.2f}%. {paired['utterances_improved']} clips improve and {paired['utterances_worsened']} worsen. "
        f"Exploratory paired speaker-cluster bootstrap WER-reduction interval: {lo:.2f} to {hi:.2f} pp (20 clusters, 5,000 resamples).", "",
        "The gain is uneven: one avoided repetitive hallucination accounts for 157 of the 198 fewer errors. "
        "Against pretrained Small, E16 removes only 31 errors (8.16% → 7.89% WER); its interval crosses zero. "
        "This supports reduced forgetting relative to E10 on these known clips, not a robust general improvement over pretrained Small.", "",
        f"FLEURS validation worsens {ov['wer']:.2f}% → {v['wer']:.2f}% (24 additional errors), so E10 remains selected for that domain. "
        "The MLS corpus was already examined in earlier rounds; this is a reused diagnostic, not fresh blind evidence.", "",
        f"The recipe freezes all pretrained weights and trains **{small['training']['trainable_parameters']:,} decoder LoRA parameters** "
        f"(rank 8, dropout 0.1, adapter-only LR 1e-4). Peak allocated GPU memory falls {old_memory:.0f} → {memory:.0f} MB "
        f"({100*(old_memory-memory)/old_memory:.1f}% lower for these measured training recipes). "
        f"The merged model retains **{v['inference_parameters']:,} inference parameters**. "
        "All 48 saved adapter B tensors have nonzero updates; CPU gradient/merge checks establish that fine-tuning actually changes adapters while base weights stay frozen.", "",
        "### Tiny: Latin American speech with FLEURS replay", "",
        "E17 starts from E11 and fine-tunes the same Tiny weights at LR 5e-6 on 12.98 hours: original FLEURS training plus "
        "3,000 human Argentinian Spanish recordings (4.17 hours). Light time masking and early stopping constrain overfitting. "
        "The best checkpoint is at update 182; training stops at 545 updates after validation worsens.", "",
        f"Reloaded FLEURS validation WER: **{runs['E17']['metrics']['wer']:.2f}%**, versus E11 **{runs['E11']['metrics']['wer']:.2f}%**. "
        "E11 remains the FLEURS choice. A 300-clip, text-disjoint holdout was reserved before training; all three Tiny checkpoints were frozen before its scores were read.", "",
        "| Same Tiny backbone | Latin American holdout WER | CER | Word errors |", "| --- | --- | --- | --- |"]
    for identifier in ("E0", "E11", "E17"):
        value = runs[identifier]["latin_metrics"]
        if not value:
            raise ValueError("Finish the frozen holdout evaluation first")
        errors = sum(value[k] for k in ("substitutions", "deletions", "insertions"))
        lines.append(f"| {identifier} · {runs[identifier]['name']} | {value['wer']:.2f}% | {value['cer']:.2f}% | {errors:,} |")
    b, prior, after = (runs[i]["latin_metrics"] for i in ("E0", "E11", "E17"))
    if not compatible_metrics(b, after) or not compatible_metrics(prior, after):
        raise ValueError("Latin holdout protocols differ")
    from localvoice.diagnostics import compare_predictions
    change = compare_predictions("E17", split="latin-holdout", baseline_id="E11", primary=False)
    low, high = change["wer_reduction_95_interval_pp"]
    lines += ["", f"Compared with E11, E17 removes {change['errors_removed']:+,} word errors: "
        f"{change['utterances_improved']} clips improve and {change['utterances_worsened']} worsen. "
        f"Exploratory utterance-bootstrap WER-reduction interval: {low:.2f} to {high:.2f} pp. "
        "Speaker dependence cannot be accounted for because source speaker IDs are missing.", ""]
    lines += ["", f"Relative WER change for E17: {100*(b['wer']-after['wer'])/b['wer']:+.1f}% reduction versus pretrained Tiny; "
        f"{100*(prior['wer']-after['wer'])/prior['wer']:+.1f}% versus prior tuned E11. Negative values mean regression. "
        "All holdout scores use identical batch-four float32 greedy decoding. Speaker IDs are unavailable, so text disjointness does not establish speaker independence. "
        "Whisper pretraining overlap is unknown. No further E17 tuning uses these scores.", "",
        "Source: [OpenSLR 61](https://www.openslr.org/61/), Google Latin American Spanish corpus, **CC-BY-SA-4.0**. "
        "Keep this attribution/license with derived data and review its terms before redistributing derived artifacts. "
        "Methods: `docs/REGULARIZED_LORA_ROUND.md`, `docs/LATIN_REPLAY_ROUND.md`. "
        "Selection hashes, data audit, real predictions and weight audits are preserved under `runs/`.", "",
        "### Earlier rounds (historical)", ""]
    write_public_snapshot(ROOT / "docs/evidence/regularized-latin-round-20261101.json", {
        i: {k: runs[i].get(k) for k in ("id", "name", "metrics", "independent_metrics", "latin_metrics", "adapter_audit", "weight_audit")}
        for i in ("E0", "E11", "E17", "E7", "E10", "E16")})
    return lines
