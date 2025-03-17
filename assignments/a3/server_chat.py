
import socket
import threading
import logging
from collections import Counter

# Set up basic logging configuration
logging.basicConfig(filename='server_log.txt', level=logging.INFO, format='%(asctime)s - %(message)s')

# Constants for the server configuration
HOST = 'localhost'
PORT = 12345
RECV_SIZE = 1024
CLIENT_TIMEOUT = 60
LIST_OF_CLIENTS = []
LIST_OF_USERNAMES = []
CHECK_USER = "CHECK_UNIQUE_USER"


def handle_client(client_socket, client_address):
    """ Handle incoming client requests. """
    logging.info(f"Connection from {client_address}")
    print(f"Connection from {client_address}")
    
    LIST_OF_CLIENTS.append(client_socket)
    
    client_socket.settimeout(CLIENT_TIMEOUT)  # Set timeout for receiving data
    numTimeouts = 0  # Initialize timeout counter
    username = ""

    try:
        
        # check unique username
        # asking_for_username -= True
        while (username != ""):
            client_data = client_socket.recv(RECV_SIZE).decode()
            user = client_data
            # user, message = client_data.split("|")
            
            if (is_unique_username(user)):
                username = user
                break
            else:
                response = "EXIST"
                client_socket.send(response.encode())
            
        while numTimeouts < 3:  # Allow up to 3 timeouts before closing connection
            try:
                # Receive data from the client
                client_data = client_socket.recv(RECV_SIZE).decode()
                message = client_data
                
                # log data recieved from specific client
                logging.info(f"Data recieved: <username:{username}, message:{message}> from {client_address}")
                print(f"Data recieved: <username:{username}, message:{message}> from {client_address}")
                
                if not client_data:  # Client has closed the connection
                    logging.info(f"Client {client_address} disconnected...")
                    print(f"Client {client_address} disconnected...")
                    break

                numTimeouts = 0 # reset count 
                
                # send this message to every client
                for i in range(0, len(LIST_OF_CLIENTS)):
                    if (LIST_OF_CLIENTS == client_socket):
                        continue
                    LIST_OF_CLIENTS[i].send(f"<{username}>: {message}")
                                
                logging.info(f"Sent response: <{client_data}> to {client_address}")
                print(f"Sent response: <{client_data}> to {client_address}")

            except socket.timeout:
                numTimeouts += 1
                logging.info(f"Client {client_address} timeout ({numTimeouts} timeouts)... Waiting...")
                print(f"Client {client_address} timeout ({numTimeouts} timeouts)... Waiting...")
        
        # print and log time out due to client not responding
        if (numTimeouts >= 3):
            logging.info(f"Max timeouts reached, closing connection with client {client_address}...")
            print(f"Max timeouts reached, closing connection with client {client_address}...")
        
    finally:
        # Close the client connection
        client_socket.close()
        logging.info(f"Closed connection with {client_address}")
        print(f"Closed connection with {client_address}")


def start_server():
    """ Start the server and listen for incoming connections. """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen(5)     # Listening to 5 clients
        logging.info(f"Server started and listening on {HOST}:{PORT}")
        print(f"Server started and listening on {HOST}:{PORT}")
        
        while True:
            # Accept new client connections and start a thread for each client
            client_socket, client_address = server_socket.accept()
            threading.Thread(target=handle_client, args=(client_socket, client_address)).start() # include error checking for threads -> ex. terminate unexpectedly, or when server shuts down. 

def is_unique_username(check_user):
    
    for i in range(0, len(LIST_OF_USERNAMES)):
        if (LIST_OF_USERNAMES[i] == check_user):
            return False
    
    return True

if __name__ == '__main__':
    start_server()
