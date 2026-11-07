from types import SimpleNamespace
import numpy as np
import pytest
torch = pytest.importorskip("torch")
from localvoice import training


@pytest.mark.parametrize("batch_size,expected", [(1, [1, 1, 1, 1, 1]), (2, [2, 2, 1])])
def test_evaluation_keeps_tail_batch_order_and_references(monkeypatch, batch_size, expected):
    class Processor:
        def __call__(self, audio, **kwargs):
            features = torch.tensor(np.stack(audio))
            return SimpleNamespace(input_features=features, attention_mask=torch.ones_like(features))

        def batch_decode(self, ids, **kwargs):
            return [f"clip {int(row[0])}" for row in ids]

    class Model:
        sizes = []
        def eval(self):
            return self

        def generate(self, features, **kwargs):
            self.sizes.append(len(features))
            assert kwargs["max_new_tokens"] == 225
            assert kwargs["attention_mask"].shape == features.shape
            return features.long()

    monkeypatch.setattr(training, "decode_audio", lambda path: np.array([int(path)], dtype=np.float32))
    rows = [{"audio_path": str(i), "transcript": f"clip {i}"} for i in range(5)]
    model = Model()
    metrics, predictions = training.evaluate_rows(model, Processor(), rows, "cpu", context={"evaluation_batch_size": batch_size})
    assert model.sizes == expected
    assert metrics["samples"] == 5 and metrics["wer"] == 0
    assert [p["audio_path"] for p in predictions] == [str(i) for i in range(5)]
