import unittest
from library_system.book import Book


class TestBook(unittest.TestCase):
    def setUp(self):
        self.book = Book("Fluent Python", "Luciano Ramalho", "9781491946008", 2022)

    def test_initial_state(self):
        self.assertTrue(self.book.available)
        self.assertIsNone(self.book.borrowed_by)
        self.assertIsNone(self.book.due_date)

    def test_check_out_success(self):
        success, message = self.book.check_out("MEM001")
        self.assertTrue(success)
        self.assertFalse(self.book.available)
        self.assertEqual(self.book.borrowed_by, "MEM001")
        self.assertIsNotNone(self.book.due_date)

    def test_check_out_already_borrowed(self):
        self.book.check_out("MEM001")
        success, message = self.book.check_out("MEM002")
        self.assertFalse(success)
        self.assertIn("already checked out", message)

    def test_return_book(self):
        self.book.check_out("MEM001")
        success, message = self.book.return_book()
        self.assertTrue(success)
        self.assertTrue(self.book.available)
        self.assertIsNone(self.book.borrowed_by)

    def test_return_book_not_borrowed(self):
        success, message = self.book.return_book()
        self.assertFalse(success)

    def test_matches_search(self):
        self.assertTrue(self.book.matches("fluent"))
        self.assertTrue(self.book.matches("Ramalho"))
        self.assertTrue(self.book.matches("9781491946008"))
        self.assertFalse(self.book.matches("java"))

    def test_to_dict_and_from_dict(self):
        self.book.check_out("MEM001")
        data = self.book.to_dict()
        restored = Book.from_dict(data)
        self.assertEqual(restored.title, self.book.title)
        self.assertEqual(restored.borrowed_by, "MEM001")
        self.assertFalse(restored.available)


if __name__ == '__main__':
    unittest.main()
