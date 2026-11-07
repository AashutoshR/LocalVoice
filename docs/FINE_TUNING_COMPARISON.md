# Fine-tuning the existing Spanish models

Updated 1 November 2026. This round retains the existing Tiny and Small architectures. Run IDs identify training recipes/checkpoints, not additional backbones.

## Latest completed fine-tuning round: E16 and E17

These are new training recipes on the two existing backbones. **Neither new recipe beats the retained FLEURS validation record.** Small LoRA reduces the audiobook regression and training memory; the separate Tiny replay result is below.

| Existing Small checkpoint | FLEURS validation WER | Reused MLS WER | Reused MLS CER | Training peak allocated GPU memory |
| --- | --- | --- | --- | --- |
| E7 · Whisper Small pretrained | 6.34% | 8.16% | 3.18% | — |
| E10 · Small encoder + decoder adaptation | 5.61% | 9.63% | 3.42% | 4746 MB |
| E16 · Small regularized decoder LoRA | 5.84% | 7.89% | 2.55% | 1570 MB |

E16 removes **198 word errors** versus full-tuned E10 across the same 300 MLS recordings: 9.63% → 7.89% WER (**18.0% relative reduction**). CER improves 3.42% → 2.55%. 62 clips improve and 36 worsen. Exploratory paired speaker-cluster bootstrap WER-reduction interval: 0.21 to 4.21 pp (20 clusters, 5,000 resamples).

The gain is uneven: one avoided repetitive hallucination accounts for 157 of the 198 fewer errors. Against pretrained Small, E16 removes only 31 errors (8.16% → 7.89% WER); its interval crosses zero. This supports reduced forgetting relative to E10 on these known clips, not a robust general improvement over pretrained Small.

FLEURS validation worsens 5.61% → 5.84% (24 additional errors), so E10 remains selected for that domain. The MLS corpus was already examined in earlier rounds; this is a reused diagnostic, not fresh blind evidence.

The recipe freezes all pretrained weights and trains **589,824 decoder LoRA parameters** (rank 8, dropout 0.1, adapter-only LR 1e-4). Peak allocated GPU memory falls 4746 → 1570 MB (66.9% lower for these measured training recipes). The merged model retains **241,734,912 inference parameters**. All 48 saved adapter B tensors have nonzero updates; CPU gradient/merge checks establish that fine-tuning actually changes adapters while base weights stay frozen.

### Tiny: Latin American speech with FLEURS replay

E17 starts from E11 and fine-tunes the same Tiny weights at LR 5e-6 on 12.98 hours: original FLEURS training plus 3,000 human Argentinian Spanish recordings (4.17 hours). Light time masking and early stopping constrain overfitting. The best checkpoint is at update 182; training stops at 545 updates after validation worsens.

Reloaded FLEURS validation WER: **18.64%**, versus E11 **18.40%**. E11 remains the FLEURS choice. A 300-clip, text-disjoint holdout was reserved before training; all three Tiny checkpoints were frozen before its scores were read.

| Same Tiny backbone | Latin American holdout WER | CER | Word errors |
| --- | --- | --- | --- |
| E0 · Pretrained baseline | 24.42% | 9.13% | 714 |
| E11 · Tiny stronger acoustic adaptation | 24.97% | 9.36% | 730 |
| E17 · Tiny Latin American replay tuning | 19.80% | 7.11% | 579 |

Compared with E11, E17 removes +151 word errors: 105 clips improve and 23 worsen. Exploratory utterance-bootstrap WER-reduction interval: 3.66 to 6.71 pp. Speaker dependence cannot be accounted for because source speaker IDs are missing.


Relative WER change for E17: +18.9% reduction versus pretrained Tiny; +20.7% versus prior tuned E11. Negative values mean regression. All holdout scores use identical batch-four float32 greedy decoding. Speaker IDs are unavailable, so text disjointness does not establish speaker independence. Whisper pretraining overlap is unknown. No further E17 tuning uses these scores.

Source: [OpenSLR 61](https://www.openslr.org/61/), Google Latin American Spanish corpus, **CC-BY-SA-4.0**. Keep this attribution/license with derived data and review its terms before redistributing derived artifacts. Methods: `docs/REGULARIZED_LORA_ROUND.md`, `docs/LATIN_REPLAY_ROUND.md`. Selection hashes, data audit, real predictions and weight audits are preserved under `runs/`.

### Earlier rounds (historical)

**Data-focused Tiny E13 improves the new audiobook sample from 23.93% to 20.27% WER (15.3% relative reduction), with the same Tiny architecture.** Its FLEURS validation WER is 18.91%, versus pretrained 20.79% and previous best E11 18.40%. This is a domain tradeoff, not a claim that every metric or clip improves.

**Best Tiny FLEURS validation result: E11 · 18.40% WER, 5.80% CER.** The matching pretrained Tiny baseline is 20.79% WER and 6.50% CER: 2.40 percentage points, or 11.5% relative WER reduction.

## Same Tiny model, before and after

All rows use the same original 407 FLEURS validation clips, normalization, pinned Tiny revision, float32 single-clip greedy decoding and token limit. Training data can differ; evaluation data does not.

| Recipe | WER ↓ | CER ↓ | Word errors | Cumulative training time |
| --- | --- | --- | --- | --- |
| E0 · Pretrained baseline | 20.79% | 6.50% | 2,092 | 0.0 min |
| E9 · Prompt-aligned Tiny tuning | 19.25% | 5.87% | 1,937 | 17.9 min |
| E11 · Tiny stronger acoustic adaptation | 18.40% | 5.80% | 1,851 | 27.0 min |
| E12 · Tiny teacher-regularized fine-tuning | 21.49% | 6.53% | 2,162 | 28.7 min |
| E13 · Tiny diverse-data fine-tuning | 18.91% | 5.86% | 1,903 | 32.7 min |
| E14 · Tiny final domain refinement | 18.96% | 5.84% | 1,908 | 40.8 min |
| E17 · Tiny Latin American replay tuning | 18.64% | 5.80% | 1,876 | 32.1 min |

Compared with the previous best E11 (18.40% WER), the selected checkpoint removes 0.00 pp WER. The newer recipes did not beat E11 on this split.

## Which errors changed

| Error type | Pretrained Tiny | Selected Tiny | Fewer errors |
| --- | --- | --- | --- |
| Substitutions | 1,547 | 1,383 | +164 |
| Deletions | 186 | 181 | +5 |
| Insertions | 359 | 287 | +72 |

Total word errors: 2,092 → 1,851, **241 fewer errors across 10,062 reference words**. CER changes by +0.70 percentage points.

195 validation clips improve and 115 worsen. Paired utterance-bootstrap WER-reduction interval: 1.57 to 3.22 pp. This interval is exploratory after validation selection; FLEURS speaker IDs are unavailable.

## What changed in training

- E11 increases Tiny's learning rate from 2e-6 to 1e-5, reduces effective batch 32 to 16, and adds light time masking. Validation exposes overfitting after epoch 2.
- E12 tests a frozen pretrained Small teacher penalty on training clips. It worsens validation WER and is retained as a negative result, not promoted.
- E13 expands unique training speech from 8.81 to 21.28 hours: 2,796 FLEURS clips plus 3,000 official Spanish MLS train clips from 21 speakers. Validation/test clips remain excluded.
- E14 starts from E13 and briefly refines on FLEURS training at 2e-6, with augmentation disabled. Prior checkpoints remain available if refinement regresses.
- Checkpoints are selected by full validation WER; saved weights are reloaded for final scoring. Multiple recipe settings change together, so one-factor causal attribution is not established.

The selected Tiny model still has **37,760,640 total parameters** and 37,184,640 trainable during fine-tuning. The teacher is not part of the deployed Tiny checkpoint. Training time includes parent stages and validation checks, but not dataset download/preparation. Measured latency is a local single-run benchmark, not evidence of a reliable speed improvement.

## New audiobook clips: exploratory follow-up

Fixed seed-43 sample of 300 previously unused MLS dev clips from 20 speakers; these speakers do not occur in the added training sample. All four Tiny checkpoints use the same batch-four float32 greedy protocol. The earlier MLS test was already read before choosing this data-focused recipe, so this is an exploratory follow-up, not a fully blind study. Those checkpoints were frozen before these scores; later rounds are reported separately.

| Tiny recipe | MLS dev WER ↓ | MLS dev CER ↓ | Relative WER reduction vs pretrained |
| --- | --- | --- | --- |
| E0 · Pretrained baseline | 23.93% | 7.54% | +0.0% |
| E11 · Tiny stronger acoustic adaptation | 27.32% | 9.24% | -14.2% |
| E13 · Tiny diverse-data fine-tuning | 20.27% | 6.47% | +15.3% |
| E14 · Tiny final domain refinement | 20.36% | 6.50% | +14.9% |

E13 removes **390 word errors versus pretrained Tiny** across 10,660 reference words: 254 fewer substitutions, 20 fewer deletions, and 116 fewer insertions. Compared with E11, it removes 751 errors (25.8% relative WER reduction).

186 clips improve and 80 worsen versus pretrained. The paired speaker-cluster bootstrap interval for WER reduction is 2.48 to 4.84 percentage points (20 speaker clusters; 5,000 resamples). This describes uncertainty on this exploratory sample.

FLEURS validation and MLS dev are different corpora and must not be combined into one score. A domain-specific gain does not establish improvement for every Spanish speaker, recording condition, or utterance. The original MLS test regressions remain in `docs/RESULTS.md`; its artifacts are unchanged. Whisper pretraining overlap with these public corpora is unknown.

## Fine-tuning the existing Small decoder

The acoustic continuation only moved validation WER from 5.67% to 5.61%, removing 7 additional errors. That step is marginal.

E15 keeps E8's existing Small decoder and frozen encoder, raises learning rate from 2e-6 to 1e-5, and selects by validation with early stopping. It retains the same training clips, target text, effective batch 16 and model architecture.

| Small recipe | Validation WER | Validation CER |
| --- | --- | --- |
| E7 · Whisper Small pretrained | 6.34% | 2.16% |
| E8 · Whisper Small decoder tuning | 5.67% | 1.83% |
| E10 · Small encoder + decoder adaptation | 5.61% | 1.83% |
| E15 · Small higher-rate decoder refinement | 5.83% | 1.95% |
| E16 · Small regularized decoder LoRA | 5.84% | 1.92% |

Selected Small checkpoint: **E10**, 5.61% WER; 11.6% relative WER reduction versus pretrained Small. This comparison does not change backbone size.

The higher-rate Small decoder recipe regressed and is not selected.

Reused 907-clip FLEURS test diagnostic: 6.34% → 5.65% WER (11.0% relative reduction); 2.16% → 1.81% CER. The project had already examined this corpus in earlier rounds. The checkpoint choice was frozen using validation before this diagnostic; it is not a fresh blind study.

The original E8 decoder test WER was 5.62%, versus 5.65% for E10. The later Small trials did not establish a meaningful improvement over E8.

## Reproducible evidence

- `runs/E*/training.json`, `history.json`, `metrics-validation.json`, `predictions-validation.json`: training, selection and exact recognition outputs.
- `runs/E*/weight-audit.json`: actual saved encoder/decoder changes against each initial checkpoint.
- `runs/selection-diverse.json`: hashes and validation choices frozen before follow-up evaluation.
- `runs/E*/metrics-mls-dev.json`, `predictions-mls-dev.json`, `paired-mls-dev.json`: complete follow-up evidence and speaker-cluster bootstrap analysis.
- `docs/DIVERSE_DATA_TUNING.md` and `docs/TEACHER_REGULARIZED_TUNING.md`: methods, data provenance, limitations and failed recipe.
