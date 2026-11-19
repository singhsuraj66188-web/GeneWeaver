import pytest

from geneweaver.candidate_ranking import (
    calculate_candidate_score,
    rank_crispr_candidates,
)


def make_candidate(start, mismatches, strand="+"):
    return {
        "start": start,
        "end": start + 20,
        "strand": strand,
        "mismatches": mismatches,
        "pam_sequence": "AGG",
    }


def test_exact_match_ranks_first():
    candidates = [
        make_candidate(10, 2),
        make_candidate(30, 0),
        make_candidate(50, 1),
    ]

    ranked = rank_crispr_candidates(candidates)

    assert ranked[0]["mismatches"] == 0
    assert ranked[0]["rank"] == 1


def test_candidate_scores():
    assert calculate_candidate_score(0) == 100.0
    assert calculate_candidate_score(1) == 90.0
    assert calculate_candidate_score(2) == 80.0


def test_candidates_are_sorted_by_score():
    candidates = [
        make_candidate(10, 3),
        make_candidate(20, 1),
        make_candidate(30, 0),
    ]

    ranked = rank_crispr_candidates(candidates)

    assert [item["score"] for item in ranked] == [
        100.0, 90.0, 70.0
    ]


def test_ties_are_sorted_by_position():
    candidates = [
        make_candidate(50, 0),
        make_candidate(10, 0),
        make_candidate(30, 0),
    ]

    ranked = rank_crispr_candidates(candidates)

    assert [item["start"] for item in ranked] == [10, 30, 50]


def test_strand_information_is_preserved():
    candidates = [
        make_candidate(10, 0, "-"),
        make_candidate(20, 0, "+"),
    ]

    ranked = rank_crispr_candidates(candidates)

    assert {item["strand"] for item in ranked} == {"+", "-"}


def test_genomic_coordinates_are_preserved():
    candidate = make_candidate(25, 0)

    ranked = rank_crispr_candidates([candidate])

    assert ranked[0]["start"] == 25
    assert ranked[0]["end"] == 45


def test_original_candidates_are_not_modified():
    candidate = make_candidate(10, 0)
    original = candidate.copy()

    rank_crispr_candidates([candidate])

    assert candidate == original


def test_empty_candidates():
    assert rank_crispr_candidates([]) == []


def test_rank_numbers_are_sequential():
    candidates = [
        make_candidate(10, 2),
        make_candidate(30, 0),
        make_candidate(50, 1),
    ]

    ranked = rank_crispr_candidates(candidates)

    assert [item["rank"] for item in ranked] == [1, 2, 3]


def test_invalid_mismatch_count():
    with pytest.raises(ValueError):
        calculate_candidate_score(-1)


def test_invalid_candidate_strand():
    candidate = make_candidate(10, 0, "?")

    with pytest.raises(ValueError):
        rank_crispr_candidates([candidate])


def test_invalid_coordinates():
    candidate = make_candidate(10, 0)
    candidate["end"] = 5

    with pytest.raises(ValueError):
        rank_crispr_candidates([candidate])


def test_missing_required_field():
    candidate = make_candidate(10, 0)
    del candidate["strand"]

    with pytest.raises(ValueError):
        rank_crispr_candidates([candidate])


def test_invalid_candidate_type():
    with pytest.raises(TypeError):
        rank_crispr_candidates(["invalid"])


def test_deterministic_ranking():
    candidates = [
        make_candidate(50, 1, "-"),
        make_candidate(10, 0, "+"),
        make_candidate(20, 0, "-"),
    ]

    first = rank_crispr_candidates(candidates)
    second = rank_crispr_candidates(candidates)

    assert first == second
