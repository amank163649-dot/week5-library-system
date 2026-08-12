import os
import shutil
import unittest
from library_system.library import Library


class TestLibrary(unittest.TestCase):
    def setUp(self):
        self.test_dir = 'test_data_tmp'
        self.lib = Library(
            books_file=os.path.join(self.test_dir, 'books.json'),
            members_file=os.path.join(self.test_dir, 'members.json'),
            backup_dir=os.path.join(self.test_dir, 'backup')
        )
        self.lib.add_book("Python Crash Course", "Eric Matthes", "9781593279288", 2019)
        self.lib.register_member("Alice Smith", "MEM001")

    def tearDown(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_add_book(self):
        success, _ = self.lib.add_book("Fluent Python", "Luciano Ramalho", "9781491946008")
        self.assertTrue(success)
        self.assertIn("9781491946008", self.lib.books)

    def test_add_duplicate_book(self):
        success, message = self.lib.add_book("Dup", "Author", "9781593279288")
        self.assertFalse(success)

    def test_remove_book(self):
        success, _ = self.lib.remove_book("9781593279288")
        self.assertTrue(success)

    def test_remove_borrowed_book_fails(self):
        self.lib.borrow_book("9781593279288", "MEM001")
        success, message = self.lib.remove_book("9781593279288")
        self.assertFalse(success)

    def test_search_books(self):
        results = self.lib.search_books("python", "title")
        self.assertEqual(len(results), 1)

    def test_borrow_and_return_flow(self):
        success, message = self.lib.borrow_book("9781593279288", "MEM001")
        self.assertTrue(success)
        self.assertFalse(self.lib.books["9781593279288"].available)
        self.assertIn("9781593279288", self.lib.members["MEM001"].borrowed_books)

        success, message = self.lib.return_book("9781593279288", "MEM001")
        self.assertTrue(success)
        self.assertTrue(self.lib.books["9781593279288"].available)

    def test_borrow_nonexistent_book(self):
        success, message = self.lib.borrow_book("0000000000", "MEM001")
        self.assertFalse(success)

    def test_statistics(self):
        stats = self.lib.statistics()
        self.assertEqual(stats['total_books'], 1)
        self.assertEqual(stats['total_members'], 1)
        self.assertEqual(stats['available_books'], 1)

    def test_save_and_load_data(self):
        success, _ = self.lib.save_data()
        self.assertTrue(success)

        new_lib = Library(
            books_file=self.lib.books_file,
            members_file=self.lib.members_file,
            backup_dir=self.lib.backup_dir
        )
        books_loaded, members_loaded = new_lib.load_data()
        self.assertEqual(books_loaded, 1)
        self.assertEqual(members_loaded, 1)
        self.assertIn("9781593279288", new_lib.books)


if __name__ == '__main__':
    unittest.main()
