
# Assignment 3: Create a Panda-Chat
#     CPSC 441 Winter 2025 | Benny Liang | 30192142

import socket
import threading
import random
import logging
from collections import Counter

# Set up basic logging configuration
logging.basicConfig(filename='server_log.txt', level=logging.INFO, format='%(asctime)s - %(message)s')

# Constants for the server configuration
HOST = 'localhost'
PORT = 12345

RECV_SIZE = 1024
CHAT_ROOM_SIZE = 5
LIST_OF_CLIENTS = []
LIST_OF_USERNAMES = []  # turn this into a set

REQUEST_CHECK_UNIQUE_USERNAME = "CHECK_UNIQUE_USER"
REQUEST_SEND_MESSAGE = "SEND_MESSAGE"
REQUEST_GROVE = "@grove"
REQUEST_EXIT = "EXIT"

LIST_PANDA_THEMED_DECORATIONS = [
    "\U0001F43C", # 🐼
    "\U0001F38D", # 🎍
    "\U0001F43E", # 🐾
    "\U0001F96C"  # 🥬
    ]


def is_unique_username(client_socket, username):
    """
    [Server] Checks if the user name is unique, ie. if there is no client already with this username.
    """
    
    for user in LIST_OF_USERNAMES:
        if (username == user):
            return "false" # is not a unique username
    
    LIST_OF_USERNAMES.append(username)
    joined_message = f"{username} joined the chat! {LIST_PANDA_THEMED_DECORATIONS[0]}{LIST_PANDA_THEMED_DECORATIONS[2]}" 
    send_message_to_chatroom(client_socket, username, joined_message) # announce a new user joined to all the clients
    
    print(f"[SERVER] {username} joined the chat.")  # debug
    return "true" # is a unique username


def send_message_to_chatroom(client_socket, username, message):
    """
    Sends the `message` to all the clients. (ie updates the chat room with the new message)
    """
    message_from_other_user = f"{username} > {message}"  # format message 
    
    # send the `message_from_other_user` to all other users (excluding the one who sent it)
    for client in LIST_OF_CLIENTS:
        if client != client_socket:
            try:
                client.send(message_from_other_user.encode())
            except:                             # client no longer exists
                LIST_OF_CLIENTS.remove(client)  # remove the non_existant client

def handle_client(client_socket, client_address):
    """ 
    Handle incoming client requests. 
    """
    
    logging.info(f"Connection from {client_address}")
    print(f"Connection from {client_address}")
    
    try:
        while True:
            client_message = client_socket.recv(RECV_SIZE).decode()
            
            if not client_message:
                break
                
            print(f"received client message: {client_message}")
            logging.info(f"Server received client message <{client_message}> from [{client_address}]")
            
            # incoming message will be in the form of (excluding the spaces): "<request type> | <user name> | <message>"
            request_type, username, message = client_message.strip().split("|")
            
            if request_type == REQUEST_EXIT:
                LIST_OF_USERNAMES.remove(username)
                leave_message = f"{username} has left..."
                send_message_to_chatroom(client_socket, "Server", leave_message)        # notify the chat room this user left \
                print(f"[SERVER] {username} has left.")
                logging.info(f"[{client_address}] | {username} has left.")
                break
            
            # send the `message` to the chat
            if (request_type == REQUEST_SEND_MESSAGE):
                send_message_to_chatroom(client_socket, username, message)
                print("[SERVER] sent message to all clients")     # debug
                logging.info(f"[{client_address}] | sent message to chat: {message}")
                
            # checking if the username entered is unique
            elif (request_type == REQUEST_CHECK_UNIQUE_USERNAME):
                result = is_unique_username(client_socket, username).strip()
                print(f"[SERVER] {username} is unique: {result}")  # debug
                client_socket.send(result.encode())     # tell client the if the username is unique
                logging.info(f"[{client_address}] | username <{message}> is unique: ")
                
            elif (request_type == REQUEST_GROVE):
                # formmated_list_of_connected_users = "@grove|----Connected users----\n"
                formmated_list_of_connected_users = "----Connected users----\n"
                
                for connected_user in LIST_OF_USERNAMES:
                    formmated_list_of_connected_users = f"{formmated_list_of_connected_users}[{connected_user}]\n"
                
                client_socket.send(formmated_list_of_connected_users.encode())
                print("[SERVER] grove sent...")
                logging.info(f"[{client_address}] | sent @grove {formmated_list_of_connected_users}.")
                
            else:
                print("_____INVALID REQUEST TYPE_____")
        
        client_socket.close()
        logging.info(f"Closed connection with {client_address}")
        print(f"Closed connection with {client_address}")
    finally:
        # Close the client connection
        client_socket.close()
        logging.info(f"Closed connection with {client_address}")
        print(f"Closed connection with {client_address}")
    
def start_server():
    """ Start the server and listen for incoming connections. """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen(CHAT_ROOM_SIZE)
        logging.info(f"Server started and listening on {HOST}:{PORT}")
        print(f"Server started and listening on {HOST}:{PORT}")
        
        while True:
            # Accept new client connections and start a thread for each client
            client_socket, client_address = server_socket.accept()
            LIST_OF_CLIENTS.append(client_socket)
            threading.Thread(target=handle_client, args=(client_socket, client_address)).start() # include error checking for threads -> ex. terminate unexpectedly, or when server shuts down. 

if __name__ == '__main__':
    start_server()
