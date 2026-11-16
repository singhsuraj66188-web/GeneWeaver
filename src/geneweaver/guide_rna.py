"""Guide RNA validation and processing utilities."""

from geneweaver.sequence import validate_dna_sequence

VALID_RNA_NUCLEOTIDES = frozenset("ACGU")
DEFAULT_GUIDE_LENGTH = 20


def validate_guide_rna(
    sequence: str,
    expected_length: int = DEFAULT_GUIDE_LENGTH,
) -> str:
    """Validate an RNA guide spacer and return uppercase RNA."""

    if not isinstance(sequence, str):
        raise TypeError("Guide RNA sequence must be a string.")

    if isinstance(expected_length, bool) or not isinstance(expected_length, int):
        raise TypeError("Expected guide length must be an integer.")

    if expected_length <= 0:
        raise ValueError("Expected guide length must be positive.")

    normalized = sequence.strip().upper()

    if not normalized:
        raise ValueError("Guide RNA sequence cannot be empty.")

    invalid = set(normalized) - VALID_RNA_NUCLEOTIDES

    if invalid:
        raise ValueError(
            f"Invalid RNA nucleotides: {', '.join(sorted(invalid))}"
        )

    if len(normalized) != expected_length:
        raise ValueError(
            f"Guide RNA must contain exactly {expected_length} nucleotides."
        )

    return normalized


def guide_rna_to_dna(
    sequence: str,
    expected_length: int = DEFAULT_GUIDE_LENGTH,
) -> str:
    """Convert a validated RNA guide spacer into DNA representation."""

    normalized = validate_guide_rna(sequence, expected_length)
    return normalized.replace("U", "T")


def dna_to_guide_rna(
    sequence: str,
    expected_length: int = DEFAULT_GUIDE_LENGTH,
) -> str:
    """Convert a DNA guide spacer into RNA representation."""

    normalized = validate_dna_sequence(sequence)

    if isinstance(expected_length, bool) or not isinstance(expected_length, int):
        raise TypeError("Expected guide length must be an integer.")

    if expected_length <= 0:
        raise ValueError("Expected guide length must be positive.")

    if len(normalized) != expected_length:
        raise ValueError(
            f"Guide sequence must contain exactly {expected_length} nucleotides."
        )

    return normalized.replace("T", "U")
