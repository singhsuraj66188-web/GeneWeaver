
# GeneWeaver — System Architecture

## 1. Overview

GeneWeaver is planned as a modular DNA sequence alignment engine. The architecture separates sequence handling, alignment logic, execution backends, testing, and benchmarking.

The design will evolve as project requirements and hardware compatibility are verified.

## 2. High-Level Workflow

1. Receive DNA sequences as input.
2. Validate sequence data.
3. Prepare sequences for alignment.
4. Execute the selected alignment algorithm.
5. Return alignment results.
6. Validate correctness and measure performance.

## 3. Planned Components

### Sequence Input and Validation
- Accept DNA sequence inputs.
- Validate supported nucleotide characters.
- Handle invalid or empty input appropriately.

### Alignment Engine
- Contain the core sequence alignment logic.
- Begin with a CPU-based reference implementation.
- Keep algorithm-specific logic separate from input handling.

### Execution Backend
- Provide the CPU execution path.
- Investigate a GPU execution path after compatibility checks.
- Allow CPU fallback when GPU execution is unavailable.

### Testing
- Verify sequence validation.
- Test alignment correctness.
- Cover edge cases and invalid inputs.
- Compare results across execution backends when available.

### Benchmarking
- Measure execution time.
- Record input sizes and test conditions.
- Compare CPU and GPU performance only under equivalent conditions.

## 4. Proposed Repository Structure

```text
GeneWeaver/
├── src/
│   └── geneweaver/
├── tests/
├── benchmarks/
├── docs/
│   ├── project_plan.md
│   └── architecture.md
├── scripts/
├── .gitignore
└── README.md
```

## 5. Hardware and Compatibility

Development hardware currently includes an NVIDIA GeForce MX130 with 2 GB VRAM.

The CUDA Toolkit and compatibility of GPU libraries have not yet been verified. GPU implementation decisions will be made only after testing the available environment.

## 6. Design Principles

- Modular and maintainable code.
- Correctness before optimization.
- Reproducible tests and benchmarks.
- CPU fallback for compatibility.
- Documented performance limitations.
- No unsupported claims about GPU acceleration.

## 7. Current Architecture Status

**Status:** Initial design

The component boundaries and execution workflow are proposed. The final alignment algorithm, GPU framework, and data format remain to be selected.
