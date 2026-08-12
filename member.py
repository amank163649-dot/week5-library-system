"""Member class - represents a library member."""


class Member:
    """Represents a library member."""

    MAX_BOOKS = 5

    def __init__(self, name, member_id, max_books=None):
        self.name = name
        self.member_id = member_id
        self.borrowed_books = []  # list of ISBNs
        self.max_books = max_books or Member.MAX_BOOKS

    def borrow_book(self, isbn):
        """Record that this member borrowed a book (by ISBN)."""
        if len(self.borrowed_books) >= self.max_books:
            return False, f"{self.name} has reached the maximum borrow limit ({self.max_books})"
        if isbn in self.borrowed_books:
            return False, f"{self.name} has already borrowed this book"
        self.borrowed_books.append(isbn)
        return True, f"{self.name} borrowed the book successfully"

    def return_book(self, isbn):
        """Record that this member returned a book (by ISBN)."""
        if isbn not in self.borrowed_books:
            return False, f"{self.name} has not borrowed this book"
        self.borrowed_books.remove(isbn)
        return True, f"{self.name} returned the book successfully"

    def can_borrow(self):
        """Check if member is under their borrow limit."""
        return len(self.borrowed_books) < self.max_books

    def to_dict(self):
        """Convert member to dictionary for serialization."""
        return {
            'name': self.name,
            'member_id': self.member_id,
            'borrowed_books': self.borrowed_books,
            'max_books': self.max_books
        }

    @classmethod
    def from_dict(cls, data):
        """Create Member instance from dictionary."""
        member = cls(
            name=data['name'],
            member_id=data['member_id'],
            max_books=data.get('max_books', Member.MAX_BOOKS)
        )
        member.borrowed_books = data.get('borrowed_books', [])
        return member

    def __str__(self):
        return f"{self.name} (ID: {self.member_id}) - {len(self.borrowed_books)}/{self.max_books} books borrowed"

    def __repr__(self):
        return f"Member('{self.name}', '{self.member_id}')"
