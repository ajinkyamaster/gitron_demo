from dataclasses import dataclass


@dataclass(frozen=True)
class Document:
    name: str
    body: str


@dataclass(frozen=True)
class Match:
    document: str
    excerpt: str
    score: float
