from Bio import SeqIO


def parse_fasta(file_path):
    """Parse a FASTA file and return sequence records."""
    records = []

    for record in SeqIO.parse(file_path, "fasta"):
        records.append({
            "id": record.id,
            "description": record.description,
            "sequence": str(record.seq)
        })

    return records