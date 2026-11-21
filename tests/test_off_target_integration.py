
"""Integration tests for CRISPR search and off-target analysis."""

from geneweaver.crispr_search import find_crispr_targets
from geneweaver.off_target import analyze_off_targets


GUIDE_RNA = "ACGUUGCAACGAUCGUACGA"
GUIDE_DNA = GUIDE_RNA.replace("U", "T")


def test_crispr_search_integrates_with_off_target_analysis():
    # Create two exact target sites and one site with one mismatch.
    mutated_guide = "T" + GUIDE_DNA[1:]

    reference = (
        GUIDE_DNA + "AGG" +
        "AAA" +
        GUIDE_DNA + "TGG" +
        "AAA" +
        mutated_guide + "CGG"
    )

    # Step 1: Find CRISPR targets.
    candidates = find_crispr_targets(
        reference,
        GUIDE_RNA,
        max_mismatches=1,
        both_strands=False,
    )

    assert len(candidates) == 3

    # Step 2: Identify the first candidate as the intended target.
    intended_target = candidates[0]

    # Step 3: Analyze potential off-target sites.
    result = analyze_off_targets(
        candidates,
        intended_target=intended_target,
    )

    # Verify the complete integration result.
    assert result["guide_rna"] == GUIDE_RNA
    assert result["candidate_site_count"] == 3
    assert result["intended_target_found"] is True

    assert result["off_target_count"] == 2
    assert result["exact_off_targets"] == 1
    assert result["mismatched_off_targets"] == 1

    assert result["forward_off_targets"] == 2
    assert result["reverse_off_targets"] == 0

    assert result["mismatch_distribution"] == {
        0: 1,
        1: 1,
    }

    assert result["specificity_score"] == 40.0


def test_crispr_search_with_no_off_target_candidates():
    reference = GUIDE_DNA + "AGG"

    candidates = find_crispr_targets(
        reference,
        GUIDE_RNA,
        both_strands=False,
    )

    result = analyze_off_targets(
        candidates,
        intended_target=candidates[0],
    )

    assert result["intended_target_found"] is True
    assert result["off_target_count"] == 0
    assert result["exact_off_targets"] == 0
    assert result["mismatched_off_targets"] == 0
    assert result["specificity_score"] == 100.0
    assert result["potential_off_targets"] == []
