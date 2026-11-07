# Fine-tuning Spanish speech recognition with limited labeled data

## Objective

Measure how full fine-tuning, LoRA, and speech augmentation change Spanish transcription accuracy and adaptation cost. Spanish is the target language; the low-resource condition is the limited amount of labeled training speech.

## Current evidence

The Spanish experiment series uses its own dataset and run artifacts. Superseded results from the earlier language choice are archived and never compared with Spanish. Live results are appended below from actual local metrics. No improvement is assumed before a tuned checkpoint is evaluated.

## Data and checkpoint

Dataset: Google FLEURS, Latin American Spanish configuration `es_419`, licensed CC-BY-4.0. Official train, validation, and test splits are retained. Audio becomes mono 16 kHz WAV; empty or longer-than-30-second clips are excluded with reasons. Full validation checks transcript, duration, file content duplicates, format, and speaker overlap where IDs are available. Missing speaker IDs mean speaker independence cannot be verified. This limitation is retained in evaluation artifacts.

Model: multilingual `openai/whisper-tiny`, fixed repository revision `169d4a4341b33bc18d8881c4b69c2e104e1cc0af`, Apache-2.0. Keeping the family, size, and revision fixed makes the initial strategy comparison interpretable. Tiny fits the available RTX 4060 and permits a full experiment cycle; it is not presented as the strongest Spanish recognizer.

## Exact adaptation methods

E0 is the untouched pretrained baseline. E1 updates all model parameters. E2 freezes the base weights and trains rank-eight LoRA updates on query and value projections (`q_proj`, `v_proj`), alpha sixteen, dropout 0.05. E3 repeats full tuning with training-only augmentation. E4 repeats LoRA with the same augmentation. Actual parameter counts are measured from the instantiated model.

The initial E1–E4 runs have a maximum five-epoch budget, batch size eight, one gradient accumulation step, seed 42, AdamW, weight decay 0.01, gradient clipping 1.0, 10% warmup, and linear learning-rate decay. Full tuning uses learning rate 0.00001; LoRA uses 0.0001. The optimizer settings differ intentionally by strategy and are disclosed. This does not isolate parameter count from learning-rate choice.

CUDA uses bfloat16 when supported, otherwise scaled float16, with gradient checkpointing. Successful and skipped updates are counted. Non-finite loss stops training. Unaugmented features are cached by audio content and model revision; augmented features are never reused across epochs. Validation WER chooses the best checkpoint. Two consecutive epochs without improvement trigger early stopping. Training loss and validation WER/CER are recorded every epoch; live progress records intermediate loss and optimizer updates.

## Follow-up optimization

E5 tests conservative full tuning at learning rate 0.000002, batch eight with four accumulation steps (effective batch 32), weight decay 0.05, and up to six epochs. E6 tests rank-16 LoRA at learning rate 0.00002, alpha 32, dropout 0.10, batch 32, and the same decay and epoch budget. Both use 5% warmup. These recipes address the original early overfitting and unstable LoRA curves.

E5/E6 preserve punctuation and casing in training targets, using only train parquet text. Raw targets are accepted only if their normalized words match the original training transcript; otherwise capitalization and a final period are restored to the same words. Evaluation text normalization, base checkpoint, and split membership are unchanged. Multiple settings change together, so these are recipe comparisons rather than isolated causal tests. All original E0–E4 results remain visible.

Paired utterance bootstrap analysis uses 5,000 resamples and seed 42 to report word errors removed, improved/worsened clips, and an exploratory 95% WER-difference interval. Validation data guide selection, so these intervals do not replace a final held-out evaluation.

## Prompt alignment and stronger backbone

Inspection of actual fast-tokenizer output found that E1–E6 training labels omitted Spanish/task prompt tokens, although generation used them. Those runs are retained as superseded prompt recipes. Training now explicitly sets the Spanish/transcription prefix and verifies encoded token IDs; a real-tokenizer save/reload regression test covers the defect. E9 repeats E5's Tiny settings with this correction. The accuracy effect is measured rather than assumed.

E7 establishes an independent pinned Whisper Small baseline; E8 adapts its decoder with the encoder frozen. E8 uses learning rate 0.000002, effective batch 16, weight decay .05, up to four epochs and patience two. Both Small evaluations use batch four and float32 greedy generation. Their amortized per-clip generation timings are distinct from Tiny single-clip timings. E8 versus E7 isolates adaptation within Small; Small versus Tiny includes a backbone upgrade. The source model file is verified against its official SHA256.

## Augmentation and text handling

Training-only speed perturbation samples 0.95–1.05; additive Gaussian noise samples 20–35 dB SNR. Clips near thirty seconds are not slowed past the model context limit, avoiding transcript-invalidating truncation. Small pitch changes can occur; these augmentations still need interpretation on real speech. Validation/test audio is never augmented.

All references and predictions share Unicode NFC, lowercase, Unicode punctuation removal, and whitespace normalization. Spanish accents and ñ are preserved. Generation is fixed at a maximum 225 new tokens across experiments. Very long tokenizations may reach that cap, and resulting errors remain counted.

## What is compared

E1 versus E0 measures full adaptation. E2 versus E0 measures adapter adaptation. E3 versus E1 and E4 versus E2 measure augmentation under each strategy. E2 versus E1 and E4 versus E3 compare strategies at each augmentation setting. Common base model/revision, data fingerprint, language, evaluation split, and text normalization are required for dashboard comparisons.

WER and CER are computed using JiWER. Absolute WER reduction is baseline minus tuned WER in percentage points. Relative reduction divides that difference by baseline WER; it is undefined for a zero baseline. Negative reductions are regressions and remain visible. WER can exceed 100% when insertions are frequent. Substitution, deletion, insertion counts and common aligned spans are retained, along with per-clip reference/hypothesis pairs.

Cost includes training wall time, peak PyTorch GPU allocation, trainable weights, and warmed generation latency. Peak allocation is not total board memory. Baseline trainable parameters are zero because no training is performed. Nonempty dialect/condition groups receive separate scores when at least ten labeled clips exist; this threshold does not establish statistical reliability.

## Checkpoint and test policy

Checkpoints are independently loadable full models or LoRA adapters with their processor files. The experiment series evaluates only validation data. The held-out test set requires explicit `--split test --final-test` after experiment choices are frozen. Validation improvements guide development and are not final test findings. Multiple seeds and paired uncertainty estimates are needed before claiming statistical significance.

## Artifacts and progress

Each run retains `training.json`, `progress.json`, `history.json`, `checkpoint/`, `metrics-validation.json`, and `predictions-validation.json` as applicable. The website shows optimizer updates, training loss, validation curves, selected epochs, recognition errors, baseline differences, and training cost. The run matrix stores stage status and logs. Failures stop the series rather than silently skipping a strategy.

## Limitations

- FLEURS is read speech; results do not establish conversational or dialect-wide Spanish performance.
- Missing speaker IDs prevent an independent audit of speaker separation.
- One seed and one model size support an initial controlled study, not a universal ranking.
- Augmentation and LoRA can worsen accuracy; all measured outcomes must be reported.
- Training-set playground clips are diagnostic and cannot support evaluation claims.

## Sources

[FLEURS dataset and license](https://huggingface.co/datasets/google/fleurs), [Whisper Tiny](https://huggingface.co/openai/whisper-tiny), [Whisper fine-tuning guide](https://huggingface.co/blog/fine-tune-whisper), and [PEFT LoRA](https://huggingface.co/docs/peft/en/package_reference/lora).
