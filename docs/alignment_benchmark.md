# DNA Alignment Benchmark Results

## Overview

This document records the actual performance measurements
of GeneWeaver's CPU-based DNA alignment implementation.

## Benchmark Environment

- Python Version: 3.12.10
- Operating System: Windows
- Target Sequence Length: 20 bases
- Search Strands: Forward and reverse
- Runs Per Dataset: 3
- Measurement: Median execution time

## Benchmark Results

| Dataset | Reference Length | Median Time | Matches | Throughput |
|---|---:|---:|---:|---:|
| Small | 10,000 | 0.033228 s | 1 | 300,952 bases/sec |
| Medium | 100,000 | 0.364368 s | 1 | 274,448 bases/sec |
| Large | 1,000,000 | 3.440903 s | 1 | 290,621 bases/sec |

## Performance Observations

- The alignment algorithm successfully processed all three datasets.
- Each dataset returned one match.
- Throughput remained within approximately 274,000–301,000 bases per second.
- Execution time increased with reference sequence length.
- The implementation currently uses a CPU-based sliding-window approach.

## Limitations

- The benchmark uses a limited number of runs.
- Results represent the current Windows environment.
- Performance may vary across hardware and Python versions.
- Further optimization is required for large-scale genomic searches.

## Conclusion

GeneWeaver successfully completed DNA alignment benchmarks
on reference sequences ranging from 10,000 to 1,000,000 bases.

The measured results establish an initial performance baseline
for future optimization and comparison.