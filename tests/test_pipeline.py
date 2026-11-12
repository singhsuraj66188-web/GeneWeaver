import pytest
from geneweaver.pipeline import process_fasta


def test_pipeline_processes_all_fasta_records():
    records = process_fasta("data/sample.fasta")

    assert len(records) == 3


def test_pipeline_creates_correct_chunks():
    records = process_fasta("data/sample.fasta", chunk_size=4)

    assert records[0]["chunks"] == ["ATGC", "GTAC", "GTAG"]


def test_pipeline_preserves_original_sequences():
    records = process_fasta("data/sample.fasta")

    assert records[0]["sequence"] == "ATGCGTACGTAG"


def test_pipeline_preserves_record_ids():
    records = process_fasta("data/sample.fasta")

    assert [record["id"] for record in records] == [
        "gene_001",
        "gene_002",
        "gene_003"
    ]

import pytest


def test_pipeline_normalizes_dna_sequences():
    records = process_fasta("data/sample.fasta")

    for record in records:
        assert record["sequence"] == record["sequence"].upper()


def test_pipeline_rejects_invalid_dna(tmp_path):
    from geneweaver.pipeline import process_fasta

    fasta_file = tmp_path / "invalid.fasta"
    fasta_file.write_text(">invalid_gene\nATGX\n")

    with pytest.raises(ValueError, match="Invalid DNA nucleotides"):
        process_fasta(fasta_file)