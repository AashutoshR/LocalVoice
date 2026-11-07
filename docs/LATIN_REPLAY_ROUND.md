# Target-matched replay tuning of the existing Tiny model

E17 starts from the retained E11 Tiny checkpoint. It retains the original
FLEURS training clips and adds a deterministic sample of human-recorded
Argentinian Spanish sentences from [OpenSLR 61](https://www.openslr.org/61/).
The hypothesis is that Latin American read speech is closer to the original
`es_419` task than the earlier audiobook-heavy mixture. That is a hypothesis,
not a promised accuracy gain. No additional pretrained backbone is introduced.

The public corpus contains 5,739 recordings from volunteers in Buenos Aires.
Its source license is **CC-BY-SA-4.0**, distinct from FLEURS' CC-BY-4.0.
Source attribution: Guevara-Rukoz et al.,
[Crowdsourcing Latin American Spanish for Low-Resource Text-to-Speech](https://aclanthology.org/2020.lrec-1.801/),
LREC 2020; copyright Google 2018/2019. This project uses the human sentence
recordings, excluding the separate weather-message collection.

## Data partition fixed before training

The preparer reads both public sentence indexes and audio archives, checks
archive CRCs during extraction, records source SHA-256s, converts to mono 16kHz,
and excludes invalid/overlong audio, corrupt text, duplicate audio, and exact
FLEURS evaluation references. Opaque file IDs are retained; undocumented IDs
are not treated as speaker identities, and gender is never used to infer them.

Seed 43 selects 300 normalized reference-text groups not present anywhere in
FLEURS. One clip per group is held out, and every clip with any of those texts
is excluded from added training. Seed 42 samples up to 3,000 remaining clips.
Thus the holdout is text-disjoint from both FLEURS and the added training
sample. Speaker IDs are unavailable: speaker independence cannot be verified.
All selected IDs, hours, exclusions and fingerprints are frozen in
`data/latin-spanish/source.json` before E17 training. Published natural target
text is retained only when its normalized words exactly match its transcript.

## Prespecified recipe and evaluation

`configs/tiny-latin-replay.json`: initial E11 weights, learning rate 5e-6 for
encoder and decoder, effective batch 16, seed 42, weight decay 0.05, 5% warmup,
linear decay, light train-only time masking, four-epoch maximum, and patience
two validation checks. The original FLEURS training clips provide replay.
Training-data license/provenance is explicit in the configuration and artifacts.

Select using only the original 407 FLEURS validation clips, then score the
reloaded model with the original Tiny float32 single-clip greedy protocol.
Retain E11 if the new recipe regresses. Multiple recipe/data settings change
together, so attribution to one setting alone is not established.

After freezing validation choices and checkpoint files, compare E0, E11 and
E17 on the new 300-clip holdout using identical batch-four float32 greedy
decoding. These are locally untrained phrases, with unknown speaker and
pretraining overlap. Do not describe them as independently unseen speakers.
No further E17 tuning uses their scores. Existing MLS/FLEURS test results are
already known and are not fresh blind evidence for this round.


## Completed result

The same Tiny backbone scores 19.8016% WER / 7.1109% CER on the reserved 300
Latin American recordings, versus E11 24.9658% / 9.3629% and pretrained E0
24.4186% / 9.1328%. That is 151 fewer word errors versus E11, 20.7% relative
WER reduction, and 105 clips improved versus 23 worsened. Error counts change
from 559 to 440 substitutions, 90 to 72 deletions, and 81 to 67 insertions.
The exploratory utterance-bootstrap WER-reduction interval is 3.66–6.71 pp;
missing speaker identities prevent accounting for speaker-level dependence.

FLEURS validation regresses from E11 18.3959% to E17 18.6444% WER (25 additional
errors), with unchanged CER 5.8015%. E11 therefore remains selected for FLEURS.
E17 is evidence of useful local domain adaptation, not broad Spanish superiority.
The stage required 5.0 minutes of training/validation (32.1 cumulative including
E11 ancestry), 545 optimizer updates, and 1,265 MB peak allocated GPU memory.
The saved checkpoint at update 182 is selected before holdout evaluation.
Weight audit verifies 66/67 encoder and 100/100 decoder tensors changed from E11.
Inference remains 37,760,640 parameters. All metrics and actual predictions are
preserved under `runs/E*/metrics-latin-holdout.json` and matching prediction files.
