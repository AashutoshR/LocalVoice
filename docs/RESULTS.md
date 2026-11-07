# Spanish fine-tuning results

## Measured Spanish results

Validation findings are provisional. Held-out test evaluation remains separate. Negative reductions are regressions; missing runs are pending.

| Run | WER | CER | WER reduction vs matched baseline | Trainable weights | Training time |
| --- | --- | --- | --- | --- | --- |
| E0 · Pretrained baseline | 20.79% | 6.50% | — | 0 | 0.0 min |
| E1 · Full fine-tuning | 20.91% | 6.71% | -0.12 pp vs E0 | 37,184,640 | 8.5 min |
| E2 · LoRA fine-tuning | 21.57% | 6.90% | -0.78 pp vs E0 | 147,456 | 20.0 min |
| E3 · Full + augmentation | 20.48% | 6.55% | +0.31 pp vs E0 | 37,184,640 | 14.4 min |
| E4 · LoRA + augmentation | 23.26% | 7.62% | -2.46 pp vs E0 | 147,456 | 29.5 min |
| E5 · Conservative full tuning | 19.48% | 6.06% | +1.31 pp vs E0 | 37,184,640 | 15.2 min |
| E6 · Stable LoRA tuning | 20.88% | 6.79% | -0.09 pp vs E0 | 294,912 | 11.9 min |
| E7 · Whisper Small pretrained | 6.34% | 2.16% | — | 0 | 0.0 min |
| E8 · Whisper Small decoder tuning | 5.67% | 1.83% | +0.67 pp vs E7 | 153,580,800 | 29.0 min |
| E9 · Prompt-aligned Tiny tuning | 19.25% | 5.87% | +1.54 pp vs E0 | 37,184,640 | 17.9 min |
| E10 · Small encoder + decoder adaptation | 5.61% | 1.83% | +0.74 pp vs E7 | 240,582,912 | 59.9 min |
| E11 · Tiny stronger acoustic adaptation | 18.40% | 5.80% | +2.40 pp vs E0 | 37,184,640 | 27.0 min |
| E12 · Tiny teacher-regularized fine-tuning | 21.49% | 6.53% | -0.70 pp vs E0 | 37,184,640 | 28.7 min |
| E13 · Tiny diverse-data fine-tuning | 18.91% | 5.86% | +1.88 pp vs E0 | 37,184,640 | 32.7 min |
| E14 · Tiny final domain refinement | 18.96% | 5.84% | +1.83 pp vs E0 | 37,184,640 | 40.8 min |
| E15 · Small higher-rate decoder refinement | 5.83% | 1.95% | +0.51 pp vs E7 | 153,580,800 | 39.7 min |
| E16 · Small regularized decoder LoRA | 5.84% | 1.92% | +0.50 pp vs E7 | 589,824 | 25.9 min |
| E17 · Tiny Latin American replay tuning | 18.64% | 5.80% | +2.15 pp vs E0 | 37,184,640 | 32.1 min |
| E18 · Small matched full-tuning control | 5.57% | 1.82% | +0.78 pp vs E7 | 240,582,912 | 60.2 min |
| E19 · Small lower-six encoder blocks frozen | 5.58% | 1.82% | +0.77 pp vs E7 | 196,104,960 | 66.6 min |
| E20 · Small lower-nine encoder blocks frozen | 5.63% | 1.80% | +0.72 pp vs E7 | 174,843,648 | 53.5 min |
| E21 · Tiny matched replay control | 18.68% | 5.81% | +2.11 pp vs E0 | 37,184,640 | 33.4 min |
| E22 · Tiny Fisher-protected replay | 18.59% | 5.78% | +2.20 pp vs E0 | 37,184,640 | 34.4 min |
| E23 · Tiny stronger Fisher-protected replay | 18.83% | 5.90% | +1.96 pp vs E0 | 37,184,640 | 36.6 min |

Base model: `openai/whisper-tiny`. Language: Spanish. Baseline evaluation: 407 clips, `validation` split. Each comparison also requires the same dataset fingerprint and normalization.

Lowest measured Tiny tuned WER: **E11 · 18.40%**. Versus E0: **+2.40 percentage points** WER reduction (**+11.52% relative**), and **+0.70 points** CER reduction.

E5/E6 are follow-up recipe experiments, not replacements for E1–E4. They use lower learning rates, effective batch 32, restored training punctuation/casing, and weight decay 0.05. See `docs/FINE_TUNING_IMPROVEMENTS.md` for exact settings. Several settings changed together; gains cannot be attributed to one change alone.

E1–E6 preserve measurements from a superseded tokenizer-prompt setup. The fast tokenizer omitted Spanish/task tokens from training labels; E9 explicitly aligns and verifies them. See `docs/TRAINING_PREFIX_FIX.md`. The original pretrained generation baselines are unaffected.

### Whisper Small accuracy track

E7 is the original Whisper Small checkpoint; E8 tunes its decoder while freezing its audio encoder. E10 also adapts the encoder. E8 versus E7 measures fine-tuning. Small versus Tiny also changes the base model and is not a pure tuning gain. Small runs use batch-four float32 greedy evaluation, with amortized generation time per clip. Tiny timings use single-clip generation.

**E8 fine-tuning gain versus E7: +0.67 pp WER (+10.50% relative)**. CER reduction: +0.33 pp.

**E10 fine-tuning gain versus E7: +0.74 pp WER (+11.60% relative)**. CER reduction: +0.33 pp.

**E15 fine-tuning gain versus E7: +0.51 pp WER (+7.99% relative)**. CER reduction: +0.21 pp.

**E16 fine-tuning gain versus E7: +0.50 pp WER (+7.84% relative)**. CER reduction: +0.24 pp.

**E18 fine-tuning gain versus E7: +0.78 pp WER (+12.23% relative)**. CER reduction: +0.34 pp.

**E19 fine-tuning gain versus E7: +0.77 pp WER (+12.07% relative)**. CER reduction: +0.34 pp.

**E20 fine-tuning gain versus E7: +0.72 pp WER (+11.29% relative)**. CER reduction: +0.36 pp.

### Original FLEURS test after the earlier frozen selection

These checkpoints were chosen using validation scores before the original test evaluation. That test has already been reported and is not fresh evidence for the later E10/E11 development round.

| Run | Test WER | Test CER | Test clips |
| --- | --- | --- | --- |
| E0 · Pretrained baseline | 19.11% | 6.10% | 907 |
| E5 · Conservative full tuning | 18.16% | 5.96% | 907 |
| E7 · Whisper Small pretrained | 6.34% | 2.16% | 907 |
| E8 · Whisper Small decoder tuning | 5.62% | 1.80% | 907 |
| E9 · Prompt-aligned Tiny tuning | 17.93% | 5.51% | 907 |
| E10 · Small encoder + decoder adaptation | 5.65% | 1.81% | 907 |

E5 held-out WER reduction versus E0: **+0.95 pp (+4.97% relative)**.

E8 held-out WER reduction versus E7: **+0.73 pp (+11.46% relative)**.

E9 held-out WER reduction versus E0: **+1.18 pp (+6.17% relative)**.

E10 held-out WER reduction versus E7: **+0.70 pp (+10.98% relative)**.

### Spanish MLS: historical test and reused diagnostic

Fixed 300-clip sample from 20 speakers; 1.276 hours. Selection is frozen in `runs/selection-acoustic.json` using FLEURS validation only. All models use the same batch-four float32 greedy decoding. MLS is a separate audiobook domain. These scores belong to the frozen E10/E11 round; later recipes are exploratory and do not inherit this holdout's independence. Pretraining overlap is unknown.

| Run | MLS WER | MLS CER | Clips |
| --- | --- | --- | --- |
| E0 · Pretrained baseline | 22.13% | 7.12% | 300 |
| E7 · Whisper Small pretrained | 8.16% | 3.18% | 300 |
| E8 · Whisper Small decoder tuning | 9.49% | 3.40% | 300 |
| E9 · Prompt-aligned Tiny tuning | 23.31% | 7.44% | 300 |
| E10 · Small encoder + decoder adaptation | 9.63% | 3.42% | 300 |
| E11 · Tiny stronger acoustic adaptation | 25.68% | 8.38% | 300 |
| E16 · Small regularized decoder LoRA | 7.89% | 2.55% | 300 |

E8 MLS WER reduction versus E7: **-1.33 pp (-16.24% relative)**.

E9 MLS WER reduction versus E0: **-1.18 pp (-5.31% relative)**.

E10 MLS WER reduction versus E7: **-1.47 pp (-17.96% relative)**.

E11 MLS WER reduction versus E0: **-3.55 pp (-16.02% relative)**.

E16 MLS WER reduction versus E7: **+0.27 pp (+3.33% relative)**.

### New-clip MLS dev follow-up (exploratory)

A fixed seed-43 sample of 300 previously unused dev clips. The earlier MLS test was already read before this data-focused round, so this is an exploratory follow-up, not a fully blind study. The listed checkpoints were frozen before these scores; later rounds are reported separately. All Tiny checkpoints use the same batch-four float32 greedy decoding.

| Run | MLS dev WER | MLS dev CER | Clips |
| --- | --- | --- | --- |
| E0 · Pretrained baseline | 23.93% | 7.54% | 300 |
| E11 · Tiny stronger acoustic adaptation | 27.32% | 9.24% | 300 |
| E13 · Tiny diverse-data fine-tuning | 20.27% | 6.47% | 300 |
| E14 · Tiny final domain refinement | 20.36% | 6.50% | 300 |

E11 MLS dev WER reduction versus E0: **-3.39 pp (-14.15% relative)**.


E13 MLS dev WER reduction versus E0: **+3.66 pp (+15.29% relative)**.


E14 MLS dev WER reduction versus E0: **+3.57 pp (+14.94% relative)**.


### Latin American text-disjoint holdout

300 locally untrained recordings reserved before E17 training; no exact transcript overlap with FLEURS or added training. Speaker IDs are unavailable; pretraining overlap is unknown.

| Tiny checkpoint | WER | CER | Clips |
| --- | --- | --- | --- |
| E0 · Pretrained baseline | 24.42% | 9.13% | 300 |
| E11 · Tiny stronger acoustic adaptation | 24.97% | 9.36% | 300 |
| E17 · Tiny Latin American replay tuning | 19.80% | 7.11% | 300 |

Recipes: `docs/ACOUSTIC_ADAPTATION.md`, `docs/TEACHER_REGULARIZED_TUNING.md`, `docs/DIVERSE_DATA_TUNING.md`. Training time includes the parent stage for warm-started runs.

Exact errors, memory, latency, hyperparameters, checkpoint selection, and epoch history are available in the website and `runs/E*/` artifacts.

Generated from local artifacts at 2026-11-02T05:06:53.003163+00:00.
