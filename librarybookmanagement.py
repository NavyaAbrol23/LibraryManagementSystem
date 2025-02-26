import os
from datetime import datetime

BOOKS_FILE = "books.txt"
BORROWED_FILE = "borrowed.txt"

def initialize_files():
    if not os.path.exists(BOOKS_FILE):
        with open(BOOKS_FILE, "w") as f:
            f.write("ID,Title,Author,Available\n")

    if not os.path.exists(BORROWED_FILE):
        with open(BORROWED_FILE, "w") as f:
            f.write("BookID,Borrower,BorrowDate,ReturnDate\n")

def add_book():
    title = input("Enter book title: ").strip()
    author = input("Enter author name: ").strip()

    with open(BOOKS_FILE, "r") as f:
        lines = f.readlines()
        book_id = len(lines)

    with open(BOOKS_FILE, "a") as f:
        f.write(f"{book_id},{title},{author},Yes\n")

    print(f"Book '{title}' by {author} added successfully!")

def view_books():
    with open(BOOKS_FILE, "r") as f:
        books = f.readlines()[1:]

    print("\nAvailable Books:")
    for book in books:
        book_id, title, author, available = book.strip().split(",")
        status = "Available" if available == "Yes" else "Borrowed"
        print(f"ID: {book_id}, Title: {title}, Author: {author}, Status: {status}")

def borrow_book():
    view_books()

    book_id = input("Enter book ID to borrow: ").strip()
    borrower = input("Enter your name: ").strip()

    with open(BOOKS_FILE, "r") as f:
        books = f.readlines()

    header, book_records = books[0], books[1:]

    updated_books = []
    borrowed = False

    for book in book_records:
        b_id, title, author, available = book.strip().split(",")

        if b_id == book_id and available == "Yes":
            updated_books.append(f"{b_id},{title},{author},No\n")
            borrowed = True

            with open(BORROWED_FILE, "a") as bf:
                bf.write(f"{b_id},{borrower},{datetime.now().strftime('%Y-%m-%d')},\n")

            print(f"Book '{title}' borrowed by {borrower}!")
        else:
            updated_books.append(book)

    if not borrowed:
        print("Book not available or invalid ID.")

    with open(BOOKS_FILE, "w") as f:
        f.write(header)
        f.writelines(updated_books)

def return_book():
    book_id = input("Enter book ID to return: ").strip()

    with open(BOOKS_FILE, "r") as f:
        books = f.readlines()

    header, book_records = books[0], books[1:]

    updated_books = []
    returned = False

    for book in book_records:
        b_id, title, author, available = book.strip().split(",")

        if b_id == book_id and available == "No":
            updated_books.append(f"{b_id},{title},{author},Yes\n")
            returned = True

            # Update borrowed records
            with open(BORROWED_FILE, "r") as bf:
                borrowed_records = bf.readlines()

            with open(BORROWED_FILE, "w") as bf:
                bf.write(borrowed_records[0])
                for record in borrowed_records[1:]:
                    r_id, borrower, borrow_date, return_date = record.strip().split(",")

                    if r_id == book_id and not return_date:
                        bf.write(f"{r_id},{borrower},{borrow_date},{datetime.now().strftime('%Y-%m-%d')}\n")
                    else:
                        bf.write(record)

            print(f"Book '{title}' returned successfully!")
        else:
            updated_books.append(book)

    if not returned:
        print("Invalid book ID or book not borrowed.")

    with open(BOOKS_FILE, "w") as f:
        f.write(header)
        f.writelines(updated_books)

def view_borrowed_books():
    with open(BORROWED_FILE, "r") as f:
        records = f.readlines()[1:]

    print("\nBorrowed Books Record:")
    for record in records:
        book_id, borrower, borrow_date, return_date = record.strip().split(",")
        return_date = return_date if return_date else "Not Returned"
        print(f"Book ID: {book_id}, Borrower: {borrower}, Borrowed On: {borrow_date}, Returned On: {return_date}")

def main():
    initialize_files()

    while True:
        print("\nLibrary Management System")
        print("1. Add Book")
        print("2. View Books")
        print("3. Borrow Book")
        print("4. Return Book")
        print("5. View Borrowed Books")
        print("6. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == '1':
            add_book()
        elif choice == '2':
            view_books()
        elif choice == '3':
            borrow_book()
        elif choice == '4':
            return_book()
        elif choice == '5':
            view_borrowed_books()
        elif choice == '6':
            print("Exiting... Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
