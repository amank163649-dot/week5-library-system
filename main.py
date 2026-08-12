"""Command-line interface for the Library Management System."""
from .library import Library


def print_header():
    print("=" * 32)
    print("    LIBRARY MANAGEMENT SYSTEM")
    print("=" * 32)


def print_menu():
    print("""
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
""")


def prompt(text):
    return input(text).strip()


def add_book(lib):
    title = prompt("Title: ")
    author = prompt("Author: ")
    isbn = prompt("ISBN: ")
    year = prompt("Year (optional): ")
    year = int(year) if year.isdigit() else None
    success, message = lib.add_book(title, author, isbn, year)
    print(message)


def register_member(lib):
    name = prompt("Member name: ")
    member_id = prompt("Member ID: ")
    success, message = lib.register_member(name, member_id)
    print(message)


def borrow_book(lib):
    isbn = prompt("Book ISBN: ")
    member_id = prompt("Member ID: ")
    success, message = lib.borrow_book(isbn, member_id)
    print(message)


def return_book(lib):
    isbn = prompt("Book ISBN: ")
    member_id = prompt("Member ID: ")
    success, message = lib.return_book(isbn, member_id)
    print(message)


def search_books(lib):
    print("""
Search books by:
1. Title
2. Author
3. ISBN
4. Show all available books
""")
    option = prompt("Enter search option: ")
    field_map = {'1': 'title', '2': 'author', '3': 'isbn'}

    if option == '4':
        results = lib.available_books()
        print(f"\nAvailable books ({len(results)}):")
    else:
        field = field_map.get(option, 'all')
        query = prompt(f"Enter {field} to search: ")
        results = lib.search_books(query, field)
        print(f"\nSearch Results for '{query}':")

    print("-" * 40)
    for i, book in enumerate(results, 1):
        print(f"{i}. {book}")
    print(f"\nFound {len(results)} book(s)")


def view_all_books(lib):
    print(f"\nAll Books ({len(lib.books)}):")
    print("-" * 40)
    for i, book in enumerate(lib.books.values(), 1):
        print(f"{i}. {book}")


def view_all_members(lib):
    print(f"\nAll Members ({len(lib.members)}):")
    print("-" * 40)
    for i, member in enumerate(lib.members.values(), 1):
        print(f"{i}. {member}")


def view_overdue(lib):
    overdue = lib.overdue_books()
    print(f"\nOverdue Books ({len(overdue)}):")
    print("-" * 40)
    for i, book in enumerate(overdue, 1):
        print(f"{i}. {book} - {book.days_overdue()} day(s) overdue")


def print_stats(lib):
    stats = lib.statistics()
    print("\nLibrary Statistics:")
    print(f"- Total Books: {stats['total_books']}")
    print(f"- Available Books: {stats['available_books']}")
    print(f"- Total Members: {stats['total_members']}")
    print(f"- Books Borrowed: {stats['borrowed_books']}")
    print(f"- Overdue Books: {stats['overdue_books']}")


def main():
    print_header()
    lib = Library()
    books_loaded, members_loaded = lib.load_data()
    print(f"Loaded {books_loaded} books from file")
    print(f"Loaded {members_loaded} members from file")

    actions = {
        '1': add_book,
        '2': register_member,
        '3': borrow_book,
        '4': return_book,
        '5': search_books,
        '6': view_all_books,
        '7': view_all_members,
        '8': view_overdue,
    }

    while True:
        print_menu()
        choice = prompt("Enter your choice: ")

        if choice in actions:
            actions[choice](lib)
        elif choice == '9':
            lib.backup_data()
            success, message = lib.save_data()
            print(message)
            print_stats(lib)
            print("Goodbye!")
            break
        elif choice == '0':
            print("Exiting without saving. Goodbye!")
            break
        else:
            print("Invalid choice, please try again.")


if __name__ == '__main__':
    main()
