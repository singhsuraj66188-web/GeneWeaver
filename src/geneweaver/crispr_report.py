
"""Statistical reporting utilities for CRISPR target search results."""

from collections import Counter
from typing import Any


def _validate_target(target: dict[str, Any], index: int) -> None:
    """Validate the required fields of an individual CRISPR target."""

    if not isinstance(target, dict):
        raise TypeError(f"Target at index {index} must be a dictionary.")

    required_fields = {
        "strand",
        "mismatches",
        "pam_sequence",
    }

    missing_fields = required_fields - target.keys()

    if missing_fields:
        raise ValueError(
            f"Target at index {index} is missing fields: "
            f"{', '.join(sorted(missing_fields))}"
        )

    if target["strand"] not in {"+", "-"}:
        raise ValueError(f"Invalid strand at target index {index}.")

    mismatches = target["mismatches"]

    if isinstance(mismatches, bool) or not isinstance(mismatches, int):
        raise TypeError("Mismatch count must be an integer.")

    if mismatches < 0:
        raise ValueError("Mismatch count cannot be negative.")

    pam = target["pam_sequence"]

    if not isinstance(pam, str) or len(pam) != 3:
        raise ValueError("PAM sequence must contain exactly 3 bases.")

    if set(pam.upper()) - set("ATGC"):
        raise ValueError("PAM sequence contains invalid DNA nucleotides.")


def summary_crispr_targets(
    targets: list[dict[str, Any]],
) -> dict[str, Any]:
    """Generate statistical summaries of CRISPR search results.

    The input is expected to contain dictionaries returned by
    geneweaver.crispr_search.find_crispr_targets.

    Returns total targets, strand counts, exact and mismatched
    matches, mismatch distribution, and PAM distribution.
    """

    if not isinstance(targets, list):
        raise TypeError("Targets must be provided as a list.")

    forward_count = 0
    reverse_count = 0
    exact_count = 0
    mismatched_count = 0

    mismatch_distribution: Counter[int] = Counter()
    pam_distribution: Counter[str] = Counter()

    for index, target in enumerate(targets):
        _validate_target(target, index)

        strand = target["strand"]
        mismatches = target["mismatches"]
        pam = target["pam_sequence"].upper()

        if strand == "+":
            forward_count += 1
        else:
            reverse_count += 1

        if mismatches == 0:
            exact_count += 1
        else:
            mismatched_count += 1

        mismatch_distribution[mismatches] += 1
        pam_distribution[pam] += 1

    return {
        "total_targets": len(targets),
        "forward_targets": forward_count,
        "reverse_targets": reverse_count,
        "exact_matches": exact_count,
        "mismatched_targets": mismatched_count,
        "mismatch_distribution": dict(sorted(mismatch_distribution.items())),
        "pam_distribution": dict(sorted(pam_distribution.items())),
    }
