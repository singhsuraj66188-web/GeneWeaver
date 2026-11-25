
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

The current verification establishes GPU correctness. GPU performance
superiority requires separate benchmark measurements.

Future work will investigate:

Large-scale GPU alignment benchmarks.

CUDA kernel occupancy optimization.

GPU memory usage for large reference sequences.

Automatic CPU fallback integration.

Performance evaluation on larger DNA datasets.

## Conclusion

The initial CUDA alignment backend successfully executed
on the NVIDIA GeForce MX130.

All 10 dedicated GPU tests passed, including CPU-GPU
result parity verification. The complete project regression
suite also passed all 169 tests.

Subsequent CPU-versus-GPU benchmarking established measurable
GPU performance improvements across three tested dataset sizes.

---

## CUDA GPU Backend Verification

### Verification Environment

- Date: November 24, 2026
- Python: 3.12.10
- Platform: Windows
- GPU: NVIDIA GeForce MX130
- GPU Memory: 2 GB
- NVIDIA Driver: 581.83
- CUDA availability: Confirmed
- Backend: Numba CUDA

### Implementation

A CUDA-accelerated DNA alignment backend was implemented in:

`src/geneweaver/gpu_backend.py`

The backend includes:

- Integer encoding of DNA nucleotides.
- CUDA kernel for parallel mismatch counting.
- Exact DNA sequence matching.
- Reverse-strand alignment.
- Configurable mismatch tolerance.
- Zero-based, end-exclusive alignment coordinates.
- CUDA execution error handling.

### GPU Correctness Verification

The dedicated GPU test suite contains 10 tests.

| Verification | Result |
|---|---|
| Exact forward matching | PASSED |
| Reverse-strand matching | PASSED |
| One-mismatch matching | PASSED |
| Target longer than reference | PASSED |
| Empty target validation | PASSED |
| Negative mismatch validation | PASSED |
| Invalid mismatch type | PASSED |
| Boolean mismatch validation | PASSED |
| CPU-GPU result parity | PASSED |
| CUDA unavailable handling | PASSED |

GPU-specific test results:

- Tests passed: 10
- Tests failed: 0
- Execution time: 8.97 seconds

### Full Project Regression Testing

The complete GeneWeaver test suite was executed after
integrating the CUDA backend.

| Metric | Result |
|---|---:|
| Total tests | 169 |
| Passed | 169 |
| Failed | 0 |
| Skipped | 0 |
| Execution time | 8.51 seconds |

All existing CPU processing, FASTA parsing, CRISPR search,
PAM detection, candidate ranking, and off-target analysis
tests continued to pass.

### GPU Performance Observation

A Numba performance warning was observed during small
alignment tests:

`Grid size 1 will likely result in GPU under-utilization`

This warning indicates low GPU occupancy for small workloads.
It does not indicate a CUDA execution failure.

### Limitations and Future Improvements

The current verification establishes GPU correctness,
not GPU performance superiority.

Future work will investigate:

- Large-scale GPU alignment benchmarks.
- CPU versus GPU execution-time comparisons.
- CUDA kernel occupancy optimization.
- GPU memory usage for large reference sequences.
- Automatic CPU fallback integration.
- Performance evaluation on larger DNA datasets.

No GPU speedup claim is made at this verification stage.

### Conclusion

The initial CUDA alignment backend successfully executed
on the NVIDIA GeForce MX130.

All 10 dedicated GPU tests passed, including CPU-GPU
result parity verification. The complete project regression
suite also passed all 169 tests.

This establishes a working GPU acceleration foundation
for subsequent performance benchmarking and optimization.

CPU vs GPU Alignment Performance Benchmark

Benchmark Environment

Date: November 25, 2026

Python: 3.12.10

Platform: Windows

GPU: NVIDIA GeForce MX130

GPU Memory: 2 GB

NVIDIA Driver: 581.83

CUDA availability: Confirmed

Backend: Numba CUDA

Target sequence length: 20 bases

Search strands: Forward and reverse

Benchmark runs per implementation: 3

Statistical measurement: Median execution time

Reference generation: Deterministic random DNA (seed 42)

Benchmark Methodology

The CPU and GPU alignment implementations were evaluated
using three reference sequence sizes:

Small: 10,000 bases

Medium: 100,000 bases

Large: 1,000,000 bases

Both implementations performed forward and reverse-strand
alignment with zero allowed mismatches.

The CUDA kernel was warmed up before performance measurements
to exclude initial compilation overhead.

Each implementation was executed three times per dataset.
Median execution time was used for comparison.

CPU and GPU alignment results were compared before timing
to verify identical output.

Performance Results

Dataset Size

CPU Median (s)

GPU Median (s)

CPU Throughput (bases/s)

GPU Throughput (bases/s)

Speedup

10,000

0.035904

0.006486

278,522

1,541,687

5.535x

100,000

0.338533

0.038124

295,393

2,623,033

8.880x

1,000,000

3.217291

0.334021

310,820

2,993,822

9.632x

Correctness Verification

All three benchmark configurations successfully produced
identical CPU and GPU alignment results.

10,000-base dataset: PASSED

100,000-base dataset: PASSED

1,000,000-base dataset: PASSED

Forward-strand alignment: VERIFIED

Reverse-strand alignment: VERIFIED

Zero-mismatch matching: VERIFIED

No CPU-GPU result mismatches occurred.

Performance Analysis

GPU execution was faster across all three tested datasets.

The 10,000-base dataset achieved a 5.535x speedup.

The 100,000-base dataset achieved an 8.880x speedup.

The 1,000,000-base dataset achieved a 9.632x speedup.

GPU throughput increased to approximately 2.99 million
bases per second on the largest tested dataset.

CPU throughput remained approximately 279,000 to
311,000 bases per second.

The results indicate that GPU acceleration provides
increasing performance benefits as the tested reference
sequence size increases.

Performance Warnings and Limitations

Numba emitted GPU occupancy warnings for small CUDA grid sizes.

These warnings indicate that the GPU may not be fully utilized
for smaller workloads. They did not prevent successful
execution or correctness verification.

The measurements include GPU memory transfers and alignment
execution time. They represent local benchmark results on
the NVIDIA GeForce MX130 and are not production performance
guarantees.

Further evaluation is required for larger reference genomes,
different mismatch tolerances, and other GPU architectures.

Conclusion

The CPU-versus-GPU benchmark demonstrates that the GeneWeaver
CUDA alignment backend can outperform the existing CPU
alignment implementation across all three tested datasets.

The largest dataset achieved a measured speedup of 9.632x,
with GPU throughput reaching approximately 2.99 million
bases per second.

These measurements establish an initial performance baseline
for future GPU optimization and larger-scale genome alignment.
