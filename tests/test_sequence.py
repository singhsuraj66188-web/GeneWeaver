import pytest

from geneweaver.sequence import validate_dna_sequence


@pytest.mark.parametrize(
    ("sequence", "expected"),
    [
        ("ATGC", "ATGC"),
        ("atgc", "ATGC"),
        ("  atgc  ", "ATGC"),
        ("AAAA", "AAAA"),
        ("GGGG", "GGGG"),
    ],
)
def test_valid_dna_sequences(sequence, expected):
    assert validate_dna_sequence(sequence) == expected


@pytest.mark.parametrize(
    "sequence",
    [
        "",
        "   ",
        "ATGX",
        "ATGCN",
        "1234",
    ],
)
def test_invalid_dna_sequences(sequence):
    with pytest.raises(ValueError):
        validate_dna_sequence(sequence)


@pytest.mark.parametrize(
    "sequence",
    [
        None,
        123,
        ["A", "T", "G", "C"],
    ],
)
def test_non_string_input(sequence):
    with pytest.raises(TypeError):
        validate_dna_sequence(sequence)