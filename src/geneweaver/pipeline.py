"""DNA sequence processing pipeline."""

from geneweaver.fasta_parser import parse_fasta
from geneweaver.chunking import chunk_sequence
from geneweaver.sequence import validate_dna_sequence
from geneweaver.alignment import find_matches


def process_fasta(
    file_path,
    chunk_size=4,
    target=None,
    max_mismatches=0,
    both_strands=True,
):
    """Parse, validate, normalize, chunk and optionally align FASTA sequences."""

    records = parse_fasta(file_path)
    processed_records = []

    normalized_target = (
        validate_dna_sequence(target) if target is not None else None
    )

    for record in records:
        sequence = validate_dna_sequence(record["sequence"])

        processed_record = {
            "id": record["id"],
            "description": record["description"],
            "sequence": sequence,
            "chunks": chunk_sequence(sequence, chunk_size),
        }

        if normalized_target is not None:
            processed_record["matches"] = find_matches(
                reference=sequence,
                target=normalized_target,
                max_mismatches=max_mismatches,
                both_strands=both_strands,
            )

        processed_records.append(processed_record)

    return processed_records
