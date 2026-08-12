# Library Management System

## Project Description
A comprehensive library management system built using Object-Oriented Programming principles. This system allows librarians to manage books, members, and borrowing operations efficiently.

## What I Learned
- **OOP Principles**: Classes, objects, inheritance, and encapsulation
- **Class Design**: How to design classes for real-world systems
- **Class Relationships**: Understanding how `Book`, `Member`, and `Library` interact
- **Method Implementation**: Creating methods that model real behaviors (checkout, return, overdue tracking)
- **Data Persistence**: Saving and loading object data to/from JSON files

## Features
- Add, remove, and search for books
- Register and manage library members
- Borrow and return books with due dates
- Track overdue books and calculate days overdue
- Search books by title, author, or ISBN
- Limit maximum books per member (default: 5)
- Save/load data to JSON files, with timestamped backups
- User-friendly menu interface
- Error handling for file operations and invalid input

## Project Structure
```
week5-library-system/
├── library_system/
│   ├── __init__.py
│   ├── book.py       # Book class
│   ├── member.py      # Member class
│   ├── library.py     # Library class (manages books/members)
│   └── main.py         # CLI entry point
├── data/
│   ├── books.json
│   ├── members.json
│   └── backup/
├── tests/
│   ├── test_book.py
│   ├── test_member.py
│   └── test_library.py
├── requirements.txt
├── README.md
└── .gitignore
```

## How to Run
```bash
cd week5-library-system
python -m library_system.main
```

## How to Run Tests
```bash
cd week5-library-system
python -m unittest discover -s tests -v
```

## Class Structure

```python
class Book:
    def __init__(self, title, author, isbn, year=None):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.available = True
        self.borrowed_by = None
        self.due_date = None

class Member:
    def __init__(self, name, member_id, max_books=5):
        self.name = name
        self.member_id = member_id
        self.borrowed_books = []
        self.max_books = max_books

class Library:
    def __init__(self):
        self.books = {}     # isbn -> Book
        self.members = {}   # member_id -> Member
```

## Sample Menu
```
================================
    LIBRARY MANAGEMENT SYSTEM
================================
1. Add New Book
2. Register New Member
3. Borrow Book
4. Return Book
5. Search Books
6. View All Books
7. View All Members
8. View Overdue Books
9. Save & Exit
0. Exit Without Saving

Enter your choice:
```

## Sample Output
```
Search Results for 'python':
----------------------------------------
1. Python Crash Course by Eric Matthes (9781593279288) - Available
2. Automate the Boring Stuff with Python by Al Sweigart (9781593275990) - Borrowed by MEM001 (Due: 2024-02-15)
3. Fluent Python by Luciano Ramalho (9781491946008) - Available

Found 3 book(s)

Library Statistics:
- Total Books: 5
- Available Books: 4
- Total Members: 2
- Books Borrowed: 1
- Overdue Books: 0
```

## Technical Details
- **Data structures**: books and members are stored as dictionaries keyed by ISBN / member ID for O(1) lookup.
- **Persistence**: `Book.to_dict()`/`from_dict()` and `Member.to_dict()`/`from_dict()` handle serialization; `Library.save_data()` / `load_data()` handle JSON I/O with error handling for missing/corrupt files.
- **Overdue calculation**: `Book.is_overdue()` and `Book.days_overdue()` compare the stored due date against the current date using `datetime`.
- **Backups**: `Library.backup_data()` copies the current JSON files into `data/backup/` with a timestamp before saving.

## Testing Evidence
23 unit tests across `test_book.py`, `test_member.py`, and `test_library.py` cover checkout/return flows, borrow limits, search, duplicate handling, statistics, and save/load round-trips. All tests pass:
```
Ran 23 tests in 0.007s
OK
```
