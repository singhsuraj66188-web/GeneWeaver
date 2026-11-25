
"""Compare CPU and CUDA GPU DNA alignment performance."""

import platform
import random
import statistics
import time

from numba import cuda

from geneweaver.alignment import find_matches
from geneweaver import gpu_backend


def generate_reference(size, target):
    """Generate deterministic DNA data with a known target."""
    rng = random.Random(42)
    reference = "".join(rng.choices("ATGC", k=size))
    position = size // 2

    return (
        reference[:position]
        + target
        + reference[position + len(target):]
    )


def measure(function, runs=3):
    """Return median execution time and final results."""
    if not isinstance(runs, int) or isinstance(runs, bool) or runs < 1:
        raise ValueError("Runs must be a positive integer.")

    timings = []
    results = None

    for _ in range(runs):
        start = time.perf_counter()
        results = function()
        elapsed = time.perf_counter() - start
        timings.append(elapsed)

    return statistics.median(timings), results


def benchmark_cpu_gpu():
    target = "ATGCGTACGTAGCTAGCTAA"

    datasets = [
        ("Small", 10_000),
        ("Medium", 100_000),
        ("Large", 1_000_000),
    ]

    runs = 3

    print("GeneWeaver CPU vs GPU Alignment Benchmark")
    print("=" * 65)
    print(f"Python: {platform.python_version()}")
    print(f"Platform: {platform.system()}")
    print(f"CUDA available: {gpu_backend.is_cuda_available()}")

    if not gpu_backend.is_cuda_available():
        print("CUDA is unavailable. GPU benchmark cannot run.")
        return

    try:
        print(f"GPU device: {cuda.get_current_device().name}")

        print(f"Target length: {len(target)} bases")
        print(f"Runs per implementation: {runs}")
        print("Strands: Forward and reverse")
        print("-" * 65)

        # Compile and warm up the CUDA kernel.
        print("Warming up GPU...")
        gpu_backend.find_matches_gpu(
            "TTACGAAA",
            "ACG",
            both_strands=True,
        )

        for name, size in datasets:
            print(f"\n{name} dataset: {size:,} bases")

            reference = generate_reference(size, target)

            cpu_function = lambda: find_matches(
                reference,
                target,
                max_mismatches=0,
                both_strands=True,
            )

            gpu_function = lambda: gpu_backend.find_matches_gpu(
                reference,
                target,
                max_mismatches=0,
                both_strands=True,
            )

            # Verify identical results before measuring.
            cpu_results = cpu_function()
            gpu_results = gpu_function()

            if cpu_results != gpu_results:
                raise AssertionError(
                    f"CPU-GPU result mismatch for {size:,} bases"
                )

            print("Correctness: PASSED")

            cpu_time, _ = measure(cpu_function, runs)
            gpu_time, _ = measure(gpu_function, runs)

            cpu_throughput = size / cpu_time
            gpu_throughput = size / gpu_time
            speedup = cpu_time / gpu_time

            print(f"CPU median: {cpu_time:.6f} seconds")
            print(f"GPU median: {gpu_time:.6f} seconds")
            print(
                f"CPU throughput: "
                f"{cpu_throughput:,.0f} bases/second"
            )
            print(
                f"GPU throughput: "
                f"{gpu_throughput:,.0f} bases/second"
            )
            print(f"CPU/GPU time ratio: {speedup:.3f}x")

            if speedup > 1:
                print("Observation: GPU was faster for this dataset.")
            elif speedup < 1:
                print("Observation: CPU was faster for this dataset.")
            else:
                print("Observation: Equal median execution times.")

        print("\nBenchmark completed.")

    except Exception as exc:
        print(f"\nBenchmark failed: {exc}")
        raise


if __name__ == "__main__":
    benchmark_cpu_gpu()
