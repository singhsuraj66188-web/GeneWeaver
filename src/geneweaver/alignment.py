"""Basic CPU-based DNA sequence alignment."""

from geneweaver.sequence import validate_dna_sequence
from geneweaver.sequence_utils import reverse_complement


def find_matches(
    reference: str,
    target: str,
    max_mismatches: int = 0,
    both_strands: bool = True,
) -> list[dict]:
    """Find target matches in a reference DNA sequence.

    Coordinates are zero-based and end-exclusive.
    """

    reference = validate_dna_sequence(reference)
    target = validate_dna_sequence(target)

    if not isinstance(max_mismatches, int) or isinstance(max_mismatches, bool):
        raise TypeError("Maximum mismatches must be an integer.")

    if max_mismatches < 0:
        raise ValueError("Maximum mismatches cannot be negative.")

    if not isinstance(both_strands, bool):
        raise TypeError("both_strands must be a boolean.")

    if len(target) > len(reference):
        return []

    strands = [("+", target)]

    if both_strands:
        strands.append(("-", reverse_complement(target)))

    results = []

    for strand, query in strands:
        for start in range(len(reference) - len(target) + 1):
            window = reference[start:start + len(query)]

            mismatches = sum(
                base_a != base_b
                for base_a, base_b in zip(window, query)
            )

            if mismatches <= max_mismatches:
                results.append({
                    "start": start,
                    "end": start + len(target),
                    "strand": strand,
                    "matched_sequence": window,
                    "mismatches": mismatches,
                })

    return results
