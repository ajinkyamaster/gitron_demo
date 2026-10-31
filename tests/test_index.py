import unittest

from rag_demo.index import search
from rag_demo.models import Document


class SearchTests(unittest.TestCase):
    def test_relevant_document_ranks_first(self) -> None:
        documents = [
            Document("a", "Dogs bark."),
            Document("b", "Python indexes documents."),
        ]
        self.assertEqual(search("python documents", documents)[0].document, "b")
