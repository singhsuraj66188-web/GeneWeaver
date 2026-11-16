import pytest

from geneweaver.guide_rna import (
    validate_guide_rna,
    guide_rna_to_dna,
    dna_to_guide_rna,
)


VALID_RNA = "AUGCAUGCAUGCAUGCAUGC"
VALID_DNA = "ATGCATGCATGCATGCATGC"


def test_validate_valid_guide_rna():
    assert validate_guide_rna(VALID_RNA) == VALID_RNA


def test_validate_lowercase_guide_rna():
    assert validate_guide_rna(VALID_RNA.lower()) == VALID_RNA


def test_validate_guide_rna_with_outer_whitespace():
    assert validate_guide_rna(f"  {VALID_RNA}  ") == VALID_RNA


def test_reject_empty_guide_rna():
    with pytest.raises(ValueError):
        validate_guide_rna("")


def test_reject_whitespace_only_guide_rna():
    with pytest.raises(ValueError):
        validate_guide_rna("   ")


@pytest.mark.parametrize("sequence", [
    "ATGCATGCATGCATGCATGC",
    "AUGCAUGCAUGCAUGCAUGX",
    "AUGCAUGCAUGCAUGCAUG1",
])
def test_reject_invalid_rna_nucleotides(sequence):
    with pytest.raises(ValueError):
        validate_guide_rna(sequence)


def test_reject_non_string_guide_rna():
    with pytest.raises(TypeError):
        validate_guide_rna(None)


def test_reject_incorrect_guide_length():
    with pytest.raises(ValueError):
        validate_guide_rna("AUGCAUGC")


def test_support_custom_guide_length():
    assert validate_guide_rna("AUGC", expected_length=4) == "AUGC"


def test_reject_invalid_expected_length_type():
    with pytest.raises(TypeError):
        validate_guide_rna(VALID_RNA, expected_length=True)


def test_reject_non_positive_expected_length():
    with pytest.raises(ValueError):
        validate_guide_rna(VALID_RNA, expected_length=0)


def test_convert_rna_to_dna():
    assert guide_rna_to_dna(VALID_RNA) == VALID_DNA


def test_convert_dna_to_rna():
    assert dna_to_guide_rna(VALID_DNA) == VALID_RNA


def test_dna_to_rna_supports_lowercase():
    assert dna_to_guide_rna(VALID_DNA.lower()) == VALID_RNA


def test_dna_to_rna_rejects_invalid_sequence():
    with pytest.raises(ValueError):
        dna_to_guide_rna("ATGCATGCATGCATGCATGN")


def test_dna_to_rna_rejects_incorrect_length():
    with pytest.raises(ValueError):
        dna_to_guide_rna("ATGC")


def test_rna_to_dna_rejects_invalid_sequence():
    with pytest.raises(ValueError):
        guide_rna_to_dna("ATGCATGCATGCATGCATGC")
