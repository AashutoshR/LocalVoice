# Fine-tuning the existing Tiny model with teacher regularization

## Problem observed

E11's validation WER reached 18.40% at epoch 2, then worsened even as its
training loss continued falling. E10's Small result was 5.61%, only 0.07
percentage points below the previous 5.67%. Neither is a large improvement.
The independent 300-clip MLS check also showed regressions: E11 25.68% versus
pretrained Tiny 22.13%, and E10 9.63% versus pretrained Small 8.16%. These
results are preserved and do not establish broad Spanish improvement.

## Training change

E12 is another fine-tuning recipe for the same existing `openai/whisper-tiny`
architecture, initialized from E9. It does not introduce a larger deployed
model. The already available pretrained Small baseline E7 acts as a frozen
training teacher. Its logits are computed only for the 2,796 training clips,
conditioned on the same training target tokens. No teacher-generated reference
replaces a validation or test transcript.

The objective is `0.5 × supervised cross-entropy + 0.5 × T² KL(teacher || student)`,
with temperature `T=2`. Padding targets are excluded from KL. Teacher logits
are detached, all teacher parameters are frozen, and the teacher stays in
evaluation mode. The teacher sees clean features; Tiny receives light training
time masking. This tests whether a soft-target penalty reduces the drift
seen with supervised fitting alone. It is not a guarantee of improvement.

The student retains trainable encoder and decoder weights, learning rate
`1e-5`, effective batch 16, weight decay 0.05, 5% warmup, linear decay, and seed
42. Microbatch 4 with four accumulation steps fits the frozen teacher and
student on the existing GPU. The run allows at most six epochs and stops
after three validation checks without improvement. The complete configuration
is `configs/tiny-regularized.json`.

Implementation reference: the official
[Distil-Whisper training code](https://github.com/huggingface/distil-whisper/tree/main/training).
This project uses token-level teacher regularization on the existing Tiny
architecture; it does not claim to reproduce Distil-Whisper, its architecture,
training scale, or published performance.

## What would count as better

Compare the final saved Tiny checkpoint against E0, E9 and E11 on exactly the
same 407 FLEURS validation clips, normalization, pinned model revision,
float32 single-clip greedy decoding, and token limits. Report absolute WER/CER,
relative reductions, error counts, paired improved/worsened clips, and cost.
E11's 18.40% WER is the previous best Tiny validation result to beat. A change
in model size cannot be credited as fine-tuning improvement.

Intermediate checks use batch four; the reloaded final evaluation uses the
published Tiny single-clip protocol. Checkpoint selection uses validation WER.
The earlier MLS test was already read before this exploratory round. E12 must
not be described as validated on a fresh blind holdout, and the original MLS
scores must not be retuned, replaced, or silently removed.
