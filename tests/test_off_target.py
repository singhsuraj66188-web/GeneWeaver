
import pytest

from geneweaver.off_target import (
    group_candidates_by_guide,
    analyze_off_targets,
)


def make_candidate(start, end, strand, mismatches, guide="ATGC"):
    return {
        "guide_rna": guide,
        "start": start,
        "end": end,
        "strand": strand,
        "mismatches": mismatches,
    }


def test_group_candidates_by_guide():
    candidates = [
        make_candidate(10, 14, "+", 0, "atgc"),
        make_candidate(20, 24, "-", 1, "ATGC"),
        make_candidate(30, 34, "+", 2, "GGGG"),
    ]

    grouped = group_candidates_by_guide(candidates)

    assert len(grouped["ATGC"]) == 2
    assert len(grouped["GGGG"]) == 1


def test_group_candidates_normalizes_guide():
    candidates = [
        make_candidate(10, 14, "+", 0, "atgc"),
        make_candidate(20, 24, "-", 1, " ATGC "),
    ]

    grouped = group_candidates_by_guide(candidates)

    assert "ATGC" in grouped
    assert len(grouped["ATGC"]) == 2


def test_group_candidates_rejects_invalid_input():
    with pytest.raises(TypeError):
        group_candidates_by_guide("invalid")


def test_analyze_off_targets_detects_intended_target():
    intended = make_candidate(10, 14, "+", 0)

    candidates = [
        intended,
        make_candidate(20, 24, "-", 1),
        make_candidate(30, 34, "+", 2),
    ]

    result = analyze_off_targets(candidates, intended)

    assert result["intended_target_found"] is True
    assert result["off_target_count"] == 2
    assert result["candidate_site_count"] == 3


def test_analyze_off_targets_counts_exact_and_mismatched():
    intended = make_candidate(10, 14, "+", 0)

    candidates = [
        intended,
        make_candidate(20, 24, "+", 0),
        make_candidate(30, 34, "-", 1),
        make_candidate(40, 44, "+", 2),
    ]

    result = analyze_off_targets(candidates, intended)

    assert result["exact_off_targets"] == 1
    assert result["mismatched_off_targets"] == 2


def test_analyze_off_targets_counts_strands():
    intended = make_candidate(10, 14, "+", 0)

    candidates = [
        intended,
        make_candidate(20, 24, "+", 1),
        make_candidate(30, 34, "-", 1),
    ]

    result = analyze_off_targets(candidates, intended)

    assert result["forward_off_targets"] == 1
    assert result["reverse_off_targets"] == 1


def test_analyze_off_targets_calculates_specificity_score():
    intended = make_candidate(10, 14, "+", 0)

    candidates = [
        intended,
        make_candidate(20, 24, "-", 0),
    ]

    result = analyze_off_targets(candidates, intended)

    assert result["specificity_score"] == 50.0


def test_analyze_off_targets_without_intended_target():
    candidates = [
        make_candidate(10, 14, "+", 0),
        make_candidate(20, 24, "-", 1),
    ]

    result = analyze_off_targets(candidates)

    assert result["specificity_score"] is None
    assert result["off_target_count"] is None
    assert len(result["potential_off_targets"]) == 2


def test_analyze_off_targets_rejects_multiple_guides():
    candidates = [
        make_candidate(10, 14, "+", 0, "ATGC"),
        make_candidate(20, 24, "-", 1, "GGGG"),
    ]

    with pytest.raises(ValueError):
        analyze_off_targets(candidates)


def test_analyze_off_targets_rejects_invalid_strand():
    candidates = [
        make_candidate(10, 14, "invalid", 0),
    ]

    with pytest.raises(ValueError):
        analyze_off_targets(candidates)


def test_analyze_off_targets_handles_empty_candidates():
    result = analyze_off_targets([])

    assert result["guide_rna"] is None
    assert result["candidate_site_count"] == 0
    assert result["off_target_count"] is None
    assert result["potential_off_targets"] == []


def test_analyze_off_targets_rejects_missing_candidate_fields():
    candidates = [
        {
            "guide_rna": "ATGC",
            "start": 10,
            "end": 14,
            "strand": "+",
        }
    ]

    with pytest.raises(ValueError, match="mismatches"):
        analyze_off_targets(candidates)


def test_analyze_off_targets_rejects_negative_mismatches():
    candidates = [
        make_candidate(10, 14, "+", -1),
    ]

    with pytest.raises(ValueError, match="Mismatch count"):
        analyze_off_targets(candidates)


def test_analyze_off_targets_rejects_invalid_coordinate_types():
    candidates = [
        make_candidate(True, 14, "+", 0),
    ]

    with pytest.raises(TypeError, match="start"):
        analyze_off_targets(candidates)


def test_analyze_off_targets_rejects_invalid_intended_coordinates():
    intended = make_candidate(-1, 14, "+", 0)
    candidates = [
        make_candidate(10, 14, "+", 0),
    ]

    with pytest.raises(ValueError, match="coordinates"):
        analyze_off_targets(candidates, intended)


def test_group_candidates_rejects_empty_guide_rna():
    candidates = [
        make_candidate(10, 14, "+", 0, "   "),
    ]

    with pytest.raises(ValueError, match="guide RNA"):
        group_candidates_by_guide(candidates)

