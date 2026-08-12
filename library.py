"""Library class - manages books, members, and borrowing operations."""
import json
import os
import shutil
from datetime import datetime

from .book import Book
from .member import Member


class Library:
    """Manages the collection of books and members."""

    def __init__(self, books_file='data/books.json', members_file='data/members.json',
                 backup_dir='data/backup'):
        self.books = {}      # isbn -> Book
        self.members = {}    # member_id -> Member
        self.books_file = books_file
        self.members_file = members_file
        self.backup_dir = backup_dir

    # ---------- Book management ----------
    def add_book(self, title, author, isbn, year=None):
        if isbn in self.books:
            return False, "A book with this ISBN already exists"
        self.books[isbn] = Book(title, author, isbn, year)
        return True, f"Book '{title}' added successfully"

    def remove_book(self, isbn):
        if isbn not in self.books:
            return False, "Book not found"
        if not self.books[isbn].available:
            return False, "Cannot remove a book that is currently borrowed"
        del self.books[isbn]
        return True, "Book removed successfully"

    def find_book(self, isbn):
        return self.books.get(isbn)

    def search_books(self, query, field='all'):
        """Search books by title, author, isbn, or all fields."""
        results = []
        query_lower = query.lower()
        for book in self.books.values():
            if field == 'title' and query_lower in book.title.lower():
                results.append(book)
            elif field == 'author' and query_lower in book.author.lower():
                results.append(book)
            elif field == 'isbn' and query_lower in book.isbn.lower():
                results.append(book)
            elif field == 'all' and book.matches(query):
                results.append(book)
        return results

    def available_books(self):
        return [b for b in self.books.values() if b.available]

    # ---------- Member management ----------
    def register_member(self, name, member_id, max_books=None):
        if member_id in self.members:
            return False, "A member with this ID already exists"
        self.members[member_id] = Member(name, member_id, max_books)
        return True, f"Member '{name}' registered successfully"

    def find_member(self, member_id):
        return self.members.get(member_id)

    # ---------- Borrow / Return ----------
    def borrow_book(self, isbn, member_id, loan_period=14):
        book = self.find_book(isbn)
        member = self.find_member(member_id)

        if not book:
            return False, "Book not found"
        if not member:
            return False, "Member not found"
        if not member.can_borrow():
            return False, f"Member has reached max borrow limit ({member.max_books})"

        success, message = book.check_out(member_id, loan_period)
        if not success:
            return False, message

        member.borrow_book(isbn)
        return True, message

    def return_book(self, isbn, member_id):
        book = self.find_book(isbn)
        member = self.find_member(member_id)

        if not book:
            return False, "Book not found"
        if not member:
            return False, "Member not found"

        overdue_days = book.days_overdue()
        success, message = book.return_book()
        if not success:
            return False, message

        member.return_book(isbn)
        if overdue_days > 0:
            message += f" ({overdue_days} day(s) overdue)"
        return True, message

    def overdue_books(self):
        return [b for b in self.books.values() if b.is_overdue()]

    # ---------- Statistics ----------
    def statistics(self):
        total_books = len(self.books)
        available = len(self.available_books())
        borrowed = total_books - available
        return {
            'total_books': total_books,
            'available_books': available,
            'borrowed_books': borrowed,
            'total_members': len(self.members),
            'overdue_books': len(self.overdue_books())
        }

    # ---------- File persistence ----------
    def save_data(self):
        """Save books and members to JSON files."""
        try:
            os.makedirs(os.path.dirname(self.books_file), exist_ok=True)
            os.makedirs(os.path.dirname(self.members_file), exist_ok=True)

            with open(self.books_file, 'w') as f:
                json.dump([b.to_dict() for b in self.books.values()], f, indent=2)

            with open(self.members_file, 'w') as f:
                json.dump([m.to_dict() for m in self.members.values()], f, indent=2)

            return True, "Data saved successfully"
        except (IOError, OSError) as e:
            return False, f"Error saving data: {e}"

    def load_data(self):
        """Load books and members from JSON files."""
        books_loaded = 0
        members_loaded = 0

        try:
            if os.path.exists(self.books_file):
                with open(self.books_file, 'r') as f:
                    books_data = json.load(f)
                    for data in books_data:
                        book = Book.from_dict(data)
                        self.books[book.isbn] = book
                    books_loaded = len(books_data)
        except (IOError, json.JSONDecodeError) as e:
            print(f"Warning: Could not load books ({e}). Starting with empty catalog.")

        try:
            if os.path.exists(self.members_file):
                with open(self.members_file, 'r') as f:
                    members_data = json.load(f)
                    for data in members_data:
                        member = Member.from_dict(data)
                        self.members[member.member_id] = member
                    members_loaded = len(members_data)
        except (IOError, json.JSONDecodeError) as e:
            print(f"Warning: Could not load members ({e}). Starting with empty roster.")

        return books_loaded, members_loaded

    def backup_data(self):
        """Create a timestamped backup of the current data files."""
        try:
            os.makedirs(self.backup_dir, exist_ok=True)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

            if os.path.exists(self.books_file):
                shutil.copy(self.books_file, os.path.join(self.backup_dir, f'books_{timestamp}.json'))
            if os.path.exists(self.members_file):
                shutil.copy(self.members_file, os.path.join(self.backup_dir, f'members_{timestamp}.json'))

            return True, f"Backup created at {timestamp}"
        except (IOError, OSError) as e:
            return False, f"Error creating backup: {e}"
