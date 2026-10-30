from .index import format_matches, search
from .models import Document


def main() -> None:
    documents = [
        Document("guide", "A small retrieval index answers questions from documents."),
        Document("notes", "Python can tokenize text and rank matching chunks."),
    ]
    print(format_matches(search("python retrieval", documents)))


if __name__ == "__main__":
    main()
