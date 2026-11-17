# CRISPR Search Performance Benchmark

## Overview

This benchmark measures the end-to-end execution performance of the
GeneWeaver CRISPR target search implementation.

It evaluates guide RNA validation, RNA-to-DNA conversion, DNA alignment,
PAM detection, and final candidate generation.

## Environment

- Python: 3.12.10
- Platform: Windows 10
- Search engine: GeneWeaver CPU implementation
- Guide RNA length: 20 bases
- PAM pattern: NGG
- Search strands: Forward and reverse
- Runs per dataset: 3
- Reported measurement: Median execution time

## Benchmark Results

| Dataset | Reference size | Median time (s) | Throughput (bases/s) | Candidates |
|---|---:|---:|---:|---:|
| Small | 10,000 | 0.045372 | 220,398 | 1 |
| Medium | 100,000 | 0.450947 | 221,755 | 1 |
| Large | 1,000,000 | 4.042041 | 247,400 | 1 |

## Validation

All three datasets successfully detected the deliberately inserted
CRISPR target.

- Small dataset: PASSED
- Medium dataset: PASSED
- Large dataset: PASSED

## Performance Observations

The measured throughput ranged from approximately 220,000 to
247,000 bases per second.

The benchmark demonstrates that the current CPU implementation can
process increasingly large synthetic DNA reference sequences.

These results provide an initial performance baseline for future
optimization and GPU acceleration.

## Limitations

- The benchmark uses synthetic DNA sequences.
- Results are specific to the recorded hardware and software environment.
- Only three timing runs were performed per dataset.
- These measurements are not representative of a complete human genome
  analysis workload.
- No GPU performance comparison has been performed yet.

## Conclusion

The end-to-end CRISPR search benchmark completed successfully.

All three datasets detected the expected target. The recorded CPU
measurements will serve as a baseline for future GeneWeaver optimization.
