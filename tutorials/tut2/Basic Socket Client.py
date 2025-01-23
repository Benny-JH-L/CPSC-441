
import socket

# Create a socket object
    # both client and server must have the same socket type (in this example it is TCP)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Define the server address and port to connect to
host = 'localhost' # IP address
port = 12345

# Connect to the server
client_socket.connect((host, port))

# Send data to the server
message = "Hello from the client!"
client_socket.send(message.encode()) # need to use 'encode()', cannot send a string to socket

# Receive the server's response
 # '.recv(max size of message [in bytes])' receive the server message, 
 # if the server message is larger than this, use a loop to get the rest of the chuncks
 # the message is encoded, so you'll need to decode it.
response = client_socket.recv(1024).decode()
print(f"Received from server: {response}")  # 'f' in the beginning formats the printing

# Close the connection
client_socket.close()
