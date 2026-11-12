from pathlib import Path

from geneweaver.fasta_parser import parse_fasta


def test_parse_fasta_returns_all_records():
    fasta_file = Path("data/sample.fasta")

    records = parse_fasta(fasta_file)

    assert len(records) == 3


def test_parse_fasta_extracts_correct_ids():
    records = parse_fasta("data/sample.fasta")

    assert [record["id"] for record in records] == [
        "gene_001",
        "gene_002",
        "gene_003",
    ]


def test_parse_fasta_extracts_sequences():
    records = parse_fasta("data/sample.fasta")

    assert records[0]["sequence"] == "ATGCGTACGTAG"
    assert records[1]["sequence"] == "ATGCCCGGTTAA"
    assert records[2]["sequence"] == "ATGAAATTTCCC"