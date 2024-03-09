import xmlrpc.client
from datetime import datetime

class Client:
    def __init__(self):
        try:
            self.server = xmlrpc.client.ServerProxy('http://localhost:8000')
        except Exception as e:
            print(f"Failed to connect to server: {e}")
            exit(1)

    def send_data(self):
        try:
            topic = input("Enter topic: ")
            text = input("Enter text: ")
            timestamp = datetime.now().isoformat()
            print(self.server.save_data(topic, text, timestamp))
        except Exception as e:
            print(f"Failed to send data: {e}")

    def get_data(self):
        try:
            topic = input("Enter topic: ")
            print(self.server.get_data(topic))
        except Exception as e:
            print(f"Failed to get data: {e}")
    
    def query_wikipedia(self):
        search_term = input("Enter search term: ")
        result = self.server.query_wikipedia(search_term)
        print(f"Wikipedia link: {result}")
        topic = input("Enter topic to append data to: ")
        print(self.server.save_data(topic, result, datetime.now().isoformat()))

while True:
    client = Client()
    print("\n1. Send data")
    print("2. Get data")
    print("3. Query Wikipedia")
    print("4. Exit\n")
    choice = input("Enter your choice: ")

    if choice == '1':
        client.send_data()
    elif choice == '2':
        client.get_data()
    elif choice == '3':
        client.query_wikipedia()
    elif choice == '4':
        break
    else:
        print("Invalid choice. Please enter 1, 2, 3 or 4.")
    

