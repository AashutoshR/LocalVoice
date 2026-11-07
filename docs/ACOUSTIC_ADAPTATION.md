# Further Spanish acoustic adaptation

The earlier gains were modest: Tiny E9 reduced validation WER from 20.79% to
19.25%; Small E8 reduced it from 6.34% to 5.67%. Switching from Tiny to Small
accounts for most of the overall accuracy difference and is not a fine-tuning
gain. This round targets the remaining adaptation problem directly.

## Prespecified recipes

Both experiments retain the same 2,796 Spanish FLEURS training clips (8.81 hours)
and the same 407 validation clips. They preserve the Spanish transcription token
prefix and pinned pretrained decoding controls. No evaluation labels are added
to the training targets. Augmentation is randomized in training only.

| Setting | E10: Small acoustic adaptation | E11: Tiny stronger adaptation |
| --- | --- | --- |
| Initial checkpoint | E8, decoder-tuned Small | E9, prompt-aligned Tiny |
| Encoder | Trainable | Trainable |
| Decoder | Trainable | Trainable |
| Encoder learning rate | 2e-6 | 1e-5 |
| Decoder learning rate | 5e-7 | 1e-5 |
| Effective batch | 16 (4 × 4 accumulation) | 16 (8 × 2 accumulation) |
| Maximum additional epochs | 4 | 8 |
| Time mask probability / length | 0.03 / 10 frames | 0.02 / 10 frames |
| Feature mask probability / width | 0.015 / 4 | Disabled |
| Warmup / scheduler | 5% / linear decay | 5% / linear decay |
| Weight decay | 0.05 | 0.05 |
| Validation checks | Every 88 updates and epoch end | Same |
| Early stopping | 2 checks without improvement | 3 checks without improvement |

E10 uses a smaller decoder learning rate to preserve useful E8 language
adaptation while allowing its previously frozen audio encoder to change. E11
tests whether the compact model's earlier 2e-6 rate and effective batch 32 were
too conservative: it increases the rate fivefold, halves the effective batch,
and adds light time masking. These are hypotheses, not guaranteed improvements.
Multiple settings change together, so this round cannot attribute any gain to
one setting alone.

The [Hugging Face Whisper training guide](https://huggingface.co/blog/fine-tune-whisper)
provides the end-to-end adaptation reference. Its example learning rate is not
evidence that a particular Spanish run will improve; validation decides that.

E11's intermediate checkpoint checks use batches of four to reduce validation
overhead. Its final reloaded-model validation evaluation uses single-clip
float32 greedy generation, matching E0/E9's published Tiny comparison protocol.
All checks cover the full 407-clip validation set. The independent MLS comparison
uses batch four for every model, including the Tiny controls.

## Evidence and selection

Each run saves optimizer-update counts, training losses, per-check validation
WER/CER, the best saved checkpoint, the initial checkpoint SHA-256, and total
training time including its parent stage. `weight-audit.json` compares saved
encoder and decoder tensors against their actual initial checkpoint. Changed
weights establish that training happened; they do not establish better speech
recognition. Only measured errors establish that.

Choose the lowest validation WER within each backbone, including the prior
candidate as a fallback. Preserve regressions. The old 907-clip FLEURS test was
already reported before this round and must not be described as a fresh blind
test for these new choices.

## Fresh independent check

Before selecting this round's checkpoints, a uniform seed-42 sample of 300
Spanish MLS test clips was frozen from 2,385 eligible clips. It covers 20 speakers
and 1.276 hours. Only empty references and durations outside (0, 30] seconds
were excluded; in this source all 2,385 clips were eligible. The selected IDs,
audio/reference fingerprint, source hash, and freeze time are saved in
`data/independent-mls/sample.json`. The sample must not be used for training,
checkpoint selection, or subsequent hyperparameter tuning.

Source: [Multilingual LibriSpeech / OpenSLR 94](https://www.openslr.org/94/),
CC BY 4.0. Native Parquet release:
`facebook/multilingual_librispeech`, pinned revision
`2e83e61823b4c47dcbcb1980bb88601274127609`.
These are read audiobooks, so a cross-domain result may differ from FLEURS.
Overlap with Whisper's original pretraining is unknown; independence refers to
this project's local development and fine-tuning.

Reproduce sample preparation on a fresh output directory with
`python -m localvoice.independent prepare`. Evaluation requires a frozen
`runs/selection-acoustic.json` and refuses to replace existing independent
metrics. Each model uses the same float32, batch-four, greedy decoding protocol.
Independent metrics use `metrics-mls-test.json` and never overwrite FLEURS
validation or test results.
