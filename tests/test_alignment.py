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


def test_overlapping_matches():
    results = find_matches("ATATAT", "ATA", both_strands=False)

    assert [match["start"] for match in results] == [0, 2]


def test_match_at_reference_start():
    results = find_matches("GATCC", "GAT", both_strands=False)

    assert len(results) == 1
    assert results[0]["start"] == 0
    assert results[0]["end"] == 3


def test_match_at_reference_end():
    results = find_matches("GATCC", "TCC", both_strands=False)

    assert len(results) == 1
    assert results[0]["start"] == 2
    assert results[0]["end"] == 5


def test_repeated_matches_preserve_position_order():
    results = find_matches("AAAAAA", "AA", both_strands=False)

    assert [match["start"] for match in results] == [0, 1, 2, 3, 4]


def test_palindromic_target_matches_both_strands():
    results = find_matches("AT", "AT")

    assert len(results) == 2
    assert [match["strand"] for match in results] == ["+", "-"]
    assert results[0]["start"] == results[1]["start"] == 0


def test_lowercase_and_outer_whitespace():
    results = find_matches("  ttacg  ", " acg ", both_strands=False)

    assert len(results) == 1
    assert results[0]["matched_sequence"] == "ACG"


def test_internal_whitespace_is_rejected():
    with pytest.raises(ValueError):
        find_matches("AT GC", "ATG")


def test_empty_reference_is_rejected():
    with pytest.raises(ValueError):
        find_matches("", "ATG")


def test_empty_target_is_rejected():
    with pytest.raises(ValueError):
        find_matches("ATGC", "")


def test_non_string_reference_is_rejected():
    with pytest.raises(TypeError):
        find_matches(None, "ATG")


def test_non_string_target_is_rejected():
    with pytest.raises(TypeError):
        find_matches("ATGC", None)


def test_reverse_match_excluded_when_both_strands_disabled():
    results = find_matches("CCGTTAA", "AAC", both_strands=False)

    assert results == []


def test_target_matches_entire_reference():
    results = find_matches("ATGC", "ATGC", both_strands=False)

    assert len(results) == 1
    assert results[0]["start"] == 0
    assert results[0]["end"] == 4
    assert results[0]["matched_sequence"] == "ATGC"
