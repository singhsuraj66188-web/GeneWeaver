
"""Benchmark GeneWeaver CRISPR target search performance."""

import platform
import random
import statistics
import time

from geneweaver.crispr_search import find_crispr_targets


GUIDE_RNA = "AUGCGUACGUAGCUAGCUAA"
GUIDE_DNA = "ATGCGTACGTAGCTAGCTAA"
PAM = "AGG"

RUNS = 5

DATASETS = [
    ("Small", 10_000),
    ("Medium", 100_000),
    ("Large", 1_000_000),
]


def generate_reference(size, mismatched=False):
    """Generate deterministic DNA containing a known CRISPR target."""

    if size < len(GUIDE_DNA) + len(PAM):
        raise ValueError("Reference size is too small.")

    rng = random.Random(42)

    reference = list(
        "".join(rng.choices("ATGC", k=size))
    )

    position = size // 2

    target = GUIDE_DNA

    if mismatched:
        target = "C" + GUIDE_DNA[1:]

    reference[position:position + len(target) + len(PAM)] = (
        target + PAM
    )

    return "".join(reference)


def run_benchmark(reference, max_mismatches):
    """Measure CRISPR search execution time."""

    timings = []
    candidates = []

    for _ in range(RUNS):
        start = time.perf_counter()

        results = find_crispr_targets(
            reference=reference,
            guide_rna=GUIDE_RNA,
            max_mismatches=max_mismatches,
            both_strands=True,
        )

        elapsed = time.perf_counter() - start

        timings.append(elapsed)
        candidates = results

    return statistics.median(timings), candidates


def benchmark_crispr_search():
    """Benchmark exact and mismatch-tolerant CRISPR searches."""

    print("=" * 75)
    print("GENEWEAVER CRISPR SEARCH PERFORMANCE BENCHMARK")
    print("=" * 75)

    print(f"Python version: {platform.python_version()}")
    print(f"Platform: {platform.platform()}")
    print(f"Guide RNA length: {len(GUIDE_RNA)} bases")
    print("PAM: NGG")
    print("Search strands: Forward and reverse")
    print(f"Runs per configuration: {RUNS}")

    print("-" * 75)

    for name, size in DATASETS:

        print(f"\nDATASET: {name} ({size:,} bases)")
        print("-" * 75)

        for mismatches in (0, 1):

            reference = generate_reference(
                size,
                mismatched=(mismatches == 1),
            )

            median_time, candidates = run_benchmark(
                reference,
                mismatches,
            )

            throughput = size / median_time

            expected_position = size // 2

            known_target_found = any(
                candidate["start"] == expected_position
                and candidate["mismatches"] == mismatches
                for candidate in candidates
            )

            print(
                f"\nMaximum mismatches: {mismatches}"
            )

            print(
                f"Candidates found: {len(candidates)}"
            )

            print(
                f"Median execution time: {median_time:.6f} seconds"
            )

            print(
                f"Throughput: {throughput:,.0f} bases/second"
            )

            if not known_target_found:
                raise RuntimeError(
                    f"Known target verification failed: "
                    f"{name}, mismatches={mismatches}"
                )

            print("Known target verification: PASSED")

    print("\n" + "=" * 75)
    print("CRISPR SEARCH BENCHMARK COMPLETED SUCCESSFULLY")
    print("=" * 75)


if __name__ == "__main__":
    benchmark_crispr_search()
