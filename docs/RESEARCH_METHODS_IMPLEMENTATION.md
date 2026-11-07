# Controlled implementation of research fine-tuning methods

Started 1 November 2026. These experiments retain the existing Spanish Whisper Tiny and Small architectures. The original five checkpoints and stronger-EWC follow-up have completed saved-model validation. See [the measured comparisons](RESEARCH_METHOD_RESULTS.md); no broad accuracy gain is assumed.

## Small: partial lower-encoder freezing

The implementation in `localvoice/regularization.py` supports `freeze_encoder_layers` with strict bounds checking. Freezing N blocks also freezes the convolutional acoustic front end. The remaining encoder blocks, final encoder normalization and decoder remain trainable. This is a deliberate implementation choice inspired by [Liu et al., 2024](https://link.springer.com/article/10.1186/s13636-024-00349-3); it is not an exact reproduction of their large-v2 study.

| Recipe | Initialization | Frozen lower encoder blocks | Other settings |
| --- | --- | --- | --- |
| E18 control | Existing Small E8 checkpoint | 0 | Same as E19/E20 |
| E19 | Same E8 checkpoint | 6 of 12, plus acoustic front end | Same as E18/E20 |
| E20 | Same E8 checkpoint | 9 of 12, plus acoustic front end | Same as E18/E19 |

The starting point is the same already-tuned decoder checkpoint, E8, rather than introducing another pretrained backbone. E18 reruns the full-tuning acoustic continuation as an explicit contemporary control; E10 is retained as a historical comparison. All three recipes use the original 2,796 FLEURS training clips, encoder LR 2e-6, decoder LR 5e-7, effective batch 16, seed 42, AdamW weight decay 0.05, 5% warmup, identical SpecAugment masks, maximum four epochs and patience two validation checks. Full validation occurs at 88 within-epoch updates and epoch ends. Final Small scoring remains batch-four float32 greedy generation.

The variable is the freezing policy, not initialization, data or schedule. Effective optimizer parameter counts differ as a consequence of freezing. Early stopping can produce different actual update counts; both the planned schedule and completed counts are reported. No causal claim beyond this single-seed ablation is justified. Saved-weight audits explicitly verify that all protected convolution/block tensors match E8 exactly.

## Tiny: diagonal empirical Fisher EWC

EWC follows the principle in [Qian et al., Interspeech 2024](https://www.isca-archive.org/interspeech_2024/qian24_interspeech.pdf): discourage moving weights that matter to an earlier task.

`localvoice/fisher.py` selects 128 unique original FLEURS **training** clips with seed 42. It computes the mean squared per-utterance gradient of token-mean supervised cross-entropy at E11. This is a diagonal empirical Fisher approximation, not the exact Fisher over all possible model outputs. Augmentation/dropout are disabled while estimating importance. Validation/test clips never enter this estimate.

The saved Fisher artifact contains model/data/sample identities, every sampled path, and hashes of both E11's checkpoint and the tensor file. Loading checks hashes, the starting checkpoint identity, membership in the training split, and the sampled audio/reference fingerprint. Importance is normalized to a global unit trace. The anchor is captured before any new optimizer updates.

The EWC objective is `CE + lambda * sum(F_normalized * (theta - theta_E11)^2)`, with prespecified `lambda=10000`. This coefficient is a local hypothesis under our explicit normalization, not a coefficient copied from a paper or chosen using test scores. The first optimizer step has zero penalty; subsequent changes receive a restoring gradient weighted by importance. Logs report CE and weighted penalty separately. History training loss retains the CE meaning, allowing comparison with the control.

| Recipe | Initialization / data / optimizer | Penalty |
| --- | --- | --- |
| E21 control | Same E11, Latin American replay mixture and schedule as E22 | CE only |
| E22 | Same E11, data and schedule as E21 | CE + Fisher EWC |

Both retain the previous E17 recipe: 5,796 clips / 12.98 hours, LR 5e-6, effective batch 16, seed 42, light training-only time masking, maximum four epochs, patience two checks. Fisher preparation cost is separate from GPU training time and recorded in `runs/fisher-E11/fisher.json`. E22's reported training time includes E11 ancestry; it does not credit E21 control training. Final Tiny scoring keeps batch-one float32 greedy generation.

## Selection, provenance and evidence

- `localvoice/research_round.py` freezes the five recipe hashes before execution, runs GPU stages sequentially, and preserves first-run artifacts. It does not overwrite existing checkpoints.
- `runs/research-round.json` exposes live state and original recipe identities. The server uses it to reserve the GPU; browser transcription is disabled during these jobs.
- `runs/selection-research.json` is written only after all five final validation evaluations, with per-backbone choices and checkpoint file hashes.
- Selection uses original FLEURS validation only and includes prior better checkpoints. Existing FLEURS/MLS tests and E17's Latin holdout are already known; none is used to tune coefficients, stopping, layer counts or checkpoint selection in this round.
- This round measures whether the methods beat the primary validation record. It cannot establish Latin American retention without an appropriate separately designed development/final-evaluation protocol. Do not infer a retention gain merely because an EWC penalty was used.
- CPU tests verify frozen weights/upper gradients, Fisher-weighted restoring gradients, anchor/data integrity and tamper rejection. Recognition gains must come from actual saved-model evaluation, not these tests.

Reproduction in a fresh experiment workspace with the prior checkpoints and prepared data:

```powershell
.venv\Scripts\python.exe -m localvoice.research_round
```

The command refuses to replace an existing round. Inspect failures and preserve their evidence before any recovery. Current experiment tables and README measured sections are generated from real local artifacts.


## Separately frozen training-scale follow-up

E22's early training logs showed weighted EWC penalties around 4e-5 against
cross-entropy around 0.7–1.1. Before inspecting its validation scores, a single
stronger setting was frozen as E23: lambda 1e7, with all E21/E22 data, initialization,
learning rates, seed and stopping settings unchanged. This is a training-scale
choice, not a value copied from the paper or selected on test data. It does not
change the original five recipes or replace their first selection.

`runs/ewc-followup.json` records the decision and recipe hash before execution.
The follow-up waits for the original round, then uses the same verified 128-clip
Fisher artifact. Its validation-only choice is recorded separately in
`runs/selection-research-strong.json`. All six runs remain visible, including
negative results. The original frozen selection remains intact.
