# Spanish fine-tuning: verified improvement

Historical record from 31 October 2026. See [the later same-model fine-tuning comparison](FINE_TUNING_COMPARISON.md) for subsequent recipes, new audiobook checks, and regressions.

Measured on 31 October 2026 using Google FLEURS Latin American Spanish (`es_419`).

**The selected Small model achieves 5.62% WER and 1.80% CER on all 907 held-out test clips.** Against its matching pretrained Small baseline, fine-tuning reduces WER by 11.5% relative and CER by 16.6% relative.

## Matched before/after results

| Family / split | Pretrained WER | Tuned WER | Relative WER reduction | Pretrained CER | Tuned CER |
| --- | --- | --- | --- | --- | --- |
| Tiny · validation | 20.79% | 19.25% | 7.4% | 6.50% | 5.87% |
| Tiny · test | 19.11% | 17.93% | 6.2% | 6.10% | 5.51% |
| Small · validation | 6.34% | 5.67% | 10.5% | 2.16% | 1.83% |
| Small · test | 6.34% | 5.62% | 11.5% | 2.16% | 1.80% |

Each tuning gain uses the same model family, revision, clips, split, scoring normalization and decoding protocol. Validation uses 407 clips; test uses 907. The original Tiny test baseline is 19.11% WER, while the stronger Small pretrained baseline is 6.34%. Changing backbone explains most of the overall system gain; the 6.34% → 5.62% comparison isolates Small adaptation.

## What changed

- Corrected the encoded Spanish/transcription training prefix and verified it with a real-tokenizer save/reload test. E9 repeats E5’s hyperparameters and target words with that correction; validation WER improves from 19.48% to 19.25%, and CER from 6.06% to 5.87%.
- Added a stronger, independently measured Small baseline. E8 freezes its audio encoder and adapts the decoder with learning rate 0.000002, effective batch 16, AdamW weight decay .05, seed 42 and a four-epoch maximum.
- Added full-validation checks roughly halfway through each epoch and at epoch end. The selected Small checkpoint is epoch 4, optimizer update 700; later/poorer checkpoints never replace a lower-WER checkpoint.
- Restored pinned pretrained decoding rules after detecting a checkpoint-serialization mismatch in two special-token settings. The audit changed no weights and reproduced both validation scores exactly. Baseline and tuned configurations now have the same verified generation digest.

## Which errors improved on test

| Error type | Small pretrained | Small tuned | Fewer errors |
| --- | --- | --- | --- |
| Substitutions | 1,038 | 978 | 60 |
| Deletions | 189 | 172 | 17 |
| Insertions | 248 | 156 | 92 |

Total word errors fall from 1,475 to 1,306: **169 fewer errors across 23,253 reference words**. Insertions fall from 248 to 156. 134 clips improve and 108 worsen; the aggregate gain does not mean every clip improves.

## Selection, uncertainty and cost

The checkpoint was frozen using validation results before final test scoring. A paired utterance bootstrap (5,000 resamples, seed 42) gives a 95% interval of **0.09 to 1.87 percentage points** for the Small test WER reduction (point estimate 0.73 pp). This is one seed on read speech; missing speaker IDs prevent auditing speaker independence. Broader conversational/dialect performance has not been established.

Small adaptation took **29.0 minutes**, including validation and checkpoint saving, with **3298 MB** peak PyTorch GPU allocation and **153,580,800 trainable parameters**. Its encoder stays frozen. Small matrix generation timings are amortized over batches of four; Tiny timings are single-clip measurements.

## Reproduction and evidence

- Recipe and model revision: `configs/small-decoder.json`, `configs/whisper-small.json`.
- Download and checksum verification: `python scripts/download_small.py`.
- Training series: `python -m localvoice.accuracy` (fresh run directories; existing completed artifacts are preserved).
- Frozen selections: `runs/selection-small.json`, `runs/selection-aligned-tiny.json`.
- Metrics and per-clip predictions: `runs/E7/`, `runs/E8/`, `runs/E0/`, `runs/E9/`.
- Generation and weight audits: `runs/generation-audit.json`, `runs/E8/weights-audit.json`.
- Detailed methods: [accuracy track](ACCURACY_TRACK.md), [prompt correction](TRAINING_PREFIX_FIX.md).

Historical E1–E6 scores remain visible as superseded prompt recipes. Their regressions are preserved. The interrupted Small run, original decoding settings and aborted pre-audit test snapshot are archived with their reasons. No held-out outcome informed either correction.

Software verification: 21 tests passed, plus Python compilation and JavaScript syntax checks. The website shows validation and test results separately and recommends the lowest validation-WER available model.


## Live website verification

The live browser selected E8 by default and compared it against its matching E7 pretrained baseline. A training-split Spanish audio sample produced real CUDA transcripts and diagnostic WER/CER for both models. This is a functionality check, separate from the 907-clip test result above. Evidence: `runs/playground-smoke.json`, `docs/playground-smoke.png`, and [the benchmark screenshot](accuracy-results-preview.png). The page had no document-wide horizontal overflow at its current mobile viewport.
