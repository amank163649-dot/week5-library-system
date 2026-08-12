import unittest
from library_system.member import Member


class TestMember(unittest.TestCase):
    def setUp(self):
        self.member = Member("Alice Smith", "MEM001", max_books=2)

    def test_initial_state(self):
        self.assertEqual(len(self.member.borrowed_books), 0)
        self.assertTrue(self.member.can_borrow())

    def test_borrow_book(self):
        success, message = self.member.borrow_book("111")
        self.assertTrue(success)
        self.assertIn("111", self.member.borrowed_books)

    def test_borrow_duplicate(self):
        self.member.borrow_book("111")
        success, message = self.member.borrow_book("111")
        self.assertFalse(success)

    def test_max_borrow_limit(self):
        self.member.borrow_book("111")
        self.member.borrow_book("222")
        self.assertFalse(self.member.can_borrow())
        success, message = self.member.borrow_book("333")
        self.assertFalse(success)
        self.assertIn("maximum", message)

    def test_return_book(self):
        self.member.borrow_book("111")
        success, message = self.member.return_book("111")
        self.assertTrue(success)
        self.assertNotIn("111", self.member.borrowed_books)

    def test_return_not_borrowed(self):
        success, message = self.member.return_book("999")
        self.assertFalse(success)

    def test_to_dict_and_from_dict(self):
        self.member.borrow_book("111")
        data = self.member.to_dict()
        restored = Member.from_dict(data)
        self.assertEqual(restored.name, self.member.name)
        self.assertIn("111", restored.borrowed_books)


if __name__ == '__main__':
    unittest.main()
