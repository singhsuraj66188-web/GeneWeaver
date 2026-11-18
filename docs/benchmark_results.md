
# GeneWeaver Benchmark Results

## Environment
- Python: 3.12.10
- BioPython: 1.88
- Platform: Windows
- Chunk size: 1000 bases

## Results

| Sequence Size | Median Time | Throughput | Chunks |
|---|---:|---:|---:|
| 1 million bases | 0.0163 s | 61.24 MB/s | 1,000 |
| 5 million bases | 0.0818 s | 61.14 MB/s | 5,000 |

## Analysis

- Throughput remained approximately constant.
- Processing time scaled approximately linearly.
- The pipeline successfully processed five million DNA bases.
- These are initial local benchmark measurements, not production performance guarantees.

## Conclusion

The current GeneWeaver pipeline demonstrates consistent
processing throughput across the tested sequence sizes.


---

## CRISPR Search Performance Benchmark

### Benchmark Environment

- Date: November 18, 2026
- Python: 3.12.10
- Platform: Windows 10
- Guide RNA length: 20 bases
- PAM configuration: SpCas9 NGG
- Search strands: Forward and reverse
- Benchmark runs per configuration: 5
- Statistical measurement: Median execution time
- Reference generation: Deterministic random DNA (seed 42)

### Benchmark Methodology

The CRISPR search implementation was evaluated using three
reference sequence sizes:

- Small: 10,000 bases
- Medium: 100,000 bases
- Large: 1,000,000 bases

Two search configurations were evaluated:

1. Exact matching with zero allowed mismatches.
2. Mismatch-tolerant matching with one allowed mismatch.

Each configuration was executed five times. Median execution
time was calculated to reduce the influence of individual
execution-time variations.

A known CRISPR target with a valid NGG PAM was inserted into
each reference sequence to verify search correctness.

### Performance Results

| Reference Size | Max Mismatches | Median Time (s) | Throughput (bases/s) |
|---|---:|---:|---:|
| 10,000 | 0 | 0.037996 | 263,188 |
| 10,000 | 1 | 0.037009 | 270,202 |
| 100,000 | 0 | 0.349844 | 285,842 |
| 100,000 | 1 | 0.364376 | 274,442 |
| 1,000,000 | 0 | 3.487747 | 286,718 |
| 1,000,000 | 1 | 3.404925 | 293,692 |

### Correctness Verification

All six benchmark configurations successfully detected the
known CRISPR target.

- Exact matching: PASSED
- One-mismatch matching: PASSED
- Forward and reverse strand search enabled.
- PAM validation: PASSED
- No benchmark configuration failed.

Each configuration returned one candidate containing the
expected target position and mismatch count.

### Performance Analysis

- Search throughput remained relatively consistent across
  the tested reference sizes.
- The implementation achieved approximately 263,000 to
  294,000 bases per second.
- The one-million-base reference required approximately
  3.4 to 3.5 seconds per search.
- Execution time increased approximately linearly with
  reference sequence size.
- No consistent performance difference was observed
  between exact and one-mismatch search configurations.

### Limitations and Future Improvements

The current CRISPR search implementation uses a CPU-based
Python alignment approach.

Future optimization will investigate:

- Numba JIT compilation.
- GPU acceleration using CUDA-compatible kernels.
- Reduced Python-level iteration overhead.
- Larger reference genome benchmarks.
- Comparison between CPU and GPU execution times.

The current measurements represent local CPU benchmark
results and are not production performance guarantees.

### Conclusion

The CRISPR search benchmark demonstrates that GeneWeaver
can successfully identify guide RNA targets with valid
PAM sequences across reference sequences up to one million
bases.

The results establish an initial CPU performance baseline
for evaluating future GPU acceleration and optimization.
