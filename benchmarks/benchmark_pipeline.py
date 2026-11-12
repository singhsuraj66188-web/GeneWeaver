
import sys
import time
import statistics
import tempfile
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1] / "src")
)

from geneweaver.pipeline import process_fasta


def run_benchmark(sequence_length=1_000_000, repeats=3):
    sequence = "ATGC" * (sequence_length // 4)

    with tempfile.TemporaryDirectory() as temp_dir:
        fasta_file = Path(temp_dir) / "benchmark.fasta"

        fasta_file.write_text(
            f">benchmark_gene\n{sequence}\n",
            encoding="utf-8"
        )

        timings = []

        for run in range(repeats):
            start = time.perf_counter()

            records = process_fasta(
                fasta_file,
                chunk_size=1000
            )

            elapsed = time.perf_counter() - start
            timings.append(elapsed)

            print(
                f"Run {run + 1}: "
                f"{elapsed:.4f} seconds"
            )

        median_time = statistics.median(timings)

        throughput = sequence_length / median_time

        print("\n--- GeneWeaver Benchmark Results ---")
        print(f"Sequence length: {sequence_length:,} bases")
        print(f"Chunk size: 1000")
        print(f"Total chunks: {len(records[0]['chunks']):,}")
        print(f"Median processing time: {median_time:.4f} seconds")
        print(f"Throughput: {throughput:,.0f} bases/second")
        print(f"Throughput: {throughput / 1_000_000:.2f} MB/second")


if __name__ == "__main__":
    run_benchmark(sequence_length=5_000_000, repeats=5)
