import socket
import threading

# Server configuration
HOST = '127.0.0.1'  # Localhost
PORT = 12345        # Port to bind

# List to keep track of clients
clients = []

# Function to broadcast messages to all clients
def broadcast(message, sender_socket):
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message)
            except:
                # Remove client if sending fails
                clients.remove(client)

# Function to handle individual client connections
def handle_client(client_socket):
    while True:
        try:
            message = client_socket.recv(1024)
            if not message:
                break
            broadcast(message, client_socket)
        except:
            break

    # Remove client and close connection
    clients.remove(client_socket)
    client_socket.close()

# Setting up the server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(5)
print(f"Server listening on {HOST}:{PORT}")

while True:
    client_socket, client_address = server.accept()
    print(f"New connection from {client_address}")
    clients.append(client_socket)

    # Start a new thread to handle the client
    thread = threading.Thread(target=handle_client, args=(client_socket,))
    thread.start()
