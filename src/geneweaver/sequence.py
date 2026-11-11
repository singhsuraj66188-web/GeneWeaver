"""DNA sequence validation utilities."""

VALID_NUCLEOTIDES = frozenset("ATGC")


def validate_dna_sequence(sequence: str) -> str:
    """Validate a DNA sequence and return its uppercase representation.

    Args:
        sequence: DNA sequence containing A, T, G, and C.

    Returns:
        Normalized uppercase DNA sequence.

    Raises:
        TypeError: If the input is not a string.
        ValueError: If the sequence is empty or contains invalid characters.
    """
    if not isinstance(sequence, str):
        raise TypeError("DNA sequence must be a string.")

    normalized = sequence.strip().upper()

    if not normalized:
        raise ValueError("DNA sequence cannot be empty.")

    invalid = set(normalized) - VALID_NUCLEOTIDES

    if invalid:
        raise ValueError(
            f"Invalid DNA nucleotides: {', '.join(sorted(invalid))}"
        )

    return normalized
