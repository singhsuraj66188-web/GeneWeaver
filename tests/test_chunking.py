import pytest

from geneweaver.chunking import chunk_sequence


def test_normal_chunking():
    assert chunk_sequence("ATGCGTAC", 4) == ["ATGC", "GTAC"]


def test_incomplete_final_chunk():
    assert chunk_sequence("ATGCGTA", 3) == ["ATG", "CGT", "A"]


def test_empty_sequence():
    assert chunk_sequence("", 4) == []


def test_single_chunk():
    assert chunk_sequence("ATGC", 10) == ["ATGC"]


def test_invalid_chunk_size():
    with pytest.raises(ValueError):
        chunk_sequence("ATGC", 0)


def test_negative_chunk_size():
    with pytest.raises(ValueError):
        chunk_sequence("ATGC", -2)


def test_non_integer_chunk_size():
    with pytest.raises(TypeError):
        chunk_sequence("ATGC", 2.5)


def test_non_string_sequence():
    with pytest.raises(TypeError):
        chunk_sequence(1234, 2)