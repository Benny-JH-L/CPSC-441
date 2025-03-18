import socket
import threading

# Server details
HOST = '127.0.0.1'
PORT = 12345

# Function to receive messages from server
def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            print(message)
        except:
            break

# Connect to server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

# Start thread to listen for incoming messages
thread = threading.Thread(target=receive_messages, args=(client,))
thread.start()

# Sending messages
while True:
    message = input()
    if message.lower() == 'exit':
        break
    client.send(message.encode('utf-8'))

client.close()
