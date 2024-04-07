# Basic functionality from video. URL: https://www.youtube.com/watch?v=3UOyky9sEQY, Simple TCP Chat Room in Python
import threading
import socket

host = '127.0.0.1'
port = 6262

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # IPv4, TCP connection
server.bind((host, port))
server.listen()

clients = []
nicknames = []
channels = {}

# Used to broadcast message to all clients in channel
def broadcast_to_channel(channel, message, client):
    if channel not in channels:
        return None
    for client in channels[channel]:
        client.send(message.encode('utf-8'))
    return 0

def join_channel(client, channel, nickname):
    if channel in channels:
        channels[channel].append(client)
        broadcast_to_channel(channel, f"{nickname} joined the channel", client)

        # Server logs
        print(f"{nickname} joined channel: {channel}")
    else:
        channels[channel] = [client]
        broadcast_to_channel(channel, f"{nickname} joined the channel", client)
        print(f"{nickname} joined channel: {channel}")
    

def remove_from_channel(client, channel, nickname):
    for clients in channels.values():
        if client in clients:
            clients.remove(client)
            broadcast_to_channel(channel, f"{nickname} left the channel", client)
            client.send(f"You left the channel {channel}".encode('utf-8'))
            print(f"{nickname} left channel: {channel}")
            break
    return 0

# Utility function to find the channel a client is in
def find_channel(client):
    for channel, clients in channels.items():
        if client in clients:
            return channel
    return 0

# Utility function to find the client based off name (for private messages)
def find_user(userToFind):
    for name in nicknames:
        if name[0] == userToFind:
            return name[1]
    return None

# Main function to handle client messages
def handle(client):
    while True:
        message=client.recv(1024).decode('utf-8')
        nickname, text = message.split(':')
        if text == '/exit':
            print(f"{nickname} disconnected")
            broadcast_to_channel(find_channel(client), f"{nickname} has disconnected", client) # Notify channel of disconnect
            client.close()
            break
        if text.startswith('/message '): # Private message
            _, target, message = text.split(' ', 2) #Parse the target and message
            print(target)
            recipient = find_user(target) # Find client based on name
            if recipient != None:
                recipient.send(f"Private message from {nickname}: {message}".encode('utf-8'))
            else:
                client.send("User not found".encode('utf-8'))
        elif text.startswith('/join '):
            channel = message.split(' ', 1)[1]
            remove_from_channel(client, channel, nickname) # Remove from current channel
            join_channel(client, channel, nickname)
        elif text.startswith('/leave'):
            remove_from_channel(client, channel, nickname)
        else:
            if find_channel(client) == None:
                client.send("You are not in a channel, type /join (channel) to join".encode('utf-8'))
            else:
                broadcast_to_channel(find_channel(client), message, client)

def receive():
    while True:
        client, address = server.accept()
        print(f"New client connected with {str(address)}!")

        client.send('CALL_NAME'.encode('utf-8')) # Send the nickname request
        nickname = client.recv(1024).decode('utf-8') # Receive the nickname from client
        nicknames.append((nickname, client))
        clients.append(client)
        print(f"Client joined server: {nickname}")
        thread = threading.Thread(target=handle, args=(client,)) # Enables parallel processing of clients
        thread.start()                                           # target=handle executes the handle function with the client as an argument

print(f"Server running at: {host}:{port}")
receive()