
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

## November 26, 2026 — Repeated CPU vs GPU Benchmark

### Benchmark Configuration

Hardware: NVIDIA GeForce MX130 (2 GB VRAM)

Python: 3.12.10

Operating system: Windows

Target sequence length: 20 bases

Strands tested: Forward and reverse

Measurement runs: 7 per implementation and dataset

Warm-up runs: 2 per implementation and dataset

Primary measurement: Median execution time

Additional measurements: Minimum and maximum execution times

The benchmark used the existing CPU alignment implementation and
CUDA GPU alignment backend. Both implementations were warmed up
before collecting measurements.

### Performance Results

| Dataset | Reference Size | CPU Median (s) | GPU Median (s) | CPU Min (s) | CPU Max (s) | GPU Min (s) | GPU Max (s) | Speedup |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Small | 10,000 | 0.035026 | 0.007210 | 0.032210 | 0.051573 | 0.006156 | 0.007782 | 4.858x |
| Medium | 100,000 | 0.368436 | 0.038891 | 0.359168 | 0.388628 | 0.036762 | 0.042112 | 9.473x |
| Large | 1,000,000 | 4.176174 | 0.363920 | 3.413645 | 6.275112 | 0.346935 | 0.754989 | 11.476x |

### Throughput Results

| Dataset | CPU Throughput (bases/second) | GPU Throughput (bases/second) |
|---|---:|---:|
| 10,000 | 285,503 | 1,387,001 |
| 100,000 | 271,418 | 2,571,269 |
| 1,000,000 | 239,454 | 2,747,856 |

### Correctness Verification

All three benchmark configurations successfully produced identical
CPU and GPU alignment results.

10,000-base dataset: PASSED

100,000-base dataset: PASSED

1,000,000-base dataset: PASSED

Forward-strand alignment: VERIFIED

Reverse-strand alignment: VERIFIED

Zero-mismatch matching: VERIFIED

No CPU-GPU result mismatches occurred.

### Performance Analysis

GPU execution was faster across all three tested datasets.

The 10,000-base dataset achieved a 4.858x speedup.

The 100,000-base dataset achieved a 9.473x speedup.

The 1,000,000-base dataset achieved an 11.476x speedup.

GPU throughput reached approximately 2.75 million bases per second
on the largest tested dataset.

CPU throughput ranged from approximately 239,454 to 285,503
bases per second.

The results show increasing GPU performance advantages across
the tested reference sizes.

The largest dataset showed greater variation between minimum
and maximum execution times than the smaller datasets.
Median execution time is therefore retained as the primary
comparison metric.

### Benchmark Warnings and Limitations

Numba emitted a GPU occupancy warning for the small dataset.
This warning indicates that the GPU may not be fully utilized
for smaller workloads. It did not affect successful execution
or correctness verification.

The measurements include GPU memory transfers and alignment
execution time. They represent local benchmark results on the
NVIDIA GeForce MX130 and are not production performance guarantees.

Only three reference sizes and a 20-base target sequence were
evaluated. Further testing is required for larger reference
genomes, different mismatch tolerances, and other GPU architectures.

### Conclusion

The repeated CPU-versus-GPU benchmark confirms that the
GeneWeaver CUDA alignment backend outperformed the CPU
implementation across all three tested datasets.

The largest dataset achieved a measured speedup of 11.476x,
with GPU throughput reaching approximately 2.75 million
bases per second.

Using seven measurement runs, two warm-up runs, and minimum,
maximum, and median execution times provides a more detailed
performance baseline for future optimization.

---

## GPU Output Buffer Reuse Benchmark — November 26, 2026

### Benchmark Environment

| Configuration | Value |
|---|---|
| Python | 3.12.10 |
| Operating System | Windows |
| GPU | NVIDIA GeForce MX130 |
| CUDA availability | True |
| Target sequence length | 20 bases |
| Strands | Forward and reverse |
| Measurement runs | 7 |
| Warm-up runs | 2 |
| Primary measurement | Median execution time |

This benchmark evaluates the GPU alignment backend after modifying
the output-buffer allocation strategy.

The GPU output buffer is allocated once per alignment call and
reused for forward and reverse-strand processing.

CPU and GPU results were compared before performance measurements.

### Performance Results

| Dataset | Reference Size | CPU Median (s) | GPU Median (s) | CPU Min (s) | CPU Max (s) | GPU Min (s) | GPU Max (s) | Speedup |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Small | 10,000 | 0.040243 | 0.005157 | 0.035683 | 0.051458 | 0.005008 | 0.005453 | 7.804x |
| Medium | 100,000 | 0.411331 | 0.030130 | 0.361158 | 0.456657 | 0.029413 | 0.032763 | 13.652x |
| Large | 1,000,000 | 4.037843 | 0.336417 | 3.564935 | 4.444302 | 0.321871 | 0.732215 | 12.003x |

### Throughput Results

| Dataset | CPU Throughput (bases/second) | GPU Throughput (bases/second) |
|---|---:|---:|
| 10,000 | 248,490 | 1,939,262 |
| 100,000 | 243,114 | 3,318,973 |
| 1,000,000 | 247,657 | 2,972,504 |

### Correctness Verification

All three benchmark configurations successfully produced identical
CPU and GPU alignment results.

10,000-base dataset: PASSED

100,000-base dataset: PASSED

1,000,000-base dataset: PASSED

Forward-strand alignment: VERIFIED

Reverse-strand alignment: VERIFIED

Zero-mismatch matching: VERIFIED

No CPU-GPU result mismatches occurred.

### Performance Analysis

GPU execution was faster across all three tested datasets.

The 10,000-base dataset achieved a 7.804x speedup.

The 100,000-base dataset achieved a 13.652x speedup.

The 1,000,000-base dataset achieved a 12.003x speedup.

GPU throughput reached approximately 3.32 million bases per second
on the medium dataset.

CPU throughput remained approximately 243,000 to 248,000
bases per second across the three datasets.

The results demonstrate a substantial GPU performance advantage
on the tested NVIDIA GeForce MX130.

The largest dataset showed greater variation between minimum
and maximum GPU execution times. Median execution time remains
the primary comparison metric.

These measurements evaluate the current implementation.
They do not independently quantify the improvement caused
specifically by output-buffer reuse.

### Benchmark Warnings and Limitations

Numba emitted a GPU occupancy warning for the small dataset.
This warning did not affect successful execution or correctness.

The measurements include GPU memory transfers, allocation,
and alignment execution time.

The results represent local benchmark measurements and are
not production performance guarantees.

Only three reference sizes and a 20-base target sequence
were evaluated. Further testing is required for larger
reference genomes, different mismatch tolerances, and
other GPU architectures.

### Conclusion

The optimized GPU alignment implementation outperformed
the CPU implementation across all three tested datasets.

The highest measured speedup was 13.652x on the
100,000-base dataset.

The GPU achieved approximately 3.32 million bases per second
on that dataset.

These measurements establish an updated performance baseline
for future GeneWeaver GPU optimization work.

