
"""Optional CUDA-accelerated DNA sequence alignment backend."""

import numpy as np
from numba import cuda

from geneweaver.sequence import validate_dna_sequence
from geneweaver.sequence_utils import reverse_complement


# Encode DNA bases as integers.
_BASE_ENCODING = {
    "A": 0,
    "T": 1,
    "G": 2,
    "C": 3,
}


@cuda.jit
def _count_mismatches_kernel(reference, target, mismatch_counts):
    """Calculate mismatches for each possible alignment position."""

    position = cuda.grid(1)

    if position < mismatch_counts.size:
        mismatches = 0

        for index in range(target.size):
            if reference[position + index] != target[index]:
                mismatches += 1

        mismatch_counts[position] = mismatches


def is_cuda_available() -> bool:
    """Return whether a CUDA device is available."""

    try:
        return cuda.is_available()
    except Exception:
        return False


def find_matches_gpu(
    reference: str,
    target: str,
    max_mismatches: int = 0,
    both_strands: bool = True,
) -> list[dict]:
    """Find DNA alignment matches using CUDA.

    Raises RuntimeError if CUDA execution is unavailable or fails.
    """

    reference = validate_dna_sequence(reference)
    target = validate_dna_sequence(target)

    if not isinstance(max_mismatches, int) or isinstance(
        max_mismatches, bool
    ):
        raise TypeError("Maximum mismatches must be an integer.")

    if max_mismatches < 0:
        raise ValueError("Maximum mismatches cannot be negative.")

    if not isinstance(both_strands, bool):
        raise TypeError("both_strands must be a boolean.")

    if not is_cuda_available():
        raise RuntimeError("CUDA is not available.")

    if len(target) > len(reference):
        return []

    reference_array = np.array(
        [_BASE_ENCODING[base] for base in reference],
        dtype=np.int32,
    )

    strands = [("+", target)]

    if both_strands:
        strands.append(("-", reverse_complement(target)))

    results = []

    try:
        device_reference = cuda.to_device(reference_array)

        positions = len(reference) - len(target) + 1
        threads_per_block = 128
        blocks_per_grid = (
            positions + threads_per_block - 1
        ) // threads_per_block

        # Allocate GPU output memory once.
        device_counts = cuda.device_array(
            positions,
            dtype=np.int32,
        )

        for strand, query in strands:
            target_array = np.array(
                [_BASE_ENCODING[base] for base in query],
                dtype=np.int32,
            )

            device_target = cuda.to_device(target_array)

            _count_mismatches_kernel[
                blocks_per_grid, threads_per_block
            ](
                device_reference,
                device_target,
                device_counts,
            )

            counts = device_counts.copy_to_host()

            for start, mismatches in enumerate(counts):
                if mismatches <= max_mismatches:
                    results.append({
                        "start": start,
                        "end": start + len(target),
                        "strand": strand,
                        "matched_sequence": reference[
                            start:start + len(target)
                        ],
                        "mismatches": int(mismatches),
                    })

    except Exception as exc:
        raise RuntimeError(
            f"CUDA alignment execution failed: {exc}"
        ) from exc
    return results