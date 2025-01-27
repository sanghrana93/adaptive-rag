import unittest
from src.adaptive_rag import determine_query_complexity, handle_simple_query

class TestAdaptiveRAG(unittest.TestCase):

    def test_determine_query_complexity(self):
        self.assertEqual(determine_query_complexity("What is the capital of France?"), "simple")
        self.assertEqual(determine_query_complexity("Explain the theory of relativity in detail."), "complex")

    def test_handle_simple_query(self):
        response = handle_simple_query("What is the capital of France?")
        self.assertIsInstance(response, str)
        self.assertGreater(len(response), 0)

if __name__ == "__main__":
    unittest.main()