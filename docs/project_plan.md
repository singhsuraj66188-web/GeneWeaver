# GeneWeaver - Project Plan

## Project Overview

GeneWeaver is an individual internship project focused on DNA sequence alignment and investigating GPU acceleration for CRISPR-related sequence analysis.

**Duration:** 10 November 2026 - 10 December 2026
**Development approach:** Incremental implementation, testing, and benchmarking.

## Development Phases

### Phase 1 - Environment and Project Setup
- Initialize the repository and project structure.
- Configure the Python development environment.
- Review hardware and software compatibility.
- Document the proposed architecture.

**Status:** Completed.

### Phase 2 - Sequence Alignment Foundation
- Study sequence alignment requirements.
- Develop DNA sequence validation utilities.
- Implement FASTA parsing.
- Develop sequence chunking and processing pipeline.
- Implement CPU-based DNA sequence alignment.
- Support reverse-complement matching and configurable mismatches.
- Expand automated correctness and edge-case tests.

**Status:** In progress.

### Phase 3 - GPU Acceleration Investigation
- Evaluate GPU-compatible tools and libraries.
- Investigate NVIDIA GPU compatibility.
- Implement a GPU path if technically feasible.
- Retain a CPU fallback.

**Status:** Pending.

### Phase 4 - Testing and Optimization
- Expand automated test coverage.
- Validate CPU and GPU results.
- Measure execution time and resource usage.
- Compare performance under documented conditions.

**Status:** In progress.

### Phase 5 - Documentation and Final Review
- Organize source code and documentation.
- Record benchmark results and limitations.
- Prepare project demonstration.
- Review the final repository.

**Status:** Ongoing.

## Current Status

**Current phase:** Phase 2 - Sequence Alignment Foundation.

**Completed:**
- GitHub repository created and connected.
- Python 3.12.10 virtual environment configured.
- Initial architecture and project documentation.
- DNA sequence validation.
- FASTA parsing.
- Sequence chunking and processing pipeline.
- CPU-based DNA sequence alignment.
- Reverse-complement functionality.
- Configurable mismatch handling.
- Alignment benchmark documentation.
- Alignment edge-case testing.

**Latest testing results (14 November 2026):**
- Alignment tests: 26 passed.
- Complete test suite: 66 passed.
- Failed tests: 0.
- Python: 3.12.10.
- pytest: 9.2.0.

**Pending:**
- Further alignment optimization.
- GPU compatibility investigation.
- GPU implementation if feasible.
- CPU/GPU performance comparison.
- Additional integration and performance testing.

## Technical Constraints

- Development environment: Windows.
- Python version: 3.12.10.
- GPU: NVIDIA GeForce MX130 with 2 GB VRAM.
- GPU-library compatibility must be verified before selecting a GPU implementation.
- CPU execution must remain available as a fallback.

## Important Note

The final algorithm, dataset, and GPU implementation will be selected based on project requirements, technical compatibility, and measured performance.
