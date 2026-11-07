# Spanish fine-tuning follow-up

This records the E5/E6 recipes before the encoded-prompt defect was identified. They remain historical comparisons. Current work is described in [the accuracy track](ACCURACY_TRACK.md) and [the prompt correction](TRAINING_PREFIX_FIX.md).

The original E0–E4 artifacts remain intact. E5 and E6 are follow-up experiments selected using validation data only. No test data is used for target construction or checkpoint selection.

## Changes being tested

| Setting | E1 / E2 original | E5 conservative full | E6 stable LoRA |
| --- | --- | --- | --- |
| Learning rate | 1e-5 / 1e-4 | 2e-6 | 2e-5 |
| Effective batch | 8 | 32 (8 × 4 accumulation) | 32 |
| Training text | Lowercase, punctuation removed | Punctuation/casing restored; same normalized words | Same as E5 |
| Weight decay | .01 | .05 | .05 |
| Maximum epochs | 5 | 6 | 6 |
| LoRA rank / alpha / dropout | 8 / 16 / .05 | N/A | 16 / 32 / .10 |
| Warmup fraction | .10 | .05 | .05 |

E5 runs first. E6 runs if E5 does not reach the exploratory 19% validation WER target. The target is an experiment decision rule, not a promised score. All candidates keep the same Whisper Tiny revision, official split membership, scoring normalization and greedy generation settings as E0. There is no change to evaluation references.

Punctuation restoration reads only the existing train parquet transcription/raw_transcription columns. Original raw text is used only when its normalized words exactly match the original training transcript; otherwise the same transcript receives initial capitalization and a final period. This avoids changing number words or reference conventions. Missing raw text falls back to that same safe formatting. The manifest and dataset fingerprint are unchanged.

Hugging Face's [Whisper fine-tuning guidance](https://github.com/huggingface/community-events/blob/main/whisper-fine-tuning-event/README.md) recommends preserving casing/punctuation for training and normalizing at evaluation. The lower learning rate and larger batch are hypotheses motivated by the local E1/E3 curves: training loss decreased while validation WER worsened after epoch one.

Checkpoint selection remains lowest full-validation WER, with patience two. Each experiment retains history, optimizer steps, precision, configuration and selected checkpoint. Separate evaluation reloads the saved checkpoint before publishing results. A paired utterance bootstrap (5,000 resamples, seed 42) describes the WER difference and improved/worsened clips; validation intervals are exploratory because these data guided selection.

Run artifacts: `runs/E5`, `runs/E6`, `runs/improvement.json`. The original series remains in `runs/matrix.json`. Reproduction: `python -m localvoice.cli train E5 --config configs/conservative.json` and `python -m localvoice.cli train E6 --config configs/stable-lora.json`, each only in a fresh run directory. Evaluation: `python -m localvoice.cli evaluate E5`. Existing runs are never overwritten.
