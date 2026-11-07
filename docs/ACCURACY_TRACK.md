# Spanish accuracy track: matched Tiny and Small experiments

The original Tiny baseline is 20.7911% validation WER. Conservative Tiny tuning reached 19.4792%. These results motivated a stronger base model alongside investigation of a tokenizer-prompt defect. Neither changing a model nor correcting a bug is assumed to improve the measured score without evaluation.

## Stronger pretrained model

E7 uses official `openai/whisper-small`, pinned revision `973afd24965f72e36ca33b3055d56a652f456b4d`. The local safetensors file SHA256 was verified against the Hub's LFS metadata: `1d7734884874f1a1513ed9aa760a4f8e97aaa02fd6d93a3a85d27b2ae9ca596b`. The source manifest is `data/models/whisper-small/source.json`.

Its complete 407-clip validation baseline is **6.3407% WER, 2.1576% CER**. This is a base-model improvement over Tiny, not a fine-tuning gain. The same Spanish references, official splits, NFC/accents, and scoring normalization are retained.

## Corrected training

E9 repeats E5's Tiny recipe while explicitly setting and checking the encoded Spanish/transcription prefix. The target text SHA256, project, dataset fingerprint and hyperparameters match E5. Evidence: `runs/E9/ablation-provenance.json`. The [prompt investigation](TRAINING_PREFIX_FIX.md) records the actual before/after tokens and preserved interrupted artifacts.

E8 trains Small's decoder with its encoder frozen. Its instantiated trainable count is 153,580,800 parameters. AdamW learning rate 0.000002, effective batch 16 (4 × 4 accumulation), weight decay .05, 5% warmup, linear decay, maximum four epochs, early stopping patience two validation checks, seed 42. A full validation pass runs after 88 optimizer updates within each epoch (roughly halfway) and at epoch end; fractional epoch values identify intermediate checkpoints. Targets retain punctuation/casing without changing normalized words. Encoded labels contain the verified Spanish/transcription prefix. Validation WER selects the checkpoint.

Small baseline and tuned evaluation both use batches of four, float32 greedy decoding and a 225-token cap, preserving clip order and the incomplete final batch. Their generation time is amortized per clip and should not be interpreted as the single-request latency recorded for Tiny. Evaluation batching and metadata matching have regression tests.

## Interpreting the results

- E9 versus E0 measures corrected Tiny tuning; E9 versus E5 compares prompt alignment under matched hyperparameters and target words.
- E8 versus E7 measures Small fine-tuning under matched model, revision, dataset, split, normalization, and evaluation protocol.
- Small versus Tiny measures the combined effect of changing the backbone and any adaptation. It must not be presented as a pure tuning gain.
- All original E1–E6 measurements remain visible and are labeled as superseded prompt recipes. Regression values stay negative.

The live sequence runs E9 before restarting E8 with the corrected prompt. Status: `runs/accuracy.json`; exact recipe: `configs/small-decoder.json`. Download and verify the model with `python scripts/download_small.py`. Reproduce with `python -m localvoice.accuracy` in a checkout with prepared data and the verified model files. Completed stages are reused; unfinished runs require inspection and preservation before retrying.

Frozen Tiny and Small test selections are separate artifacts. Test data are not used for targets or checkpoint selection. Final test results are reported separately from validation. Earlier Tiny test artifacts remain preserved; a new selection never rewrites that frozen record.

## Checkpoint decoding audit

After training, a static configuration audit found that Transformers checkpoint serialization migrated legacy model-config fields and removed two task-token IDs (50358 and 50359) from Small's suppression list. The partial first baseline-test pass was stopped before any test score or prediction file was produced or consulted. Its frozen snapshot and log are preserved under `archives/decoding-audit/20261031-2253/`.

The final loader now takes decoding rules from the original pinned pretrained generation configuration for both baseline and tuned weights, and synchronizes legacy model-config fields before saving. A real model-save regression test checks that suppression rules survive serialization. Both Small models are re-evaluated on all validation clips under the same configuration digest before freezing a replacement test snapshot. No weights are changed; `runs/E8/weights-audit.json` verifies their SHA256 against the prior snapshot. `runs/generation-audit.json` records the matched decoding hashes and validation results. This correction is based on configuration inspection, not held-out outcomes.

Training wall time includes validation and checkpoint saving. Small's more frequent checks are therefore part of its reported adaptation cost. Peak memory is PyTorch allocated GPU memory, not total board usage.
