
"""Tests for integrated CRISPR target searching."""

import pytest

from geneweaver.crispr_search import find_crispr_targets
from geneweaver.sequence_utils import reverse_complement


GUIDE_RNA = "ACGUUGCAACGAUCGUACGA"
GUIDE_DNA = GUIDE_RNA.replace("U", "T")


def test_find_forward_strand_target_with_ngg_pam():
    reference = GUIDE_DNA + "AGG"

    results = find_crispr_targets(reference, GUIDE_RNA)

    assert len(results) == 1

    result = results[0]

    assert result["start"] == 0
    assert result["end"] == 20
    assert result["strand"] == "+"
    assert result["pam_start"] == 20
    assert result["pam_end"] == 23
    assert result["pam_sequence"] == "AGG"
    assert result["mismatches"] == 0


def test_find_reverse_strand_target_with_ccn_pam():
    reverse_target = reverse_complement(GUIDE_DNA)
    reference = "CCA" + reverse_target

    results = find_crispr_targets(reference, GUIDE_RNA)

    assert len(results) == 1

    result = results[0]

    assert result["start"] == 3
    assert result["end"] == 23
    assert result["strand"] == "-"
    assert result["pam_start"] == 0
    assert result["pam_end"] == 3
    assert result["pam_sequence"] == "TGG"
    assert result["mismatches"] == 0


def test_reject_guide_match_without_pam():
    reference = GUIDE_DNA + "TAA"

    results = find_crispr_targets(reference, GUIDE_RNA)

    assert results == []


def test_reject_pam_not_immediately_adjacent():
    reference = GUIDE_DNA + "A" + "AGG"

    results = find_crispr_targets(reference, GUIDE_RNA)

    assert results == []


def test_support_one_mismatch():
    mutated_guide = "T" + GUIDE_DNA[1:]
    reference = mutated_guide + "AGG"

    results = find_crispr_targets(
        reference,
        GUIDE_RNA,
        max_mismatches=1,
        both_strands=False,
    )

    assert len(results) == 1
    assert results[0]["mismatches"] == 1
    assert results[0]["strand"] == "+"


def test_reject_mismatch_above_configured_limit():
    mutated_guide = "T" + GUIDE_DNA[1:]
    reference = mutated_guide + "AGG"

    results = find_crispr_targets(
        reference,
        GUIDE_RNA,
        max_mismatches=0,
        both_strands=False,
    )

    assert results == []


def test_both_strands_disabled():
    reverse_target = reverse_complement(GUIDE_DNA)
    reference = "CCA" + reverse_target

    results = find_crispr_targets(
        reference,
        GUIDE_RNA,
        both_strands=False,
    )

    assert results == []


def test_invalid_guide_rna_is_rejected():
    with pytest.raises(ValueError):
        find_crispr_targets(
            GUIDE_DNA + "AGG",
            "INVALID",
        )


def test_invalid_reference_is_rejected():
    with pytest.raises(ValueError):
        find_crispr_targets(
            "INVALID",
            GUIDE_RNA,
        )


def test_custom_guide_length():
    guide = "AUGC"
    reference = "ATGCAGG"

    results = find_crispr_targets(
        reference,
        guide,
        expected_guide_length=4,
        both_strands=False,
    )

    assert len(results) == 1
    assert results[0]["start"] == 0
    assert results[0]["end"] == 4
    assert results[0]["pam_sequence"] == "AGG"


def test_result_contains_guide_information():
    reference = GUIDE_DNA + "AGG"

    results = find_crispr_targets(reference, GUIDE_RNA)

    assert results[0]["guide_rna"] == GUIDE_RNA
    assert results[0]["guide_dna"] == GUIDE_DNA
    assert results[0]["matched_sequence"] == GUIDE_DNA
