"""Deterministic toy retrieval engine with no external dependencies."""

import math
import re
from collections import Counter

from .models import Document, Match


def tokenize(text: str) -> list[str]:
    """Turn text into lowercase search terms."""
    return re.findall(r"[a-z0-9]+", text.lower())


def split_sentences(text: str) -> list[str]:
    """Keep sentence-like units for readable excerpts."""
    return [part.strip() for part in re.split(r"(?<=[.!?])\s+", text) if part.strip()]


def chunk_document(document: Document, maximum: int = 160) -> list[str]:
    """Make bounded chunks without discarding source text."""
    chunks: list[str] = []
    current = ""
    for sentence in split_sentences(document.body):
        if current and len(current) + len(sentence) + 1 > maximum:
            chunks.append(current)
            current = ""
        current = f"{current} {sentence}".strip()
    if current:
        chunks.append(current)
    return chunks


def term_frequency(text: str) -> Counter[str]:
    """Count each term in one text span."""
    return Counter(tokenize(text))


def vector_length(weights: Counter[str]) -> float:
    """Compute the Euclidean norm of a term vector."""
    return math.sqrt(sum(value * value for value in weights.values()))


def cosine_similarity(left: Counter[str], right: Counter[str]) -> float:
    """Score overlap without any learned embeddings."""
    denominator = vector_length(left) * vector_length(right)
    if denominator == 0:
        return 0.0
    return sum(value * right.get(term, 0) for term, value in left.items()) / denominator


def index_documents(documents: list[Document]) -> list[tuple[str, str, Counter[str]]]:
    """Precompute chunk vectors for the supplied documents."""
    records: list[tuple[str, str, Counter[str]]] = []
    for document in documents:
        for chunk in chunk_document(document):
            records.append((document.name, chunk, term_frequency(chunk)))
    return records


def rank_chunks(query: str, documents: list[Document]) -> list[Match]:
    """Return positive-scoring chunks in deterministic order."""
    query_vector = term_frequency(query)
    matches = [
        Match(name, chunk, cosine_similarity(query_vector, weights))
        for name, chunk, weights in index_documents(documents)
    ]
    return sorted(
        (match for match in matches if match.score > 0),
        key=lambda match: (-match.score, match.document, match.excerpt),
    )


def search(query: str, documents: list[Document], limit: int = 3) -> list[Match]:
    """Give callers the best few snippets."""
    if limit < 1:
        return []
    return rank_chunks(query, documents)[:limit]


def format_matches(matches: list[Match]) -> str:
    """Create a compact human-readable result."""
    if not matches:
        return "No matching documents."
    return "\n".join(
        f"{match.document} ({match.score:.2f}): {match.excerpt}"
        for match in matches
    )
