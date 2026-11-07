from types import SimpleNamespace
import numpy as np
import pytest


def test_playground_explicitly_uses_cached_autoregressive_decoding(monkeypatch):
    torch = pytest.importorskip("torch")
    from localvoice import inference
    calls = []

    class Processor:
        def __call__(self, *a, **k):
            return SimpleNamespace(input_features=torch.zeros(1, 80, 10), attention_mask=torch.ones(1, 10))

        def batch_decode(self, *a, **k):
            return ["hola mundo"]

    class Model:
        def generate(self, features, **kwargs):
            calls.append(kwargs)
            return torch.tensor([[1, 2]])

    monkeypatch.setattr(inference, "_loaded", None)
    monkeypatch.setattr(inference, "load_model", lambda _: (Processor(), Model(), "cpu"))
    monkeypatch.setattr(torch.cuda, "is_available", lambda: False)
    result = inference.transcribe(np.zeros(16000, dtype=np.float32))
    assert result["transcript"] == "hola mundo"
    assert calls[0]["use_cache"] is True and calls[0]["max_new_tokens"] == 225
