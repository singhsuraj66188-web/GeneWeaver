
import pytest

from geneweaver import gpu_backend
from geneweaver.alignment import find_matches


CUDA_AVAILABLE = gpu_backend.is_cuda_available()

requires_cuda = pytest.mark.skipif(
    not CUDA_AVAILABLE,
    reason="CUDA device is not available",
)


@requires_cuda
def test_gpu_exact_forward_match():
    results = gpu_backend.find_matches_gpu(
        "TTACGAAA", "ACG", both_strands=False
    )

    assert len(results) == 1
    assert results[0]["start"] == 2
    assert results[0]["strand"] == "+"
    assert results[0]["mismatches"] == 0


@requires_cuda
def test_gpu_reverse_strand_match():
    results = gpu_backend.find_matches_gpu("CCGTTAA", "AAC")

    assert len(results) == 1
    assert results[0]["start"] == 2
    assert results[0]["strand"] == "-"
    assert results[0]["matched_sequence"] == "GTT"


@requires_cuda
def test_gpu_one_mismatch():
    results = gpu_backend.find_matches_gpu(
        "ATG", "ACG", max_mismatches=1, both_strands=False
    )

    assert len(results) == 1
    assert results[0]["mismatches"] == 1


@requires_cuda
def test_gpu_target_longer_than_reference():
    assert gpu_backend.find_matches_gpu("AT", "ATGC") == []


def test_gpu_empty_target_rejected():
    with pytest.raises(ValueError):
        gpu_backend.find_matches_gpu("ATGC", "")


def test_gpu_negative_mismatch_limit():
    with pytest.raises(ValueError):
        gpu_backend.find_matches_gpu("ATGC", "ATG", -1)


def test_gpu_invalid_mismatch_type():
    with pytest.raises(TypeError):
        gpu_backend.find_matches_gpu("ATGC", "ATG", 1.5)


def test_gpu_boolean_mismatch_limit():
    with pytest.raises(TypeError):
        gpu_backend.find_matches_gpu("ATGC", "ATG", True)


@requires_cuda
def test_cpu_gpu_result_parity():
    reference = "TTACGAAATGCATGC"
    target = "ACG"

    cpu_results = find_matches(
        reference, target, max_mismatches=1, both_strands=True
    )

    gpu_results = gpu_backend.find_matches_gpu(
        reference, target, max_mismatches=1, both_strands=True
    )

    assert gpu_results == cpu_results


def test_cuda_unavailable_raises_error(monkeypatch):
    monkeypatch.setattr(
        gpu_backend, "is_cuda_available", lambda: False
    )

    with pytest.raises(RuntimeError, match="CUDA is not available"):
        gpu_backend.find_matches_gpu("TTACGAAA", "ACG")
