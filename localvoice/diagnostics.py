"""Paired validation error analysis, with utterance-level bootstrap uncertainty."""
import json
import numpy as np
from jiwer import process_words
from .core import ROOT, normalize, write_json


def compare_predictions(experiment, split="validation", repetitions=5000, baseline_id="E0", cluster_field=None, primary=True):
    def read(run):
        return json.loads((ROOT / "runs" / run / f"predictions-{split}.json").read_text(encoding="utf-8"))

    baseline, tuned = read(baseline_id), read(experiment)
    if len(baseline) != len(tuned) or any(
        (a["audio_path"], a["transcript"]) != (b["audio_path"], b["transcript"])
        for a, b in zip(baseline, tuned)
    ):
        raise ValueError("Paired analysis requires identical ordered clips and references")
    counts, cases = [], []
    for a, b in zip(baseline, tuned):
        ref = normalize(a["transcript"])
        base = process_words(ref, normalize(a["hypothesis"]))
        new = process_words(ref, normalize(b["hypothesis"]))
        base_errors = base.substitutions + base.insertions + base.deletions
        new_errors = new.substitutions + new.insertions + new.deletions
        words = len(ref.split())
        counts.append([base_errors, new_errors, words])
        cases.append({"audio_path": a["audio_path"], "reference": a["transcript"],
                      "baseline": a["hypothesis"], "tuned": b["hypothesis"],
                      "baseline_errors": base_errors, "tuned_errors": new_errors,
                      "errors_removed": base_errors - new_errors})
    values = np.asarray(counts)
    sampling_values = values
    if cluster_field:
        grouped = {}
        for row, other, count in zip(baseline, tuned, counts):
            key = row.get(cluster_field)
            if not key or key != other.get(cluster_field):
                raise ValueError("Cluster bootstrap needs identical nonempty grouping metadata")
            grouped.setdefault(key, np.zeros(3, dtype=np.int64))
            grouped[key] += count
        if len(grouped) < 2:
            raise ValueError("Cluster bootstrap needs at least two groups")
        sampling_values = np.asarray(list(grouped.values()))
    rng = np.random.default_rng(42)
    draws = rng.integers(0, len(sampling_values), size=(repetitions, len(sampling_values)))
    totals = sampling_values[draws].sum(axis=1)
    reductions = 100 * (totals[:, 0] - totals[:, 1]) / totals[:, 2]
    total = values.sum(axis=0)
    result = {"experiment": experiment, "baseline_id": baseline_id, "split": split, "samples": len(values),
              "method": (f"paired {cluster_field} cluster bootstrap" if cluster_field else "paired utterance bootstrap") + "; seed 42; percentile interval; " +
                        ("exploratory after validation selection" if split == "validation" else "held-out evaluation after validation-only selection"),
              "bootstrap_repetitions": repetitions,
              "sampling_units": len(sampling_values), "cluster_field": cluster_field,
              "wer_reduction_pp": 100 * (total[0] - total[1]) / total[2],
              "wer_reduction_95_interval_pp": np.quantile(reductions, [.025, .975]).tolist(),
              "errors_removed": int(total[0] - total[1]),
              "utterances_improved": sum(c["errors_removed"] > 0 for c in cases),
              "utterances_worsened": sum(c["errors_removed"] < 0 for c in cases),
              "examples_improved": sorted(cases, key=lambda c: -c["errors_removed"])[:10],
              "examples_worsened": sorted(cases, key=lambda c: c["errors_removed"])[:10]}
    write_json(ROOT / "runs" / experiment / f"paired-{split}-vs-{baseline_id}.json", result)
    if primary:
        write_json(ROOT / "runs" / experiment / f"paired-{split}.json", result)
    return result
