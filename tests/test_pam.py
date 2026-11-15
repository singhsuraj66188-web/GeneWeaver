from builtins import len

import pytest

from geneweaver.pam import find_pam_sites


def test_detect_forward_ngg_pam():
    results = find_pam_sites("ATGCAAGG")

    assert len(results) == 1
    assert results[0] == {
        "start": 5,
        "end": 8,
        "strand": "+",
        "pam_sequence": "AGG",
    }


def test_detect_reverse_ccn_pam():
    results = find_pam_sites("ATGCCAT")

    assert len(results) == 1
    assert results[0] == {
        "start": 3,
        "end": 6,
        "strand": "-",
        "pam_sequence": "TGG",
    }


def test_detect_multiple_pam_sites():
    results = find_pam_sites("AGGATGG")

    assert len(results) == 2
    assert [result["start"] for result in results] == [0, 4]


def test_both_strands_disabled():
    results = find_pam_sites("ATGCCAT", both_strands=False)

    assert results == []


def test_detect_pam_at_sequence_start():
    results = find_pam_sites("AGGATC")

    assert results[0]["start"] == 0


def test_detect_pam_at_sequence_end():
    results = find_pam_sites("ATCAGG")

    assert results[0]["start"] == 3
    assert results[0]["end"] == 6


def test_lowercase_sequence():
    results = find_pam_sites("atcagg")

    assert results[0]["pam_sequence"] == "AGG"


def test_no_pam_sites():
    assert find_pam_sites("ATATATA") == []


def test_empty_sequence_rejected():
    with pytest.raises(ValueError):
        find_pam_sites("")


def test_invalid_sequence_rejected():
    with pytest.raises(ValueError):
        find_pam_sites("ATGXGG")


def test_non_string_sequence_rejected():
    with pytest.raises(TypeError):
        find_pam_sites(None)


def test_invalid_both_strands_type():
    with pytest.raises(TypeError):
        find_pam_sites("ATCAGG", both_strands="yes")


def test_forward_pam_detected_when_both_strands_disabled():
    results = find_pam_sites("ATCAGG", both_strands=False)

    assert len(results) == 1
    assert results[0]["strand"] == "+"
    assert results[0]["pam_sequence"] == "AGG"