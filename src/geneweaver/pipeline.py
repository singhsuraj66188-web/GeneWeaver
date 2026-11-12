from geneweaver.fasta_parser import parse_fasta
from geneweaver.chunking import chunk_sequence
from geneweaver.sequence import validate_dna_sequence


def process_fasta(file_path, chunk_size=4):
    """Parse, validate, normalize and chunk FASTA sequences."""

    records = parse_fasta(file_path)
    processed_records = []

    for record in records:
        sequence = validate_dna_sequence(record["sequence"])

        processed_records.append({
            "id": record["id"],
            "description": record["description"],
            "sequence": sequence,
            "chunks": chunk_sequence(sequence, chunk_size)
        })

    return processed_records