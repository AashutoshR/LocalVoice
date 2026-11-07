# Higher-rate refinement of the existing Small decoder

E15 starts from the saved E8 checkpoint on the same Whisper Small architecture.
It retains the original 2,796 FLEURS training clips, punctuation-aware targets,
verified Spanish/task prefix, frozen audio encoder, effective batch 16,
weight decay 0.05 and seed 42. It raises decoder learning rate from 2e-6 to
1e-5 and allows up to four further epochs. Full 407-clip validation checks
occur every 88 optimizer updates and at epoch end. Patience is two checks.

The hypothesis is that E8's low-rate curve, which still reached its best score
at its final epoch, left useful decoder adaptation unfinished. This changes
both learning rate and the number of updates; it does not isolate the causal
effect of learning rate alone. Encoder weights must remain unchanged, and
`runs/E15/weight-audit.json` verifies that against E8. The deployed architecture
and parameter count remain Small's existing values.

The candidate is compared with E8 and E10 using compatible FLEURS validation
scores. `runs/selection-small-refined.json` freezes the choice and saved-weight
hash before evaluating the selected Small checkpoint on the original 907-clip
FLEURS test corpus. That corpus was already examined in earlier rounds, so this
is explicitly a **reused-test diagnostic**, not a new blind evaluation. All
scores remain separate from validation and no further tuning follows them.
The matched baseline is E7, with the same pinned revision, normalization,
float32 batch-four greedy decoding and generation configuration.

Existing original test artifacts are preserved. This workflow runs after all
Tiny training and follow-up jobs, with one GPU workload at a time. Configuration:
`configs/small-refinement.json`.
