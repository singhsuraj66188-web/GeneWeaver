# PAM Detection Design

## 1. Overview

GeneWeaver includes a PAM detection module for identifying SpCas9
Protospacer Adjacent Motif (PAM) sequences in DNA.

The implementation is located in:

- `src/geneweaver/pam.py`
- `tests/test_pam.py`

## 2. Supported PAM Patterns

The implementation detects SpCas9 PAM sequences on both DNA strands.

| Strand | Pattern | Description |
|---|---|---|
| Forward (+) | NGG | Any nucleotide followed by two guanines |
| Reverse (-) | CCN | Two cytosines followed by any nucleotide |

Here, N represents any valid DNA nucleotide (A, T, G, or C).

## 3. Implementation

The `find_pam_sites()` function accepts:

- A DNA sequence.
- An optional `both_strands` boolean parameter.

It validates the input DNA sequence and scans consecutive
three-nucleotide windows.

For each detected PAM, it returns:

- `start`: Zero-based starting coordinate.
- `end`: Zero-based end-exclusive coordinate.
- `strand`: Either `+` or `-`.
- `pam_sequence`: PAM sequence in its strand-oriented representation.

Results are sorted by genomic starting position and strand.

## 4. Validation

The implementation uses the existing DNA sequence validation
utility and reverse-complement functionality.

Invalid DNA sequences and non-boolean `both_strands` values
are rejected.

## 5. Testing

The PAM detection test module contains 13 tests covering:

- Forward NGG detection.
- Reverse CCN detection.
- Multiple PAM sites.
- Strand selection.
- Sequence boundaries.
- Lowercase input.
- Sequences without PAM sites.
- Invalid and empty DNA sequences.
- Invalid parameter types.

## 6. Test Results

The dedicated PAM test suite:

- 13 tests passed.
- 0 failures.

The complete GeneWeaver test suite:

- 79 tests passed.
- 0 failures.
- Execution time: 14.12 seconds.

## 7. Current Scope

This module detects PAM motifs only. It does not yet implement
guide RNA selection, off-target scoring, or biological activity
prediction.
