# Client.py
import xmlrpc.client
import threading

# Connect to the XML-RPC server
server = xmlrpc.client.ServerProxy('http://localhost:8000')

# Main function to interact with the server
def main():
    session_id = server.generate_session_id()  # Generate a unique session ID for this client
    while True:
        # Display available commands
        print()
        print("Available commands:")
        print("1 - Login")
        print("2 - List books")
        print("3 - Add book")
        print("4 - Buy book")
        print("5 - My books")
        print("6 - Search books")
        print("7 - Exit")
        print()
        # Get user input for command
        cmd = input("Enter command number: ")
        if cmd == '1':
            # Login command
            username = input("Enter username: ")
            print(server.login_user(username, session_id))
        elif cmd == '2':
            # List books command
            print(server.list_books())
        elif cmd == '3':
            # Add book command
            title = input("Enter title: ")
            author = input("Enter author: ")
            price = float(input("Enter price: "))
            print(server.add_book(title, author, price, session_id))
        elif cmd == '4':
            # Buy book command
            book_id = int(input("Enter book ID to purchase: "))
            print(server.buy_book(session_id, book_id)) 
        elif cmd == '5':
            # List owned books command
            print(server.list_owned_books(session_id))
        elif cmd == '6': 
            # Search books command
            keyword = input("Enter search keyword (title or author): ")
            print(server.search_books(keyword))
        elif cmd == '7':
            # Logout and exit command
            print(server.logout_user(session_id))
            print("Exiting...")
            break

# Entry point to start the client thread
if __name__ == "__main__":
    # Start a new thread for each client connection
    client_thread = threading.Thread(target=main)
    client_thread.start()
