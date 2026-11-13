import pytest

from geneweaver.alignment import find_matches


def test_exact_forward_match():
    results = find_matches("TTACGAAA", "ACG", 0)

    assert len(results) == 1
    assert results[0]["start"] == 2
    assert results[0]["end"] == 5
    assert results[0]["strand"] == "+"
    assert results[0]["mismatches"] == 0


def test_reverse_strand_match():
    results = find_matches("CCGTTAA", "AAC", 0)

    assert len(results) == 1
    assert results[0]["start"] == 2
    assert results[0]["end"] == 5
    assert results[0]["strand"] == "-"
    assert results[0]["matched_sequence"] == "GTT"


def test_one_mismatch():
    results = find_matches("ATG", "ACG", 1, both_strands=False)

    assert len(results) == 1
    assert results[0]["mismatches"] == 1


def test_two_mismatches():
    results = find_matches("ATG", "AAC", 2, both_strands=False)

    assert len(results) == 1
    assert results[0]["mismatches"] == 2


def test_reject_excessive_mismatches():
    results = find_matches("ATG", "AAC", 1, both_strands=False)

    assert results == []


def test_target_longer_than_reference():
    assert find_matches("AT", "ATGC") == []


def test_no_match():
    assert find_matches("AAAA", "GGGG", 0) == []


def test_invalid_reference():
    with pytest.raises(ValueError):
        find_matches("ATGX", "ATG")


def test_invalid_target():
    with pytest.raises(ValueError):
        find_matches("ATGC", "ATX")


def test_negative_mismatch_limit():
    with pytest.raises(ValueError):
        find_matches("ATGC", "ATG", -1)


def test_invalid_mismatch_type():
    with pytest.raises(TypeError):
        find_matches("ATGC", "ATG", 1.5)


def test_boolean_mismatch_limit():
    with pytest.raises(TypeError):
        find_matches("ATGC", "ATG", True)


def test_invalid_both_strands_type():
    with pytest.raises(TypeError):
        find_matches("ATGC", "ATG", both_strands="yes")
