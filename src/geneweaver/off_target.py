
"""Off-target analysis utilities for CRISPR candidate results."""

from collections import Counter
from typing import Any


def group_candidates_by_guide(
    candidates: list[dict[str, Any]],
) -> dict[str, list[dict[str, Any]]]:
    """Group CRISPR candidates by their guide RNA sequence."""

    if not isinstance(candidates, list):
        raise TypeError("Candidates must be provided as a list.")

    grouped: dict[str, list[dict[str, Any]]] = {}

    for index, candidate in enumerate(candidates):
        if not isinstance(candidate, dict):
            raise TypeError(
                f"Candidate at index {index} must be a dictionary."
            )

        guide = candidate.get("guide_rna")

        if not isinstance(guide, str) or not guide.strip():
            raise ValueError(
                f"Candidate at index {index} has an invalid guide RNA."
            )

        normalized_guide = guide.strip().upper()

        grouped.setdefault(normalized_guide, []).append(candidate.copy())

    return dict(sorted(grouped.items()))


def analyze_off_targets(
    candidates: list[dict[str, Any]],
    intended_target: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Analyze potential off-target sites for a guide RNA.

    An intended target is identified using genomic start, end,
    and strand coordinates.

    The specificity score is a heuristic based on mismatch-weighted
    off-target counts. It is not a biological safety prediction.
    """

    required_fields = {
        "start",
        "end",
        "strand",
        "mismatches",
    }

    if not isinstance(candidates, list):
        raise TypeError("Candidates must be provided as a list.")

    if intended_target is not None:
        if not isinstance(intended_target, dict):
            raise TypeError("Intended target must be a dictionary.")

        missing = required_fields - intended_target.keys()

        if missing:
            raise ValueError(
                f"Intended target is missing fields: "
                f"{', '.join(sorted(missing))}"
            )

    grouped = group_candidates_by_guide(candidates)

    if len(grouped) > 1:
        raise ValueError(
            "Analyze one guide RNA at a time. "
            "Use group_candidates_by_guide() first."
        )

    for index, candidate in enumerate(candidates):
        missing = required_fields - candidate.keys()

        if missing:
            raise ValueError(
                f"Candidate at index {index} is missing fields: "
                f"{', '.join(sorted(missing))}"
            )

        if candidate["strand"] not in {"+", "-"}:
            raise ValueError("Invalid candidate strand.")

        for field in ("start", "end", "mismatches"):
            value = candidate[field]

            if isinstance(value, bool) or not isinstance(value, int):
                raise TypeError(f"Candidate {field} must be an integer.")

        if candidate["start"] < 0:
            raise ValueError("Candidate start cannot be negative.")

        if candidate["end"] <= candidate["start"]:
            raise ValueError("Candidate end must exceed start.")

        if candidate["mismatches"] < 0:
            raise ValueError("Mismatch count cannot be negative.")

    if intended_target is not None:
        if intended_target["strand"] not in {"+", "-"}:
            raise ValueError("Invalid intended target strand.")

        for field in ("start", "end"):
            value = intended_target[field]

            if isinstance(value, bool) or not isinstance(value, int):
                raise TypeError(
                    f"Intended target {field} must be an integer."
                )

        if (
            intended_target["start"] < 0
            or intended_target["end"] <= intended_target["start"]
        ):
            raise ValueError("Invalid intended target coordinates.")

    def location(candidate):
        return (
            candidate["start"],
            candidate["end"],
            candidate["strand"],
        )

    intended_location = (
        location(intended_target)
        if intended_target is not None
        else None
    )

    intended_found = False
    off_targets = []

    for candidate in candidates:
        if (
            intended_location is not None
            and location(candidate) == intended_location
            and not intended_found
        ):
            intended_found = True
            continue

        off_targets.append(candidate.copy())

    mismatch_distribution = Counter(
        candidate["mismatches"]
        for candidate in off_targets
    )

    forward_count = sum(
        candidate["strand"] == "+"
        for candidate in off_targets
    )

    reverse_count = sum(
        candidate["strand"] == "-"
        for candidate in off_targets
    )

    exact_count = mismatch_distribution.get(0, 0)

    mismatched_count = len(off_targets) - exact_count

    weighted_burden = sum(
        1.0 / (candidate["mismatches"] + 1)
        for candidate in off_targets
    )

    specificity_score = (
        round(100.0 / (1.0 + weighted_burden), 2)
        if intended_target is not None and intended_found
        else None
    )

    off_targets.sort(
        key=lambda candidate: (
            candidate["mismatches"],
            candidate["start"],
            candidate["end"],
            candidate["strand"],
        )
    )

    return {
        "guide_rna": next(iter(grouped), None),
        "candidate_site_count": len(candidates),
        "intended_target_found": (
            intended_found if intended_target is not None else None
        ),
        "off_target_count": (
            len(off_targets) if intended_target is not None else None
        ),
        "exact_off_targets": (
            exact_count if intended_target is not None else None
        ),
        "mismatched_off_targets": (
            mismatched_count if intended_target is not None else None
        ),
        "forward_off_targets": (
            forward_count if intended_target is not None else None
        ),
        "reverse_off_targets": (
            reverse_count if intended_target is not None else None
        ),
        "mismatch_distribution": (
            dict(sorted(mismatch_distribution.items()))
            if intended_target is not None
            else None
        ),
        "specificity_score": specificity_score,
        "potential_off_targets": off_targets,
    }
