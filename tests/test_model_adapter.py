from types import SimpleNamespace

import pytest

from engine import model_adapter


def test_quantized_inference_evicts_owned_cache_and_uses_chat_template(
    monkeypatch, tmp_path
):
    """Oracle: mocked loading/generation; live7B checks are separately recorded."""
    torch = pytest.importorskip("torch")
    transformers = pytest.importorskip("transformers")
    pytest.importorskip("peft")
    monkeypatch.setattr(torch.cuda, "is_available", lambda: True)
    emptied = []
    monkeypatch.setattr(torch.cuda, "empty_cache", lambda: emptied.append(True))
    templates = []
    loads = []

    class Inputs(dict):
        def to(self, device):
            """Oracle: CPU test tensor mapping."""
            return self

    class Tokenizer:
        pad_token = "<eos>"
        eos_token_id = 2
        pad_token_id = 2

        def apply_chat_template(self, messages, **kwargs):
            """Oracle: verify prompt uses model's template."""
            templates.append(messages)
            return "chat"

        def __call__(self, prompt, **kwargs):
            """Oracle: bounded input token tensor."""
            return Inputs(input_ids=torch.tensor([[1, 1]]))

        def decode(self, completion, **kwargs):
            """Oracle: bounded generated body."""
            return "begin end;"

    class Model:
        config = SimpleNamespace(max_position_embeddings=4096)

        def eval(self):
            """Oracle: mocked inference state."""

        def parameters(self):
            """Oracle: CPU mock device."""
            return iter([torch.zeros(1)])

        def generate(self, **kwargs):
            """Oracle: known EOS-terminated output."""
            return torch.tensor([[1, 1, 3, 2]])

    def load_model(*args, **kwargs):
        """Oracle: record quantized loading options without allocating weights."""
        loads.append(kwargs)
        return Model()

    monkeypatch.setattr(
        transformers.AutoTokenizer,
        "from_pretrained",
        lambda *args, **kwargs: Tokenizer(),
    )
    monkeypatch.setattr(
        transformers.AutoModelForCausalLM, "from_pretrained", load_model
    )
    model_adapter._CACHE.clear()
    model_adapter._CACHE[("old", "", True)] = (None, None, None)
    try:
        assert (
            model_adapter.generate_with_adapter(
                "body", str(tmp_path), "", quantized=True
            )
            == "begin end;"
        )
        assert emptied == [True]
        assert templates == [[{"role": "user", "content": "body"}]]
        assert loads[0]["device_map"] == {"": 0}
        assert len(model_adapter._CACHE) == 1
    finally:
        model_adapter._CACHE.clear()
