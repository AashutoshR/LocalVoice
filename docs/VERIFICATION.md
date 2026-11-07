# Spanish implementation verification · 31 October 2026

- Active language: Spanish (`es`), FLEURS `es_419`.
- Full dataset validation passed: 4,110 clips; 2,796 training clips / 8.81 hours; 407 validation clips / 1.34 hours; 907 test clips / 3.08 hours. Missing speaker IDs remain an explicit limitation.
- CUDA PyTorch 2.10.0+cu128 detects the RTX 4060 Laptop GPU.
- Spanish pretrained baseline: validation WER 20.7911%, CER 6.5032%, 407 clips. Final test data remains held out.
- Ten automated tests pass, including normalization/scoring, audio handling, augmentation, leakage/duplicates, API validation, training-only sample selection, GPU job isolation, and signed/matching-data report comparisons.
- JavaScript syntax, Python compilation, and installed dependency checks pass.
- Browser checks covered the bento board, readable pending/measured states, keyboard audio tabs, skip navigation, horizontally scrollable tables, live progress semantics, text contrast, and mobile reflow. Details and limitations are in `docs/DESIGN_REVIEW.md`.

The real five-experiment series is running sequentially; completed validation metrics appear in `runs/E*/` and the README/results report. Training progress and epoch history are not final accuracy findings. No fine-tuning gain is asserted until evaluation is complete. The comparison report is regenerated after each evaluation.

The published application, active configuration and experiment evidence are Spanish-only. Machine-local archives and cleanup notes are excluded from the source distribution.


## Community skill review update

The five requested Community instruction sets were installed and applied. Current coverage and limitations are in [the review index](reviews/README.md); this supersedes earlier Figma-installation-pending statements. Browser evidence includes the live mobile overview and the separate eight-tile brand board. JavaScript syntax and the existing 10-test suite passed during the implementation pass.


## Final Spanish accuracy verification · 31 October 2026

21 tests passed; Python compilation and JavaScript syntax checks passed. The real-browser playground defaulted to E8, loaded the Spanish training sample, compared E7/E8 using CUDA, and displayed transcripts with diagnostic clip scores. Benchmark verification remained separate: both Small models completed all 907 held-out clips under the same generation digest. The tuned model reduced test WER from 6.3433% to 5.6165% and CER from 2.1573% to 1.7999%. Tiny also improved on its matching test baseline. See [the measured summary](IMPROVEMENT_SUMMARY.md), `runs/playground-smoke.json`, and `accuracy-results-preview.png`.


## Fine-tuning follow-up · 1 November 2026

- 30 automated tests pass, including actual CPU optimizer/checkpoint selection, tokenizer save/reload, KD gradient isolation, padding masks, additional-data leakage checks, and the train-only manifest regression.
- E10–E15 completed actual GPU fine-tuning/evaluation on the existing Tiny/Small backbones. Saved encoder/decoder audits and initial-weight hashes are retained. Failed hypotheses are preserved as evaluated regressions.
- E13 uses 5,796 training clips / 21.2751 hours, including 3,000 official Spanish MLS train clips from 21 speakers. Source LFS checksums pass; added speakers do not overlap the reserved MLS dev/test speakers.
- The 300-clip seed-43 follow-up was frozen before selecting E13/E14. E0/E11/E13/E14 use identical batch-four float32 greedy decoding. E13 reduces audiobook WER 23.9306 → 20.2720 and CER 7.5408 → 6.4680, removing 390 errors; speaker-bootstrap WER reduction interval 2.4824–4.8405 pp. This is exploratory after an earlier MLS test informed the domain choice.
- The original 407-clip FLEURS comparison remains unchanged: best Tiny E11 18.3959% WER; E13 18.9127%; E14 18.9624%. The broader-data recipe is not claimed to beat E11 on FLEURS.
- Small E15's higher decoder learning rate regresses; selection retains E10 at 5.6052% validation WER. Reused FLEURS test diagnostic: 5.6466% WER / 1.8073% CER on 907 clips, with canonical generation controls. Original test artifacts are preserved; this is not a new blind study.
- A train-only supplement initially hit the default three-split validator before any optimizer step; corrected with explicit required splits and an integration regression test. Failed preflight logs are archived. Two new sample metadata fingerprints were corrected to use canonical CSV-loaded rows before their evaluation; IDs, references and audio were unchanged, and original metadata/correction records are retained under archives/spanish-preflight/.

- Live browser GPU smoke tests passed for E0/E13 and E7/E10 on the fixed first FLEURS training sample. Tiny: 20% → 0% clip WER; Small: 10% → 10% clip WER and 3.2% → 1.6% clip CER. These are training-clip functional diagnostics, not benchmark or speed claims. Observed UI results are saved in runs/playground-smoke-20261101.json.
- The live research report renders four comparison tables, with no browser errors and no page overflow at the current 390px viewport. The checkpoint picker groups the same two backbones. Final results view: docs/fine-tuning-results-20261101.png; Tiny diagnostic view: docs/tiny-playground-20261101.png.
- A small, versionable evidence snapshot without audio/weights is available in docs/evidence/fine-tuning-20261101.json.


## Regularized LoRA and Latin American replay round · 1 November 2026

- Full automated suite: **35 passed**, including real CPU LoRA gradients, frozen
  base weights, merged-logit equivalence, saved adapter audits, checkpoint tamper
  rejection, natural target text preservation, and transient Windows file-lock recovery.
- E16 is a real completed RTX 4060 LoRA training run, reloaded and merged for scoring;
  48 saved B tensors updated. Its FLEURS regression remains visible.
- E17 completed 545 actual optimizer updates. A Windows metadata replacement lock
  occurred after training completed; intact final metadata was recovered from the
  temporary file, with a recovery record. The checkpoint was not retrained or altered.
- OpenSLR61 training/holdout IDs were frozen before E17 training. Audit verifies
  frozen fingerprints, no exact reference-text overlap, and actual training partition.
  Source speaker IDs are unavailable; speaker independence is not claimed.

- Completed all three reserved Latin American holdout evaluations after freezing
  checkpoint hashes: E0 24.42%, E11 24.97%, E17 19.80% WER. Source FLEURS
  regression remains 18.40% → 18.64%; E11 stays selected for that corpus.
- Browser smoke: real CUDA E0/E17 and E7/E16 transcription on the fixed first
  FLEURS training clip. Tiny sample WER changes 20% → 10%; Small remains 10%.
  These training-clip checks verify functionality only, not benchmark gains or speed.
  Actual displayed transcripts saved in `runs/playground-smoke-regularized-20261101.json`.
- Reporting/API regression checks after adding holdout tables: 9 passed. JavaScript
  syntax check passed. Main full-suite count remains 35 passed.


## Research-method implementation round · 1 November 2026

- Full automated suite after adding the EWC follow-up: **38 passed**, with the
  existing Starlette deprecation and Transformers generation-config warnings.
- Six real sequential RTX 4060 training/evaluation jobs completed: E18–E23,
  3,479 optimizer updates in total. All final scores come from reloaded checkpoints.
- Actual-input audit verifies equal initial weights, training audio/text hashes,
  learning rates, Spanish prefix and generation rules within both comparisons.
- E19: 94 protected tensors unchanged; E20: 139 unchanged. Trainable counts and
  measured allocated-memory peaks are preserved in training metadata.
- Fisher importance uses 128 original training clips only, with verified sample,
  checkpoint and tensor hashes. Unit tests reject changed anchors/data and tampering.
  Empirical-Fisher estimation and writing took 14.1 seconds, excluding earlier model
  loading and data preparation. Both penalties ran with finite, nonzero loss terms.
- Small retained E18: 5.5655% WER, four fewer errors versus E10. Tiny retained E11:
  18.3959%; E22 improves its matched E21 control by nine errors but does not beat E11.
  E23's stronger penalty regresses. No existing test corpus informed selection.
- Original and follow-up selections are separate, preserving both first outcomes.
  Final reports identify single-seed validation findings and unverified generalization.
- Real browser CUDA transcription succeeded for E7/E20 and E0/E22 on the same fixed
  training sample. Small clip WER remains 10%; Tiny changes 20% → 10%. These are
  functional checks only. Actual visible outputs are saved in
  `runs/playground-smoke-research-methods.json`.
- Website shows all six completed rows and exact error comparisons, with a 23.1%
  training-memory reduction for nine-block freezing. JavaScript syntax checks pass.

- Final research report renders eight tables with measured results. Browser console
  has no errors and the document has no horizontal overflow. Completed comparison
  screenshot: `docs/research-method-results-20261101.png`.
