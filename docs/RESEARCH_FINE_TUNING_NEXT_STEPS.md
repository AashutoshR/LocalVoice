# Research review: improving the existing Spanish Whisper models

Implementation update: partial encoder freezing and Fisher EWC have now been implemented and evaluated. See [the actual results](RESEARCH_METHOD_RESULTS.md). The review below records the earlier rationale and proposals.

Reviewed 1 November 2026. This is a literature review and proposed experiment design, not a report of new training results. Tiny and Small remain the only deployment backbones. Paper results below are not directly comparable to our scores.

## What our artifacts suggest

- Retained FLEURS validation minima: Tiny E11 18.3959% WER; Small E10 5.6052%. Later recipes have not beaten them.
- Tiny E17 improves the reserved Argentinian sample from E11 24.9658% to 19.8016%, but worsens FLEURS to 18.6444%. That is an observed domain tradeoff; forgetting/overfitting are hypotheses explaining it, not established causes.
- Small E16 uses decoder-only query/value LoRA (rank 8). It improves a reused MLS diagnostic relative to E10, but regresses on FLEURS. A large portion of its diagnostic gain is one avoided hallucination.
- Current training supports either a fully frozen or fully trainable encoder. It does not yet implement partial lower-layer freezing, EWC, adaptive ranks, or weight interpolation. E12's failed cross-backbone teacher experiment does not test EWC or old-checkpoint weight averaging.
- Most completed runs use seed 42. Repeating finalists is necessary to distinguish a stable gain from run variability.

## Papers and transferable lessons

### 1. Partial encoder freezing — highest-priority new training method

Liu, Yang and Qu, **Exploration of Whisper fine-tuning strategies for low-resource ASR**, EURASIP JASMP, 2024. [Publisher full text](https://link.springer.com/article/10.1186/s13636-024-00349-3).

The authors compare full adaptation, freezing lower encoder layers, reinitialization and adapters on seven FLEURS languages using large-v2. Their best lower-layer-freezing configurations average 6.27% relative WER reduction versus ordinary fine-tuning. Top-layer reinitialization is unhelpful. Their methods section also describes checkpoint selection using test results; we should use validation instead. The languages and model size differ from ours.

**Our proposed adaptation:** retain the original acoustic features in lower layers while adapting the upper encoder and decoder. Small has 12 encoder blocks: compare freezing blocks 0–5 and 0–8 against an otherwise identical train-all control. Fix initialization, data, optimizer schedule and update budget across these arms. Use the same principle on Tiny only after the Small ablation. These block counts are our hypotheses, not settings prescribed for Small by the paper.

### 2. Weight averaging — cheapest retention experiment

Vander Eeckt and Van hamme, **Weight Averaging: A Simple Yet Effective Method to Overcome Catastrophic Forgetting in Automatic Speech Recognition**, ICASSP 2023. [Full text](https://arxiv.org/html/2210.15282v2).

The paper averages parameters before and after adaptation, optionally adding old-model distillation during training. Its system is a Conformer/Transformer ASR model, not Whisper; applying it here is a transfer hypothesis.

**Our proposed adaptation:** because E17 descends from E11, form `theta = (1-alpha)*theta_E11 + alpha*theta_E17` for a small prespecified set of alpha values. Preserve both originals. Check matching tensor names, vocabulary and configuration, and calculate in float32. Select using development data, never the already-read Latin holdout. This is post-training interpolation, not a new optimizer fine-tuning run or a larger model. There is no guarantee that it beats either endpoint.

### 3. EWC — explicitly protect useful existing weights

Qian et al., **Learn and Don't Forget: Adding a New Language to ASR Foundation Models**, Interspeech 2024. [Paper](https://www.isca-archive.org/interspeech_2024/qian24_interspeech.pdf).

Using Whisper large-v3, the authors study new-language adaptation and show an EWC stability/adaptation tradeoff. EWC penalizes changes to parameters important to a previous task, estimated using diagonal Fisher information. Their supported-language checks include Spanish, but the main adaptation is not Spanish-only Tiny/Small tuning.

**Our proposed adaptation:** estimate importance using original FLEURS training clips at E11; protect that checkpoint during Latin American replay tuning. Compare cross-entropy alone with cross-entropy plus EWC under identical data and optimizer controls. Never estimate Fisher from validation or test clips. This is different from the E12 Small-teacher penalty. Normalize the Fisher estimate and tune the penalty on development data; blindly copying a published coefficient is inappropriate.

### 4. Better LoRA placement and adaptive rank

Xu et al., **Towards Rehearsal-Free Multilingual ASR: A LoRA-based Case Study on Whisper**, Interspeech 2024. [Paper](https://www.isca-archive.org/interspeech_2024/xu24h_interspeech.pdf).

The study uses attention and feed-forward projections, adaptive rank allocation, and orthogonal constraints for sequential learning. It evaluates base/large models on Chinese, Uyghur and Tibetan. Crucially, its orthogonal method requires earlier task adapters; it cannot directly recover all pretrained Whisper languages from nonexistent original LoRA matrices.

**Our proposed adaptation:** first compare decoder query/value adapters with broader attention placement at matched trainable-parameter budget; then test AdaLoRA if placement matters. E16 does not establish whether encoder or output projections help. Treat O-AdaLoRA as a later continual-adaptation method, potentially anchored to a saved Spanish adapter, not a drop-in guarantee of preserving pretraining.

### 5. Curriculum and quality filtering

Tan et al., **CBA-Whisper: Curriculum Learning-Based AdaLoRA Fine-Tuning on Whisper for Low-Resource Dysarthric Speech Recognition**, Interspeech 2025. [Paper](https://www.isca-archive.org/interspeech_2025/tan25b_interspeech.pdf) · [author implementation](https://github.com/tan90xx/CBA-Whisper).

The system combines adaptive ranks, staged data selection and pre/postprocessing on large-v2 for dysarthric speech. Its reported challenge improvement is for the combined system; it is not an isolated AdaLoRA effect or a Spanish forecast. The authors note that filtering can remove useful linguistic diversity.

**Our proposed adaptation:** audit training-only clipping, alignment, duplicates and implausible duration/text ratios; introduce difficult clips gradually while retaining accents and rare words. Compare against a matched unfiltered control. High baseline WER alone is not evidence that a human transcript is wrong. Keep any VAD, decoding or text postprocessing experiments separate from the fixed fine-tuning benchmark.

## Spanish-specific context and lower-priority work

- The original [HiTZ Spanish Small model card](https://huggingface.co/HiTZ/whisper-small-es) documents adaptation of the same Small backbone on Common Voice 13 Spanish, reporting 8.2668% WER on its own evaluation split. That is not comparable with our 5.61% FLEURS result and is not a reason to replace our model. Its dataset/procedure are useful references.
- [Whisper-LM](https://arxiv.org/abs/2503.23542), de Zuazo et al., 2025 preprint, combines fine-tuned ASR with language models. This is relevant to vocabulary/language errors, but changes the inference system; do not attribute a rescoring gain solely to fine-tuning. Lower priority for the current request.
- [Fine-tuning Whisper on Low-Resource Languages for Real-World Applications](https://arxiv.org/abs/2412.15726), Timmel et al., revised 2025, addresses preserving long-form segmentation through constructed training sequences in Swiss German. Our current playground is limited to 30-second clips, so this becomes relevant if product scope expands to recordings and meetings.

## Bounded next experiment sequence — proposal, not launched

1. **Freeze the evaluation protocol and target.** Primary target remains same-backbone FLEURS WER. Record a second, explicit retention target on Latin American development speech. Reserve development transcript groups from unused training-source material without touching the existing holdout or allowing reference overlap. Speaker identities are missing there, so do not claim speaker separation.
2. **Cheap diagnostic first:** evaluate three interior E11/E17 interpolation points, with endpoints as controls, on development sets only. Label all such records as interpolation, not additional training. If none improves the desired tradeoff, stop that branch.
3. **Actual training first priority:** Small train-all versus two lower-layer-freezing arms from the same pinned pretrained Small initialization, using the same FLEURS training clips, seed, update budget, target text and hyperparameters. This isolates freezing instead of confounding it with a different parent checkpoint.
4. **One retention experiment:** E11-to-Latin replay with and without EWC, all other settings held fixed. Broader/adaptive LoRA is the next branch if these methods are unhelpful, rather than running every idea simultaneously.
5. **Repeat only finalists across three seeds** (for example 17, 42, 123). Report each run plus mean/spread, actual error counts and paired uncertainty. Keep old results visible. Do not promote a lower-memory checkpoint as the accuracy winner when WER regresses.
6. **Evaluate once on genuinely untouched data after selection.** Existing FLEURS/MLS tests and the E17 Latin holdout have already been read. Future measurements on them are reused diagnostics. A fresh final test must be reserved independently; development improvements alone do not demonstrate broad generalization.

Keep accents/ñ, normalization, Spanish task prefix, generation configuration, maximum output length and per-backbone evaluation batches fixed. Report WER and CER for each corpus separately. No paper justifies guaranteeing a particular gain on our data.

## Practical recommendation

Start with partial lower-encoder freezing for a new training method and weight interpolation as an inexpensive retention probe. EWC is the next targeted method because it addresses the observed source/target tradeoff. These choices follow the literature and the project's actual gaps, rather than increasing backbone size or continuing uncontrolled learning-rate changes.
