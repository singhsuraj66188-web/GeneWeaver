"""CRISPR PAM sequence detection utilities."""

from geneweaver.sequence import validate_dna_sequence
from geneweaver.sequence_utils import reverse_complement


def find_pam_sites(
    sequence: str,
    both_strands: bool = True,
) -> list[dict]:
    """Find SpCas9 NGG PAM sites in a DNA sequence.

    Coordinates are zero-based and end-exclusive.
    Forward strand: NGG
    Reverse strand: CCN
    """

    sequence = validate_dna_sequence(sequence)

    if not isinstance(both_strands, bool):
        raise TypeError("both_strands must be a boolean.")

    results = []

    for start in range(len(sequence) - 2):
        window = sequence[start:start + 3]

        if window[1:] == "GG":
            results.append({
                "start": start,
                "end": start + 3,
                "strand": "+",
                "pam_sequence": window,
            })

        if both_strands and window[:2] == "CC":
            results.append({
                "start": start,
                "end": start + 3,
                "strand": "-",
                "pam_sequence": reverse_complement(window),
            })

    return sorted(results, key=lambda match: (match["start"], match["strand"]))
