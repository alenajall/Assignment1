books = {}  # Dictionary: {ISBN: (title, author, genre, total_copies)}
members = []  # List: [(member_id, name, email, borrowed_books), ...]
genres = ("Fiction", "Non-Fiction", "Sci-Fi")  # Tuple of valid genres


def add_book(isbn, title, author, genre, total_copies):
    if isbn in books:
        print("Error: ISBN already exists.")
        return
    if genre not in genres:
        print("Error: Invalid genre.")
        return
    if total_copies < 0:
        print("Error: Total copies cannot be negative.")
        return
    books[isbn] = (title, author, genre, total_copies)
    print(f"Book '{title}' added successfully with ISBN {isbn}.")


def add_member(member_id, name, email):
    for member in members:
        if member[0] == member_id:
            print("Error: Member ID already exists.")
            return
    members.append((member_id, name, email, []))
    print(f"Member '{name}' added successfully with ID {member_id}.")


def search_book(query):
    results = []
    for isbn, (title, author, genre, total_copies) in books.items():
        if query.lower() in title.lower() or query.lower() in author.lower():
            results.append((isbn, title, author, genre, total_copies))
    if results:
        for result in results:
            print(
                f"Found: ISBN {result[0]}, Title: {result[1]}, Author: {result[2]}, Genre: {result[3]}, Copies: {result[4]}")
    else:
        print("No books found matching the query.")


def update_book(isbn, title, author, genre, total_copies):
    if isbn not in books:
        print("Error: ISBN does not exist.")
        return
    if genre not in genres:
        print("Error: Invalid genre.")
        return
    if total_copies < 0:
        print("Error: Total copies cannot be negative.")
        return
    books[isbn] = (title, author, genre, total_copies)
    print(f"Book with ISBN {isbn} updated successfully.")


def delete_book(isbn):
    if isbn not in books:
        print("Error: ISBN does not exist.")
        return
    books.pop(isbn)
    print(f"Book with ISBN {isbn} deleted successfully.")


def borrow_book(member_id, isbn):
    # Check if member exists
    member_found = None
    for member in members:
        if member[0] == member_id:
            member_found = member
            break
    if not member_found:
        print("Error: Member ID does not exist.")
        return

    # Check if book exists and has copies
    if isbn not in books:
        print("Error: ISBN does not exist.")
        return
    title, author, genre, total_copies = books[isbn]
    if total_copies <= 0:
        print("Error: No copies available to borrow.")
        return

    # Update book copies and member's borrowed list
    books[isbn] = (title, author, genre, total_copies - 1)
    member_found[3].append(isbn)  # Add ISBN to member's borrowed_books
    print(
        f"Book with ISBN {isbn} borrowed by member {member_id} successfully.")


def return_book(member_id, isbn):
    # Check if member exists
    member_found = None
    for member in members:
        if member[0] == member_id:
            member_found = member
            break
    if not member_found:
        print("Error: Member ID does not exist.")
        return

    # Check if book exists
    if isbn not in books:
        print("Error: ISBN does not exist.")
        return
    title, author, genre, total_copies = books[isbn]

    # Check if member borrowed the book
    if isbn not in member_found[3]:
        print("Error: Member did not borrow this book.")
        return

    # Update book copies and remove ISBN from member's borrowed list
    books[isbn] = (title, author, genre, total_copies + 1)
    member_found[3].remove(isbn)
    print(
        f"Book with ISBN {isbn} returned by member {member_id} successfully.")


def run_tests():
    # Test 1: Add a book
    books.clear()
    members.clear()
    add_book("123", "Python Basics", "escanor", "Non-Fiction", 5)
    assert "123" in books, "Test 1 Failed: Book not added"
    print("Test 1 Passed: Book added successfully")

    # Test 2: Add duplicate ISBN
    add_book("123", "Duplicate Book", "senku", "Fiction", 3)
    assert len(books) == 1, "Test 2 Failed: Duplicate ISBN not handled"
    print("Test 2 Passed: Duplicate ISBN handled")

    # Test 3: Borrow a book
    add_member("M001", "jin sakai", "sakaijin@email.com")
    borrow_book("M001", "123")
    title, author, genre, copies = books["123"]
    assert copies == 4, "Test 3 Failed: Borrowing not reducing copies"
    print("Test 3 Passed: Book borrowed successfully")

    # Test 4: Borrow when no copies left
    for _ in range(4):
        borrow_book("M001", "123")
    borrow_book("M001", "123")
    assert books["123"][3] == 0, "Test 4 Failed: Borrowing with no copies"
    print("Test 4 Passed: Borrowing with no copies handled")

    # Test 5: Return a book
    return_book("M001", "123")
    title, author, genre, copies = books["123"]
    assert copies == 1, "Test 5 Failed: Return not increasing copies"
    print("Test 5 Passed: Book returned successfully")


if __name__ == "__main__":
    run_tests()
