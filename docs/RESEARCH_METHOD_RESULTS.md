# Research methods: controlled fine-tuning results

Updated 02 November 2026. Same existing Tiny and Small backbones; original FLEURS validation only. These are observed development results, not a fresh blind test or a multi-seed confirmation.

## Small: lower-encoder freezing

| Recipe | WER | CER | Word errors | Trainable weights | Stage time | Peak allocated GPU memory |
| --- | --- | --- | --- | --- | --- | --- |
| E7 · Whisper Small pretrained | 6.3407% | 2.1576% | 638 | 0 | 0.0 min | — |
| E8 · Whisper Small decoder tuning | 5.6748% | 1.8279% | 571 | 153,580,800 | 29.0 min | 3298 MB |
| E10 · Small encoder + decoder adaptation | 5.6052% | 1.8279% | 564 | 240,582,912 | 30.9 min | 4746 MB |
| E18 · Small matched full-tuning control | 5.5655% | 1.8160% | 560 | 240,582,912 | 31.2 min | 4797 MB |
| E19 · Small lower-six encoder blocks frozen | 5.5754% | 1.8177% | 561 | 196,104,960 | 37.6 min | 4031 MB |
| E20 · Small lower-nine encoder blocks frozen | 5.6251% | 1.7957% | 566 | 174,843,648 | 24.6 min | 3688 MB |

**E19 versus matched E18:** 5.5655% → 5.5754% WER; 1 more word error (-0.18% relative reduction). Paired utterance-bootstrap interval for WER reduction: -0.159 to 0.139 pp; 19 clips improve, 21 worsen. Negative reduction means regression. Intervals are exploratory after validation selection; speaker IDs are unavailable.

**E20 versus matched E18:** 5.5655% → 5.6251% WER; 6 more word errors (-1.07% relative reduction). Paired utterance-bootstrap interval for WER reduction: -0.244 to 0.112 pp; 24 clips improve, 27 worsen. Negative reduction means regression. Intervals are exploratory after validation selection; speaker IDs are unavailable.

## Tiny: training-only Fisher EWC

| Recipe | WER | CER | Word errors | Stage time |
| --- | --- | --- | --- | --- |
| E0 · Pretrained baseline | 20.7911% | 6.5032% | 2,092 | 0.0 min |
| E11 · Tiny stronger acoustic adaptation | 18.3959% | 5.8015% | 1,851 | 9.2 min |
| E17 · Tiny Latin American replay tuning | 18.6444% | 5.8015% | 1,876 | 5.0 min |
| E21 · Tiny matched replay control | 18.6842% | 5.8116% | 1,880 | 6.3 min |
| E22 · Tiny Fisher-protected replay | 18.5947% | 5.7829% | 1,871 | 7.4 min |
| E23 · Tiny stronger Fisher-protected replay | 18.8332% | 5.9046% | 1,895 | 9.6 min |

**E22 versus matched E21:** 18.6842% → 18.5947% WER; 9 fewer word errors (+0.48% relative reduction). Paired utterance-bootstrap interval for WER reduction: 0.010 to 0.180 pp; 8 clips improve, 2 worsen. Negative reduction means regression. Intervals are exploratory after validation selection; speaker IDs are unavailable.

**E23 versus matched E21:** 18.6842% → 18.8332% WER; 15 more word errors (-0.80% relative reduction). Paired utterance-bootstrap interval for WER reduction: -0.724 to 0.440 pp; 83 clips improve, 88 worsen. Negative reduction means regression. Intervals are exploratory after validation selection; speaker IDs are unavailable.

## Which checkpoint is retained?

- Small: **E18**, 5.5655% WER. Compared with previous E10: +0.0398 pp WER reduction, +4 fewer word errors. This is an observed validation gain; independent generalization remains unverified.
- Tiny: **E11**, 18.3959% WER. Compared with previous E11: +0.0000 pp WER reduction, +0 fewer word errors. The earlier checkpoint remains selected; the new methods did not beat it.

## Implementation and limits

- Small arms share E8 initialization, source clips, seed, learning-rate schedule and augmentation. E19/E20 additionally freeze the acoustic front end plus the specified lower blocks. Actual stopping times can differ.
- Tiny arms share E11 initialization and replay data. E22 adds a unit-trace diagonal empirical Fisher penalty with lambda 10000, estimated from 128 original training clips. Its preparation time is recorded separately.
- Saved-weight audits verify protected layers stayed unchanged. Fisher hashes and training-only sample membership are verified before adaptation.
- `runs/research-input-audit.json` verifies identical initial weights, actual training text/audio, prefix, generation settings and learning rates within both controlled comparisons.
- No existing FLEURS/MLS test or Latin holdout was used for coefficient/layer/checkpoint selection. No new holdout evaluation is claimed in this round.
- A smaller training-memory footprint is a separate outcome from recognition accuracy. Inference architecture size stays the same within each backbone.
- E23 is a separately preserved follow-up at lambda 1e7, chosen from E22 training penalty scale before reading its validation scores. The original five recipes and first selection are unchanged.
- Method details and source papers: `docs/RESEARCH_METHODS_IMPLEMENTATION.md`; configs: `configs/research-e18.json` through `research-e23.json`.
