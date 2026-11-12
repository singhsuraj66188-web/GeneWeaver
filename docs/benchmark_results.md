
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
