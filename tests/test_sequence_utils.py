import pytest

from geneweaver.sequence_utils import reverse_complement


def test_reverse_complement_basic():
    assert reverse_complement("ATGC") == "GCAT"


def test_reverse_complement_lowercase():
    assert reverse_complement("aatg") == "CATT"


def test_reverse_complement_with_whitespace():
    assert reverse_complement(" ATGC ") == "GCAT"


def test_reverse_complement_invalid_sequence():
    with pytest.raises(ValueError):
        reverse_complement("ATGX")


def test_reverse_complement_empty_sequence():
    with pytest.raises(ValueError):
        reverse_complement("")
