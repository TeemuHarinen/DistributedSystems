# Basic functionality from video. URL: https://www.youtube.com/watch?v=3UOyky9sEQY, Simple TCP Chat Room in Python
import socket
import threading

localhost = '127.0.0.1'
port = 6262
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
custom_ip = input("Enter IP address (default is 127.0.0.1): ")
custom_port = input("Enter port number (default is 6262): ")
if custom_ip:
    localhost = custom_ip
if custom_port:
    port = int(custom_port)
try:
    client.connect((localhost, port))
except:
    print("Failed to connect to server. Please ensure correct IP and port number.")
    exit(0)

name = input("Enter your name: ")
print(
    '''
    Welcome to the chat room!

    Type your message and press enter to send it.
    /join (channel name) to join a channel
    /leave to leave a channel
    /message (username) to send a private message
    /exit to close the program
    '''
)
def receive():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message == 'CALL_NAME':
                client.send(name.encode('utf-8')) # Answer with client's name if server requests it
            else:
                print(message)
        except:
            print("Closing connection")
            client.close()
            break

def write():
    while True:
        text=input("")
        message = '{}:{}'.format(name, text)
        client.send(message.encode('utf-8'))
        if text == '/exit':
            client.close()
            exit(0)

receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()


