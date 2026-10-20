
import unittest
import server


class TestStudyNotes(unittest.TestCase):

    def setUp(self):
        server.initialize_database()

    def test_create_note(self):
        result = server.create_note(
            "Python Basics",
            "Python supports functions and classes.",
            "Python"
        )
        self.assertIn("Note created successfully", result)

    def test_search_note(self):
        server.create_note(
            "MCP Basics",
            "MCP connects AI applications with tools.",
            "AI"
        )
        result = server.search_notes("MCP")
        self.assertIn("MCP Basics", result)

    def test_list_tags(self):
        server.create_note(
            "SQL Basics",
            "SQL is used to query databases.",
            "Database"
        )
        result = server.list_tags()
        self.assertIn("Database", result)

    def test_empty_search_rejected(self):
        with self.assertRaises(ValueError):
            server.search_notes("   ")

    def test_empty_note_rejected(self):
        with self.assertRaises(ValueError):
            server.create_note("", "Some content", "Python")


if __name__ == "__main__":
    unittest.main(verbosity=2)

