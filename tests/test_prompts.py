from pathlib import Path
from types import SimpleNamespace
import pytest
from localvoice.prompts import align_spanish_processor, canonical_generation


def test_real_fast_tokenizer_encodes_spanish_task_prefix_and_keeps_it_on_save(tmp_path):
    transformers = pytest.importorskip("transformers")
    source = Path(__file__).resolve().parents[1] / "data/models/whisper-small"
    if not (source / "tokenizer.json").exists():
        pytest.skip("Optional local Whisper tokenizer assets not downloaded")
    tokenizer = transformers.WhisperTokenizerFast.from_pretrained(source, language="spanish", task="transcribe", local_files_only=True)
    expected = ['<|startoftranscript|>', '<|es|>', '<|transcribe|>', '<|notimestamps|>']
    assert align_spanish_processor(SimpleNamespace(tokenizer=tokenizer)) == expected
    assert tokenizer.convert_ids_to_tokens(tokenizer('Hola.').input_ids[:4]) == expected
    tokenizer.save_pretrained(tmp_path)
    restored = transformers.WhisperTokenizerFast.from_pretrained(tmp_path, local_files_only=True)
    align_spanish_processor(SimpleNamespace(tokenizer=restored))
    assert restored.convert_ids_to_tokens(restored('Hola.').input_ids[:4]) == expected


def test_checkpoint_save_preserves_pinned_generation_rules(tmp_path):
    transformers = pytest.importorskip("transformers")
    pytest.importorskip("torch")
    source = Path(__file__).resolve().parents[1] / "data/models/whisper-small"
    if not (source / "generation_config.json").exists():
        pytest.skip("Optional local generation configuration not downloaded")
    cfg = transformers.WhisperConfig(vocab_size=51865, d_model=16, encoder_layers=1,
        decoder_layers=1, encoder_attention_heads=2, decoder_attention_heads=2,
        encoder_ffn_dim=32, decoder_ffn_dim=32, max_source_positions=5, max_target_positions=64)
    model = transformers.WhisperForConditionalGeneration(cfg)
    settings = dict(model_revision="973afd24965f72e36ca33b3055d56a652f456b4d", language="spanish")
    digest = canonical_generation(model, settings, source)
    expected = list(model.generation_config.suppress_tokens)
    assert 50358 in expected and 50359 in expected
    model.save_pretrained(tmp_path, safe_serialization=True)
    saved = transformers.GenerationConfig.from_pretrained(tmp_path, local_files_only=True)
    assert saved.suppress_tokens == expected
    assert saved.language == 'spanish' and saved.task == 'transcribe'
    other = SimpleNamespace(config=SimpleNamespace())
    assert canonical_generation(other, settings, source) == digest
