# Regularized fine-tuning on the existing Small backbone

This round tests decoder-only LoRA on the existing pinned Whisper Small model.
It changes the fine-tuning method, not the pretrained architecture. Earlier
Tiny LoRA runs used superseded Spanish label prompts and cannot establish how
this corrected Small recipe performs.

The reason for trying constrained updates is observed overfitting: stronger
full-decoder tuning reduced training loss while validation WER worsened.
LoRA freezes the original encoder, decoder and word embeddings and learns
low-rank residuals in the decoder query/value attention projections only.
Whether that preserves useful pretrained behavior must be measured, not assumed.

Prespecified recipe `configs/small-regularized-lora.json`:

- Original pretrained Small initialization; original 2,796 FLEURS train clips.
- Verified Spanish/transcription/no-timestamps label prefix; punctuation-aware targets.
- Rank 8, alpha 16, adapter dropout 0.1; 589,824 trainable parameters.
- Adapter learning rate 1e-4, effective batch 16 (8 × 2 accumulation), weight decay 0.01.
- 10% warmup and linear decay; seed 42; at most six epochs.
- Full 407-clip validation every 88 updates and epoch end; patience two checks.
- No waveform or feature augmentation in this recipe.

The rate applies to newly initialized adapter weights, not the frozen pretrained
weights. After loading and merging, the inference model retains Small's original
architecture and parameter count. Unit checks verify that base parameters do
not move, adapter B tensors receive updates, and merged/unmerged outputs agree
within numerical tolerance. The saved adapter audit verifies nonzero B tensors.

Checkpoint selection uses FLEURS validation only. All previously reported
FLEURS/MLS test or follow-up samples are already known and must not be called
new blind evidence for this round. No evaluation clips are added to training.
The final score must be measured after reloading and merging the adapter, with
the same normalization and float32 batch-four greedy controls as E7/E8/E10.
Keep the previous checkpoint if this candidate regresses.

References: [official PEFT LoRA documentation](https://huggingface.co/docs/peft/en/package_reference/lora)
and [official Whisper LoRA training guide](https://huggingface.co/docs/peft/main/en/task_guides/int8-asr).
This local recipe uses the existing model in float32/BF16 and does not add
quantization or reproduce the guide's larger model/language experiment.


## Completed measurements

E16 trained 589,824 adapter parameters; all pretrained tensors stayed frozen.
The saved audit finds 48 nonzero B tensors. Best validation WER after merge is
5.8438%, compared with 6.3407% pretrained Small and 5.6052% retained full-tuned E10.
E16 does not replace E10 for FLEURS.

On the reused 300-clip MLS diagnostic, E16 achieves 7.8894% WER and 2.5483% CER,
versus E10 9.6270% / 3.4191%. This removes 198 errors (18.0% relative WER reduction).
One avoided repetitive hallucination contributes 157 of those fewer errors.
Only 62 clips improve and 36 worsen versus E10; against pretrained Small the
much smaller WER gain has an interval crossing zero. These known clips do not
establish broad generalization.

Peak allocated GPU memory: 1,570 MB, versus E10 4,746 MB (66.9% lower in these
measured recipes). Training/validation stage took 25.9 minutes. Merged inference
remains 241,734,912 parameters; this is a training-memory gain, not model compression.
Exact predictions and paired speaker-bootstrap comparisons are preserved in
`runs/E16/`; configuration and checkpoint hashes were frozen before this diagnostic.
