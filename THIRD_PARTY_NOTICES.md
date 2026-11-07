# External models, datasets and research

Downloaded models, audio corpora and local training checkpoints are not included
in this source upload. External resources retain their own licenses and terms.

| Resource | Attribution / source | Stated license |
| --- | --- | --- |
| Whisper Tiny and Small | [OpenAI Whisper](https://github.com/openai/whisper) | Apache-2.0 |
| FLEURS, Spanish `es_419` | [Google FLEURS](https://huggingface.co/datasets/google/fleurs) | CC-BY-4.0 |
| Spanish Multilingual LibriSpeech | [OpenSLR 94](https://www.openslr.org/94/) | CC-BY-4.0 |
| Argentinian Spanish recordings | [OpenSLR 61](https://www.openslr.org/61/), Google 2018/2019; Guevara-Rukoz et al., LREC 2020 | CC-BY-SA-4.0 |

The Argentinian recordings are associated with Guevara-Rukoz et al.,
[Crowdsourcing Latin American Spanish for Low-Resource Text-to-Speech](https://aclanthology.org/2020.lrec-1.801/).
Dataset preparation preserves source and license metadata locally. Attribution
here does not relicense the source datasets or trained artifacts.

The fine-tuning methods are described with citations in
[the research review](docs/RESEARCH_FINE_TUNING_NEXT_STEPS.md) and
[implementation notes](docs/RESEARCH_METHODS_IMPLEMENTATION.md). Papers are linked,
not bundled. Dependencies are installed separately through `pyproject.toml`; this
repository does not vendor their code or model weights.
