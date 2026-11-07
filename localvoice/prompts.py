"""Keep the tokenizer's serialized fast post-processor aligned with generation."""


def align_spanish_processor(processor, language="spanish"):
    tokenizer = processor.tokenizer
    tokenizer.set_prefix_tokens(language=language, task="transcribe", predict_timestamps=False)
    expected = tokenizer.prefix_tokens
    actual = tokenizer("Hola.").input_ids
    if actual[:len(expected)] != expected:
        raise ValueError("Encoded training labels do not contain the configured decoder prefix")
    names = tokenizer.convert_ids_to_tokens(expected)
    if "<|es|>" not in names or "<|transcribe|>" not in names or "<|notimestamps|>" not in names:
        raise ValueError("Spanish transcription prompt tokens are missing")
    return names


def canonical_generation(model, settings, source):
    """Use pinned pretrained decoding rules, including after HF checkpoint saves."""
    import hashlib
    import json
    from transformers import GenerationConfig
    generation = GenerationConfig.from_pretrained(source, revision=settings["model_revision"])
    generation.language = settings["language"]
    generation.task = "transcribe"
    generation.forced_decoder_ids = None
    generation.use_cache = True
    generation.num_beams = 1
    generation.do_sample = False
    model.generation_config = generation
    # save_pretrained migrates legacy model-config generation fields. Keep
    # them identical so that migration cannot silently change suppression.
    for key in ("suppress_tokens", "begin_suppress_tokens", "forced_decoder_ids", "max_length"):
        setattr(model.config, key, getattr(generation, key))
    effective = generation.to_dict()
    for key in list(effective):
        if key.startswith("_") or key == "transformers_version":
            effective.pop(key)
    effective["max_new_tokens"] = 225
    digest = hashlib.sha256(json.dumps(effective, sort_keys=True, ensure_ascii=False).encode()).hexdigest()
    model._localvoice_generation_sha256 = digest
    return digest
