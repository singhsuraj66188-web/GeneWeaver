
"""Integrated CRISPR target search using guide RNA and PAM detection."""

from geneweaver.alignment import find_matches
from geneweaver.guide_rna import guide_rna_to_dna
from geneweaver.pam import find_pam_sites


def find_crispr_targets(
    reference: str,
    guide_rna: str,
    max_mismatches: int = 0,
    both_strands: bool = True,
    expected_guide_length: int = 20,
) -> list[dict]:
    """Find CRISPR targets with correctly positioned SpCas9 PAM sites.

    Coordinates are zero-based and end-exclusive.

    Forward strand:
        Guide match followed immediately by NGG.

    Reverse strand:
        CCN immediately precedes the guide match
        in the reference sequence.

    Reverse-strand PAM sequences are reported in NGG
    orientation.
    """

    guide_dna = guide_rna_to_dna(
        guide_rna,
        expected_length=expected_guide_length,
    )

    matches = find_matches(
        reference,
        guide_dna,
        max_mismatches=max_mismatches,
        both_strands=both_strands,
    )

    pam_sites = find_pam_sites(
        reference,
        both_strands=both_strands,
    )

    # Index PAM sites by their genomic coordinates and strand.
    pam_lookup = {
        (pam["start"], pam["end"], pam["strand"]): pam
        for pam in pam_sites
    }

    candidates = []

    for match in matches:
        strand = match["strand"]

        if strand == "+":
            pam_start = match["end"]
        else:
            pam_start = match["start"] - 3

        pam_end = pam_start + 3

        if pam_start < 0:
            continue

        pam = pam_lookup.get(
            (pam_start, pam_end, strand)
        )

        if pam is None:
            continue

        candidates.append({
            "start": match["start"],
            "end": match["end"],
            "strand": strand,
            "matched_sequence": match["matched_sequence"],
            "mismatches": match["mismatches"],
            "pam_start": pam["start"],
            "pam_end": pam["end"],
            "pam_sequence": pam["pam_sequence"],
            "guide_rna": guide_rna.strip().upper(),
            "guide_dna": guide_dna,
        })

    return sorted(
        candidates,
        key=lambda candidate: (
            candidate["start"],
            candidate["strand"],
        ),
    )
