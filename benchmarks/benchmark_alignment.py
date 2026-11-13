"""Benchmark the GeneWeaver DNA alignment engine."""

import platform
import random
import statistics
import time

from geneweaver.alignment import find_matches


def generate_reference(size, target):
    """Generate deterministic DNA data containing a known target."""

    rng = random.Random(42)

    reference = "".join(
        rng.choices("ATGC", k=size)
    )

    position = size // 2

    reference = (
        reference[:position]
        + target
        + reference[position + len(target):]
    )

    return reference


def benchmark_alignment():
    target = "ATGCGTACGTAGCTAGCTAA"

    datasets = [
        ("Small", 10_000),
        ("Medium", 100_000),
        ("Large", 1_000_000),
    ]

    print("GeneWeaver DNA Alignment Benchmark")
    print("=" * 55)
    print(f"Python: {platform.python_version()}")
    print(f"Platform: {platform.system()}")
    print(f"Target length: {len(target)} bases")
    print("Strands: Forward and reverse")
    print("Runs per dataset: 3")
    print("-" * 55)

    for name, size in datasets:
        reference = generate_reference(size, target)

        timings = []
        match_count = 0

        for _ in range(3):
            start = time.perf_counter()

            results = find_matches(
                reference=reference,
                target=target,
                max_mismatches=0,
                both_strands=True,
            )

            elapsed = time.perf_counter() - start

            timings.append(elapsed)
            match_count = len(results)

        median_time = statistics.median(timings)
        throughput = size / median_time

        print(f"\nDataset: {name} ({size:,} bases)")
        print(f"Median time: {median_time:.6f} seconds")
        print(f"Matches found: {match_count}")
        print(f"Throughput: {throughput:,.0f} bases/second")

    print("\nBenchmark completed.")


if __name__ == "__main__":
    benchmark_alignment()
