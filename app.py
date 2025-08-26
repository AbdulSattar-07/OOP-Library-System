# app.py
import streamlit as st
from datetime import datetime

# ---------------------------
# Classes
# ---------------------------
class Person:
    def __init__(self, name, age, contact_number):
        self.name = name
        self.age = age
        self.contact_number = contact_number

    def get_details(self):
        return f"Name: {self.name}, Age: {self.age}, Contact: {self.contact_number}"

    def update_contact(self, new_contact_number):
        self.contact_number = new_contact_number
        return f"Updated Contact Number: {self.contact_number}"


class Book:
    def __init__(self, book_id, title, author, availability=True):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.availability = availability

    def check_availability(self):
        return self.availability

    def update_availability(self, status):
        self.availability = status


class LibraryMember(Person):
    def __init__(self, name, age, contact_number, member_id):
        super().__init__(name, age, contact_number)
        self.member_id = member_id
        self.borrowed_books = []

    def borrow_book(self, book):
        if book.check_availability():
            self.borrowed_books.append(book)
            book.update_availability(False)
            return f"{self.name} borrowed {book.title}"
        else:
            return f"{book.title} is not available"

    def return_book(self, book):
        if book in self.borrowed_books:
            self.borrowed_books.remove(book)
            book.update_availability(True)
            return f"{self.name} returned {book.title}"
        else:
            return f"{self.name} does not have {book.title}"

    def view_borrowed_books(self):
        if not self.borrowed_books:
            return "No borrowed books."
        return ", ".join([book.title for book in self.borrowed_books])


class Librarian(Person):
    def __init__(self, name, age, contact_number, employee_id):
        super().__init__(name, age, contact_number)
        self.employee_id = employee_id

    def add_book(self, book, library):
        library.books.append(book)
        return f"Book '{book.title}' added."

    def remove_book(self, book_id, library):
        for book in library.books:
            if book.book_id == book_id:
                library.books.remove(book)
                return f"Book '{book.title}' removed."
        return f"No book with ID {book_id} found."

    def add_member(self, member, library):
        library.members.append(member)
        return f"Member '{member.name}' added."

    def remove_member(self, member_id, library):
        for member in library.members:
            if member.member_id == member_id:
                library.members.remove(member)
                return f"Member '{member.name}' removed."
        return f"No member with ID {member_id} found."


class Library:
    def __init__(self):
        self.books = []
        self.members = []
        self.librarians = []

    def display_books(self):
        if not self.books:
            return "No books in library."
        return [f"{b.book_id} - {b.title} by {b.author} ({'Available' if b.availability else 'Borrowed'})" for b in self.books]

    def register_member(self, member):
        self.members.append(member)
        return f"Member '{member.name}' registered."

    def deregister_member(self, member_id):
        for member in self.members:
            if member.member_id == member_id:
                self.members.remove(member)
                return f"Member '{member.name}' deregistered."
        return f"No member with ID {member_id}."

    def find_book(self, book_id):
        for book in self.books:
            if book.book_id == book_id:
                return book
        return None

    def lend_book(self, book_id, member_id):
        book = self.find_book(book_id)
        for member in self.members:
            if member.member_id == member_id and book:
                return member.borrow_book(book)
        return "Invalid book or member."

    def return_book(self, book_id, member_id):
        book = self.find_book(book_id)
        for member in self.members:
            if member.member_id == member_id and book:
                return member.return_book(book)
        return "Invalid book or member."


# ---------------------------
# Streamlit App
# ---------------------------
st.set_page_config(page_title="Library Management", layout="wide")

if "library" not in st.session_state:
    st.session_state.library = Library()
if "logs" not in st.session_state:
    st.session_state.logs = []

def log(msg):
    timestamp = datetime.now().strftime("%H:%M:%S")
    st.session_state.logs.append(f"[{timestamp}] {msg}")

st.title("📚 Library Management System")

menu = st.sidebar.radio("Menu", ["Add Book", "Remove Book", "Add Member", "Remove Member",
                                 "Borrow Book", "Return Book", "Show Books", "Show Members", "Logs"])

# ---------------------------
# Menu Actions
# ---------------------------
if menu == "Add Book":
    st.header("➕ Add Book")
    book_id = st.text_input("Book ID")
    title = st.text_input("Title")
    author = st.text_input("Author")
    if st.button("Add Book"):
        if book_id and title and author:
            book = Book(book_id, title, author)
            st.session_state.library.books.append(book)
            st.success(f"Book '{title}' added.")
            log(f"Book '{title}' added.")
        else:
            st.error("Please fill all fields.")

elif menu == "Remove Book":
    st.header("➖ Remove Book")
    book_id = st.text_input("Book ID to Remove")
    if st.button("Remove"):
        result = None
        for b in st.session_state.library.books:
            if b.book_id == book_id:
                st.session_state.library.books.remove(b)
                result = f"Book '{b.title}' removed."
                break
        if result:
            st.success(result)
            log(result)
        else:
            st.error("Book not found.")

elif menu == "Add Member":
    st.header("➕ Add Member")
    member_id = st.text_input("Member ID")
    name = st.text_input("Name")
    age = st.number_input("Age", min_value=1, step=1)
    contact = st.text_input("Contact")
    if st.button("Add Member"):
        if member_id and name and contact:
            m = LibraryMember(name, age, contact, member_id)
            st.session_state.library.members.append(m)
            st.success(f"Member '{name}' added.")
            log(f"Member '{name}' added.")
        else:
            st.error("Fill all fields.")

elif menu == "Remove Member":
    st.header("➖ Remove Member")
    member_id = st.text_input("Member ID to Remove")
    if st.button("Remove Member"):
        result = None
        for m in st.session_state.library.members:
            if m.member_id == member_id:
                st.session_state.library.members.remove(m)
                result = f"Member '{m.name}' removed."
                break
        if result:
            st.success(result)
            log(result)
        else:
            st.error("Member not found.")

elif menu == "Borrow Book":
    st.header("📖 Borrow Book")
    member_id = st.text_input("Member ID")
    book_id = st.text_input("Book ID")
    if st.button("Borrow"):
        result = st.session_state.library.lend_book(book_id, member_id)
        st.info(result)
        log(result)

elif menu == "Return Book":
    st.header("📤 Return Book")
    member_id = st.text_input("Member ID")
    book_id = st.text_input("Book ID")
    if st.button("Return"):
        result = st.session_state.library.return_book(book_id, member_id)
        st.info(result)
        log(result)

elif menu == "Show Books":
    st.header("📚 All Books")
    books = st.session_state.library.display_books()
    if isinstance(books, list):
        st.table(books)
    else:
        st.info(books)

elif menu == "Show Members":
    st.header("👥 All Members")
    if not st.session_state.library.members:
        st.info("No members.")
    else:
        st.table([m.get_details() for m in st.session_state.library.members])

elif menu == "Logs":
    st.header("📝 Transaction Logs")
    if not st.session_state.logs:
        st.info("No logs yet.")
    else:
        for log_msg in reversed(st.session_state.logs):
            st.write(log_msg)
# streamlit run app.py
