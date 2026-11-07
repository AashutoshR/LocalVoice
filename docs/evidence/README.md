# Published experiment evidence

These JSON snapshots contain measured metrics and selected provenance for the
reported Spanish experiments. They are derived exports, not replacement model
checkpoints or complete raw training records.

Machine-local project paths are exported relative to the repository. Numerical
results, checkpoint hashes and historical dataset fingerprints are unchanged.
The original fingerprints include manifest paths as well as audio content and
labels, so a different checkout can produce a different fingerprint; they verify
identity within the original run environment, not cross-machine byte equivalence.

Complete local histories, predictions and checkpoints remain under `runs/`, which
is excluded from Git alongside downloaded audio and model weights under `data/`.
Use the source dataset links and experiment configurations to reproduce training.
