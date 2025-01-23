
import socket

# Create a socket object
    # both client and server must have the same socket type (in this example it is TCP)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Get local machine name
host = 'localhost'  # IP addresss
port = 12345

# Bind to the port to listen at this specific port
server_socket.bind((host, port))

# Queue up to 5 requests
server_socket.listen(5) # default value of 3 if you don't include a number as a param

print("Server listening...")

while True:
    # Establish a connection
    client, addr = server_socket.accept()       # accepts the connection from the specific client
    # client: 
    # addr: the address connected to the server from client
    print(f"Got a connection from {addr}")

    # Receive data from the client
     # '.recv(max size of message [in bytes])' receive the client message, 
     # if the client message is larger than this, use a loop to get the rest of the chuncks
     # the message is encoded, so you'll need to decode it.
    data = client.recv(1024).decode()
    print(f"Received '{data}' from the client")

    # Send a reply to the client
    client.send('Thank you for connecting'.encode())

    # Close the connection with the client
    client.close()
    break  # Remove this to keep the server running for multiple connections

# RUNNING
# you need to open 2 different terminals, 1 for client, 1 for server
# run the server first then client (you'll get an error otherwise -> connection refused)

# if you terminate server and run it again right after, the OS is still freeing up
# that port so it will give an error saying it is not free (just wait some time before running again)

# to run python file: 'python <filename>.py'
