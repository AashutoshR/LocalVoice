# Corrected Spanish training prompt

On 31 October 2026, inspection of the actual fast-tokenizer output found that constructor language/task attributes did not match the serialized encoding post-processor. This was reproduced with both official pinned Tiny and Small tokenizers in the installed environment.

Before: `<|startoftranscript|><|notimestamps|>Hola.<|endoftext|>`.

After explicitly calling `set_prefix_tokens(language="spanish", task="transcribe", predict_timestamps=False)`: `<|startoftranscript|><|es|><|transcribe|><|notimestamps|>Hola.<|endoftext|>`.

Training removes the initial start token during collation, so the corrected target begins with Spanish, transcription and no-timestamp tokens. Generation already used that Spanish/task prefix. The old recipe therefore trained against a different decoder context. This is a concrete pipeline defect; its accuracy effect is measured by the new runs rather than assumed.

The implementation now configures and verifies actual encoded token IDs before training, records the verified prefix in training provenance, saves it with the processor, and reapplies it when loading inference processors. A regression test exercises the real local fast tokenizer and its save/reload round trip. The documented API is in the [official Transformers source](https://github.com/huggingface/transformers/blob/main/src/transformers/models/whisper/tokenization_whisper.py).

E9 repeats E5's conservative Tiny recipe with this correction. E8 restarts Small decoder adaptation with the correction. E0 and E7 remain valid pretrained baselines: their generation prompts were already explicitly set, and the correction does not change audio features or scoring references. The earlier E1–E6 measured results remain visible as superseded prompt recipes. No historical number is rewritten.

The interrupted initial E8 artifacts and log are preserved in `archives/spanish-prefix-mismatch/E8-20261031-2200/`. That run was stopped when the mismatch was verified, before publishing its results. Its training record is marked interrupted with the reason. The replacement starts from the original pinned Small model.

Both tracks preserve the same Spanish dataset, official train/validation/test membership, accents, scoring normalization, and validation-only checkpoint selection. The original Tiny test selection remains frozen separately; the Small track has its own selection file and matching baseline.
