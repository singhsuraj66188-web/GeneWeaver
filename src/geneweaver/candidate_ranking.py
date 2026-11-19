"""Candidate ranking utilities for CRISPR target search results."""

from typing import Any


def _validate_candidate(
    candidate: dict[str, Any],
    index: int,
) -> None:
    """Validate the fields required for candidate ranking."""

    if not isinstance(candidate, dict):
        raise TypeError(
            f"Candidate at index {index} must be a dictionary."
        )

    required_fields = {"start", "end", "strand", "mismatches"}
    missing_fields = required_fields - candidate.keys()

    if missing_fields:
        raise ValueError(
            f"Candidate at index {index} is missing fields: "
            f"{', '.join(sorted(missing_fields))}"
        )

    if candidate["strand"] not in {"+", "-"}:
        raise ValueError(f"Invalid strand at candidate index {index}.")

    start = candidate["start"]
    end = candidate["end"]
    mismatches = candidate["mismatches"]

    for field, value in (
        ("start", start),
        ("end", end),
        ("mismatches", mismatches),
    ):
        if isinstance(value, bool) or not isinstance(value, int):
            raise TypeError(f"Candidate {field} must be an integer.")

    if start < 0:
        raise ValueError("Candidate start cannot be negative.")

    if end <= start:
        raise ValueError("Candidate end must be greater than start.")

    if mismatches < 0:
        raise ValueError("Mismatch count cannot be negative.")


def calculate_candidate_score(mismatches: int) -> float:
    """Calculate a heuristic candidate score from mismatch count."""

    if isinstance(mismatches, bool) or not isinstance(mismatches, int):
        raise TypeError("Mismatch count must be an integer.")

    if mismatches < 0:
        raise ValueError("Mismatch count cannot be negative.")

    return 100.0 - (mismatches * 10.0)


def rank_crispr_candidates(
    candidates: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Rank CRISPR candidates by mismatch-based heuristic score.

    Higher scores rank first. Ties are resolved by genomic start,
    genomic end, and strand to ensure deterministic ordering.

    Original candidate dictionaries are not modified.
    """

    if not isinstance(candidates, list):
        raise TypeError("Candidates must be provided as a list.")

    ranked_candidates = []

    for index, candidate in enumerate(candidates):
        _validate_candidate(candidate, index)

        ranked = candidate.copy()
        ranked["score"] = calculate_candidate_score(
            candidate["mismatches"]
        )
        ranked_candidates.append(ranked)

    ranked_candidates.sort(
        key=lambda candidate: (
            -candidate["score"],
            candidate["start"],
            candidate["end"],
            candidate["strand"],
        )
    )

    for rank, candidate in enumerate(ranked_candidates, start=1):
        candidate["rank"] = rank

    return ranked_candidates
