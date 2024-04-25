# Server.py
from xmlrpc.server import SimpleXMLRPCServer
from socketserver import ThreadingMixIn
import uuid

# Define a custom threaded XML-RPC server class
class ThreadedXMLRPCServer(ThreadingMixIn, SimpleXMLRPCServer):
    pass

# Initialize a list of books, users, and sessions
books = [
    {"id": 1, "title": "Book A", "author": "Author A", "price": 15.99},
    {"id": 2, "title": "Book B", "author": "Author B", "price": 25.50},
    {"id": 3, "title": "Book C", "author": "Author C", "price": 17.75}
]
users = {}
sessions = {}

# Function to list all available books
def list_books():
    return '\n'.join(f"{book['id']} - {book['title']} by {book['author']}, ${book['price']}" for book in books) #AI Generated

# Function to add a new book to the collection
def add_book(title, author, price, session_id):
    global books
    if session_id not in sessions:
        return "Please login first."
    book_id = len(books) + 1
    books.append({"id": book_id, "title": title, "author": author, "price": price})
    return f"Added book {title} by {author} for ${price}."

# Function to allow a user to purchase a book
def buy_book(session_id, book_id):
    global books  
    if session_id not in sessions:
        return "Please login first."
    user_id = sessions.get(session_id)
    book = next((b for b in books if b['id'] == book_id), None) #AI Generated
    if book:
        books = [b for b in books if b['id'] != book_id] 
        result = add_book_to_user_by_id(users, user_id, book)
        return result if result else f"Purchased book: {book['title']} by {book['author']}."
    return "Book not available."

# Function to add a book to a user's collection by their ID
def add_book_to_user_by_id(users, user_id, book):
    for user_info in users.values():
        if user_info['user_id'] == user_id:
            user_info['books'].append(book)
            return f"Book added to {user_info['username']}'s collection."
    return "User not found."

# Function to list books owned by a user
def list_owned_books(session_id):
    user_id = sessions.get(session_id)
    if not user_id:
        return "Please login to see your books."
    
    # Find user by user_id
    for user_info in users.values():
        if user_info['user_id'] == user_id:
            owned_books = user_info['books']
            if not owned_books:
                return "You do not own any books."
            return '\n'.join([f"{book['id']} - {book['title']} by {book['author']}, ${book['price']}" for book in owned_books]) #AI Generated

    return "User not found."

# Function to search for books based on a keyword
def search_books(keyword):
    keyword = keyword.lower()
    found_books = [book for book in books if keyword in book['title'].lower() or keyword in book['author'].lower()] #AI Generated
    if not found_books:
        return "No books found matching your criteria."
    return '\n'.join([f"{book['id']} - {book['title']} by {book['author']}, ${book['price']}" for book in found_books])

# Function to log in a user
def login_user(username, session_id):
    if username in users:
        user_id = users[username]['user_id']
    else:
        user_id = uuid.uuid4().hex
        users[username] = {"user_id": user_id, "username": username, "books": []}
    sessions[session_id] = user_id
    return f"Logged in as {username}"

# Function to generate a unique session ID
def generate_session_id():
    return uuid.uuid4().hex

# Function to log out a user
def logout_user(session_id):
    if session_id in sessions:
        sessions[session_id] = None
        return "Logged out."
    return "Invalid session ID."

# Function to start the XML-RPC server
def start_server():
    port = 8000
    server = ThreadedXMLRPCServer(("localhost", port), allow_none=True)
    server.register_function(list_books, "list_books")
    server.register_function(add_book, "add_book")
    server.register_function(buy_book, "buy_book")
    server.register_function(login_user, "login_user")
    server.register_function(list_owned_books, "list_owned_books")
    server.register_function(search_books, "search_books")
    server.register_function(logout_user, "logout_user")
    server.register_function(generate_session_id, "generate_session_id")
    print(f"Server started on port: {port}")
    server.serve_forever()

# Entry point to start the server
if __name__ == "__main__":
    start_server()
