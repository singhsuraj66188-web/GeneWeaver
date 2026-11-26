
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


def measure(function, runs=7):
    """Return median, minimum, maximum execution times and results."""
    if not isinstance(runs, int) or isinstance(runs, bool) or runs < 1:
        raise ValueError("Runs must be a positive integer.")

    timings = []
    results = None

    for _ in range(runs):
        start = time.perf_counter()
        results = function()
        elapsed = time.perf_counter() - start
        timings.append(elapsed)

    return {
        "median": statistics.median(timings),
        "minimum": min(timings),
        "maximum": max(timings),
        "results": results,
    }


def benchmark_cpu_gpu():
    target = "ATGCGTACGTAGCTAGCTAA"

    datasets = [
        ("Small", 10_000),
        ("Medium", 100_000),
        ("Large", 1_000_000),
    ]

    runs = 7
    warmup_runs = 2

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
        print(f"Measurement runs: {runs}")
        print(f"Warm-up runs per implementation: {warmup_runs}")
        print("Strands: Forward and reverse")
        print("-" * 65)

        benchmark_results = []

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

            # Warm up both implementations on this dataset.
            for _ in range(warmup_runs):
                cpu_function()
                gpu_function()

            print("CPU and GPU warm-up: COMPLETED")

            # Collect repeated measurements.
            cpu_measurements = measure(cpu_function, runs)
            gpu_measurements = measure(gpu_function, runs)

            cpu_time = cpu_measurements["median"]
            gpu_time = gpu_measurements["median"]

            cpu_throughput = size / cpu_time
            gpu_throughput = size / gpu_time
            speedup = cpu_time / gpu_time

            print("\nCPU measurements:")
            print(f"  Median: {cpu_time:.6f} seconds")
            print(
                f"  Minimum: "
                f"{cpu_measurements['minimum']:.6f} seconds"
            )
            print(
                f"  Maximum: "
                f"{cpu_measurements['maximum']:.6f} seconds"
            )
            print(f"  Throughput: {cpu_throughput:,.0f} bases/second")

            print("\nGPU measurements:")
            print(f"  Median: {gpu_time:.6f} seconds")
            print(
                f"  Minimum: "
                f"{gpu_measurements['minimum']:.6f} seconds"
            )
            print(
                f"  Maximum: "
                f"{gpu_measurements['maximum']:.6f} seconds"
            )
            print(f"  Throughput: {gpu_throughput:,.0f} bases/second")

            print(f"\nCPU/GPU time ratio: {speedup:.3f}x")

            if speedup > 1:
                print("Observation: GPU was faster for this dataset.")
            elif speedup < 1:
                print("Observation: CPU was faster for this dataset.")
            else:
                print("Observation: Equal median execution times.")

            benchmark_results.append({
                "dataset": name,
                "size": size,
                "cpu": cpu_measurements,
                "gpu": gpu_measurements,
                "speedup": speedup,
            })

        print("\nBenchmark completed successfully.")

    except Exception as exc:
        print(f"\nBenchmark failed: {exc}")
        raise


if __name__ == "__main__":
    benchmark_cpu_gpu()
