"""Integration tests for CRISPR candidate ranking."""

from geneweaver.crispr_search import find_crispr_targets
from geneweaver.candidate_ranking import rank_crispr_candidates


GUIDE_RNA = "ACGUUGCAACGAUCGUACGA"
GUIDE_DNA = GUIDE_RNA.replace("U", "T")


def test_rank_real_crispr_search_candidates():
    """Exact matches should rank above candidates with mismatches."""

    mutated_guide = "T" + GUIDE_DNA[1:]

    reference = (
        mutated_guide + "AGG"
        + "AAAA"
        + GUIDE_DNA + "TGG"
    )

    candidates = find_crispr_targets(
        reference,
        GUIDE_RNA,
        max_mismatches=1,
        both_strands=False,
    )

    assert len(candidates) == 2

    ranked = rank_crispr_candidates(candidates)

    assert ranked[0]["mismatches"] == 0
    assert ranked[0]["start"] == 27
    assert ranked[0]["score"] == 100.0
    assert ranked[0]["rank"] == 1

    assert ranked[1]["mismatches"] == 1
    assert ranked[1]["start"] == 0
    assert ranked[1]["score"] == 90.0
    assert ranked[1]["rank"] == 2


def test_ranking_preserves_crispr_pam_information():
    """Ranking must preserve original PAM and guide information."""

    reference = GUIDE_DNA + "AGG"

    candidates = find_crispr_targets(reference, GUIDE_RNA)
    ranked = rank_crispr_candidates(candidates)

    assert ranked[0]["pam_sequence"] == "AGG"
    assert ranked[0]["pam_start"] == 20
    assert ranked[0]["pam_end"] == 23
    assert ranked[0]["guide_rna"] == GUIDE_RNA
    assert ranked[0]["guide_dna"] == GUIDE_DNA
    assert ranked[0]["matched_sequence"] == GUIDE_DNA


def test_ranking_preserves_reverse_strand_information():
    """Reverse-strand candidates must retain their original metadata."""

    reverse_target = GUIDE_DNA.translate(
        str.maketrans("ATGC", "TACG")
    )[::-1]

    reference = "CCA" + reverse_target

    candidates = find_crispr_targets(reference, GUIDE_RNA)
    ranked = rank_crispr_candidates(candidates)

    assert len(ranked) == 1
    assert ranked[0]["strand"] == "-"
    assert ranked[0]["start"] == 3
    assert ranked[0]["end"] == 23
    assert ranked[0]["pam_sequence"] == "TGG"
    assert ranked[0]["rank"] == 1
