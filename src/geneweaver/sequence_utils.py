"""DNA sequence utility functions."""

from geneweaver.sequence import validate_dna_sequence


def reverse_complement(sequence: str) -> str:
    """Return the reverse complement of a DNA sequence."""

    normalized = validate_dna_sequence(sequence)
    complement_table = str.maketrans("ATGC", "TACG")

    return normalized.translate(complement_table)[::-1]
