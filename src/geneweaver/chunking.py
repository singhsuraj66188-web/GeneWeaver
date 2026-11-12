def chunk_sequence(sequence, chunk_size):
    """Split a DNA sequence into fixed-size chunks."""

    if not isinstance(sequence, str):
        raise TypeError("Sequence must be a string")

    if not isinstance(chunk_size, int) or isinstance(chunk_size, bool):
        raise TypeError("Chunk size must be an integer")

    if chunk_size <= 0:
        raise ValueError("Chunk size must be greater than zero")

    return [
        sequence[i:i + chunk_size]
        for i in range(0, len(sequence), chunk_size)
    ]