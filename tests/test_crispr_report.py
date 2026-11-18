
"""Tests for CRISPR target summary and statistics."""

import pytest

from geneweaver.crispr_report import summary_crispr_targets


def make_target(strand="+", mismatches=0, pam="AGG"):
    """Create a representative CRISPR target result."""
    return {
        "start": 10,
        "end": 30,
        "strand": strand,
        "matched_sequence": "ACGTTGCAACGATCGTACGA",
        "mismatches": mismatches,
        "pam_sequence": pam,
        "pam_start": 30,
        "pam_end": 33,
        "guide_rna": "ACGUUGCAACGAUCGUACGA",
        "guide_dna": "ACGTTGCAACGATCGTACGA",
    }


def test_empty_target_list_returns_zero_counts():
    result = summary_crispr_targets([])

    assert result["total_targets"] == 0
    assert result["forward_targets"] == 0
    assert result["reverse_targets"] == 0
    assert result["exact_matches"] == 0
    assert result["mismatched_targets"] == 0
    assert result["mismatch_distribution"] == {}
    assert result["pam_distribution"] == {}


def test_summary_counts_forward_and_reverse_targets():
    targets = [
        make_target(strand="+"),
        make_target(strand="-"),
        make_target(strand="+"),
    ]

    result = summary_crispr_targets(targets)

    assert result["total_targets"] == 3
    assert result["forward_targets"] == 2
    assert result["reverse_targets"] == 1


def test_summary_separates_exact_and_mismatched_targets():
    targets = [
        make_target(mismatches=0),
        make_target(mismatches=1),
        make_target(mismatches=2),
        make_target(mismatches=0),
    ]

    result = summary_crispr_targets(targets)

    assert result["exact_matches"] == 2
    assert result["mismatched_targets"] == 2


def test_mismatch_distribution_counts_each_value():
    targets = [
        make_target(mismatches=0),
        make_target(mismatches=1),
        make_target(mismatches=1),
        make_target(mismatches=2),
        make_target(mismatches=2),
        make_target(mismatches=2),
    ]

    result = summary_crispr_targets(targets)

    assert result["mismatch_distribution"] == {
        0: 1,
        1: 2,
        2: 3,
    }


def test_pam_distribution_counts_sequences():
    targets = [
        make_target(pam="AGG"),
        make_target(pam="AGG"),
        make_target(pam="TGG"),
        make_target(pam="CGG"),
    ]

    result = summary_crispr_targets(targets)

    assert result["pam_distribution"] == {
        "AGG": 2,
        "CGG": 1,
        "TGG": 1,
    }


def test_pam_distribution_normalizes_case():
    targets = [
        make_target(pam="agg"),
        make_target(pam="AGG"),
    ]

    result = summary_crispr_targets(targets)

    assert result["pam_distribution"] == {"AGG": 2}


def test_non_list_input_raises_type_error():
    with pytest.raises(TypeError):
        summary_crispr_targets("not a list")


def test_missing_required_field_raises_value_error():
    target = make_target()
    del target["pam_sequence"]

    with pytest.raises(ValueError):
        summary_crispr_targets([target])


def test_invalid_strand_raises_value_error():
    with pytest.raises(ValueError):
        summary_crispr_targets([make_target(strand="unknown")])


def test_negative_mismatch_count_raises_value_error():
    with pytest.raises(ValueError):
        summary_crispr_targets([make_target(mismatches=-1)])


def test_non_integer_mismatch_count_raises_type_error():
    with pytest.raises(TypeError):
        summary_crispr_targets([make_target(mismatches=1.5)])


def test_invalid_pam_length_raises_value_error():
    with pytest.raises(ValueError):
        summary_crispr_targets([make_target(pam="AG")])


def test_invalid_pam_nucleotide_raises_value_error():
    with pytest.raises(ValueError):
        summary_crispr_targets([make_target(pam="AXG")])


def test_non_dictionary_target_raises_type_error():
    with pytest.raises(TypeError):
        summary_crispr_targets([None])
