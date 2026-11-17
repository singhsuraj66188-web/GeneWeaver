"""Benchmark the complete GeneWeaver CRISPR search pipeline."""

import platform
import random
import statistics
import time

from geneweaver.crispr_search import find_crispr_targets


GUIDE_RNA = "AUGCGUACGUAGCUAGCUAA"
GUIDE_DNA = "ATGCGTACGTAGCTAGCTAA"
PAM = "AGG"
RUNS = 3


def generate_reference(size):
    """Generate deterministic DNA containing a known CRISPR target."""

    if size < len(GUIDE_DNA) + len(PAM):
        raise ValueError("Reference size is too small.")

    rng = random.Random(42)

    reference = list(
        "".join(rng.choices("ATGC", k=size))
    )

    position = size // 2

    reference[position:position + len(GUIDE_DNA) + len(PAM)] = (
        GUIDE_DNA + PAM
    )

    return "".join(reference)


def benchmark_crispr_search():
    datasets = [
        ("Small", 10_000),
        ("Medium", 100_000),
        ("Large", 1_000_000),
    ]

    print("=" * 65)
    print("GENEWEAVER CRISPR SEARCH PERFORMANCE BENCHMARK")
    print("=" * 65)
    print(f"Python version: {platform.python_version()}")
    print(f"Platform: {platform.platform()}")
    print(f"Guide RNA length: {len(GUIDE_RNA)} bases")
    print("PAM: NGG")
    print("Search strands: Forward and reverse")
    print(f"Runs per dataset: {RUNS}")
    print("-" * 65)

    for name, size in datasets:
        reference = generate_reference(size)

        timings = []
        results = []

        for _ in range(RUNS):
            start = time.perf_counter()

            candidates = find_crispr_targets(
                reference=reference,
                guide_rna=GUIDE_RNA,
                max_mismatches=0,
                both_strands=True,
            )

            elapsed = time.perf_counter() - start

            timings.append(elapsed)
            results = candidates

        median_time = statistics.median(timings)
        throughput = size / median_time

        print(f"\nDataset: {name}")
        print(f"Reference size: {size:,} bases")
        print(f"Candidates found: {len(results)}")
        print(f"Median execution time: {median_time:.6f} seconds")
        print(f"Throughput: {throughput:,.0f} bases/second")

        if not results:
            raise RuntimeError(
                f"Known CRISPR target was not detected in {name} dataset."
            )

        print("Known target verification: PASSED")

    print("\n" + "=" * 65)
    print("CRISPR BENCHMARK COMPLETED SUCCESSFULLY")
    print("=" * 65)


if __name__ == "__main__":
    benchmark_crispr_search()
