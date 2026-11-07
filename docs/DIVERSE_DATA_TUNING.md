# Improving the existing Tiny fine-tuning with more Spanish training data

This round keeps the same `openai/whisper-tiny` architecture and pinned source
revision. E13 is a training recipe/checkpoint identifier, not a new backbone.
It starts from E9 and adds 3,000 official Spanish MLS **training** clips to the
2,796 FLEURS training clips. It changes the training data available to the
existing encoder and decoder; it does not improve scores by selecting a larger
pretrained model.

The MLS sample selects 1,000 eligible clips uniformly with seed 42 from each
of three prespecified training shards (indices 0, 15, 29 of 30). It excludes
empty references, durations outside (0, 30] seconds, and exact normalized
matches to FLEURS validation/test references. Reserved MLS test speakers must
not overlap training speakers. Source revisions, official LFS SHA-256 checks,
selected IDs, counts, hours, and speaker counts are recorded in
`data/additional-spanish/source.json`. This is a reproducible subset, not a
claim to use all Spanish MLS training data.

The recipe retains E11's learning rate 1e-5, effective batch 16, light time
masking, seed 42, weight decay 0.05, warmup 5%, and linear decay. Maximum six
epochs, validation near each half epoch and epoch end, early stopping after
three checks without improvement. No teacher loss is used. See
`configs/tiny-diverse.json`. Because data, training duration and scheduling
change together, the result is a recipe comparison, not an isolated causal
estimate of one setting.

All published FLEURS comparisons still use the exact original 407 validation
clips and single-clip float32 greedy decoding for the reloaded Tiny model.
The run's `dataset_fingerprint` identifies the unchanged base FLEURS corpus;
`training_dataset_fingerprint` separately identifies the actual mixed training
rows and audio. `training_data` records the additional manifest and total
training hours. Initialization from E9 and cumulative training cost are explicit.

After mixed-domain adaptation, E14 tests a brief final refinement on the original
8.81-hour FLEURS training split. It initializes from E13's saved best checkpoint,
reduces both learning rates to 2e-6, disables training augmentation explicitly
(including inherited checkpoint settings), and allows at most three epochs.
Validation checks occur every 44 updates and at epoch end; patience is three
checks. This is a two-stage curriculum on the same Tiny architecture. All prior
checkpoints remain candidates, so refinement cannot silently replace a better
earlier result. `configs/tiny-refinement.json` records the complete final recipe.

## Follow-up on new clips

The earlier MLS test scores were already read before choosing this data-focused
approach. A different seed-43 sample of 300 previously unused **dev** clips is
therefore an exploratory follow-up, not a claim of a fully blind study. IDs and
audio/reference fingerprint are fixed before E13 selection in
`data/spanish-mls-dev/sample.json`. No dev clips or their speakers may occur in
the additional training sample. This follow-up compares pretrained Tiny E0,
previous tuned Tiny E11, data-focused Tiny E13, and final refinement E14, using the same batch-four
float32 greedy generation for all three. It preserves all outcomes and forbids
further tuning based on these scores. Checkpoint hashes and validation choices
are frozen in `runs/selection-diverse.json` before evaluation. Original FLEURS
and MLS test artifacts remain unchanged.

Report WER/CER for each corpus separately, word errors removed, paired clips
improved/worsened, speaker-cluster bootstrap intervals for the audiobook sample,
and cumulative training cost. A validation-only gain does not establish
general Spanish robustness. The deployed Tiny architecture and inference
parameter count remain unchanged.

Source: [Multilingual LibriSpeech](https://www.openslr.org/94/), CC BY 4.0,
`facebook/multilingual_librispeech` revision
`2e83e61823b4c47dcbcb1980bb88601274127609`. Whisper pretraining overlap is unknown.
