
# GeneWeaver — Project Plan

## Project Overview

GeneWeaver is an individual internship project focused on DNA sequence alignment and investigating GPU acceleration for CRISPR-related sequence analysis.

**Duration:** 10 November 2026 – 10 December 2026
**Development approach:** Incremental implementation, testing, and benchmarking.

## Development Phases

### Phase 1 — Environment and Project Setup
- Initialize the repository and project structure.
- Configure the Python development environment.
- Review available hardware and software compatibility.
- Document the proposed architecture.

### Phase 2 — Sequence Alignment Foundation
- Study the sequence alignment requirements.
- Select an appropriate alignment algorithm.
- Develop a CPU-based reference implementation.
- Add basic correctness tests.

### Phase 3 — GPU Acceleration Investigation
- Evaluate GPU-compatible tools and libraries.
- Investigate whether the available NVIDIA GPU supports the selected approach.
- Implement a GPU path if technically feasible.
- Retain a CPU fallback.

### Phase 4 — Testing and Optimization
- Expand automated test coverage.
- Validate CPU and GPU results for correctness.
- Measure execution time and resource usage.
- Compare performance under documented conditions.

### Phase 5 — Documentation and Final Review
- Organize source code and documentation.
- Record benchmark results and limitations.
- Prepare project demonstration.
- Review the final repository.

## Current Status

**Phase:** Phase 1 — Environment and Project Setup

**Completed:**
- GitHub repository created and connected.
- Local Git repository initialized.
- Python 3.12.10 virtual environment configured.
- Initial project documentation created.
- README and .gitignore created.
- System architecture documented.
- Initial documentation commit pushed to GitHub.

**Pending:**
- Review official project requirements.
- Finalize the alignment algorithm.
- Develop the CPU reference implementation.
- Add automated correctness tests.
- Evaluate GPU compatibility.
- Implement GPU acceleration if technically feasible.
- Benchmark and document results.

## Technical Constraints

- Development environment: Windows.
- Python version: 3.12.10.
- GPU: NVIDIA GeForce MX130 with 2 GB VRAM.
- CUDA Toolkit (`nvcc`) was not detected during initial inspection.
- GPU-library compatibility must be verified before selecting a GPU implementation.
- CPU execution must remain available as a fallback.

## Important Note

The final algorithm, dataset, and GPU implementation will be selected after reviewing the official project requirements and verifying technical compatibility.