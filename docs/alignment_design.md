# DNA Alignment Design

## Overview

GeneWeaver includes a basic CPU-based DNA sequence alignment module.
It searches for a target DNA sequence within a reference sequence.

## Implemented Features

- Exact sequence matching.
- Reverse-strand matching using reverse complements.
- Configurable maximum mismatches.
- DNA input validation and normalization.
- Support for searching both strands or only the forward strand.

## Alignment Approach

The algorithm uses a sliding-window approach.

1. Validate and normalize the reference and target sequences.
2. Generate the reverse complement when both-strand searching is enabled.
3. Move a window across the reference sequence.
4. Compare each window with the target.
5. Count mismatched bases.
6. Return matches that do not exceed the configured mismatch limit.

## Match Result Fields

Each match contains:

- `start`: Zero-based starting position.
- `end`: Zero-based, end-exclusive position.
- `strand`: `+` for forward or `-` for reverse.
- `matched_sequence`: Observed sequence in the reference.
- `mismatches`: Number of mismatched bases.

## Pipeline Integration

The `process_fasta()` function supports optional target alignment.

When a target is provided, each FASTA record includes a `matches` field.
When no target is provided, the original pipeline output is preserved.

## Current Limitations

- The implementation uses a straightforward CPU-based sliding-window algorithm.
- It is not yet optimized for large-scale genomic searches.
- It does not currently implement biological scoring models, CRISPR PAM detection, or GPU acceleration.