
import socket
import threading

# Server configuration
SERVER_HOST = 'localhost'
SERVER_PORT = 12345
RECV_SIZE = 1024
CLIENT_TIMEOUT = 60
CHECK_USER = "CHECK_UNIQUE_USER"

def display_messages(client_socket):
    
    while True:
        response = client_socket.recv(RECV_SIZE)
        if not response:
            break
        else:
            print(response)
    
def start_client():
    """ Start the client and connect to the server. """
    # client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
       
        client_socket.settimeout(CLIENT_TIMEOUT) # set timeout
        numConnectionTries = 0
        connectedWithServer = False
        
        # attempt a connection to the server
        print("Connecting to server...")
        while(numConnectionTries < 3 and not connectedWithServer):    # try 3 connection attempts
            try:
                client_socket.connect((SERVER_HOST, SERVER_PORT))
                connectedWithServer = True          # server connected
            except ConnectionRefusedError:          # connection timed out, try again
                numConnectionTries += 1
                print(f"Connection refused (Refused: {numConnectionTries})...")
                if (numConnectionTries < 3):
                    print("Retrying...")
        
        # connection refused 3 times
        if (numConnectionTries >= 3):
            print("Could not connect to server, exiting the client....")
            return
        
        print("Connected to server...")
        
        # check if the user name exists already
        USER_NAME = ""
        while USER_NAME == "":
            user_name = input("Please enter a username: ")
            message = CHECK_USER
            client_socket.send(message.encode())
            response = client_socket.recv(RECV_SIZE).decode()
            
            if (response != "EXIST"):
                USER_NAME = user_name
                break
            print("Username already exists...")
            
        # start thread that will output server responses
        print("creating thread...") #debug
        threading.Thread(target=display_messages, args=client_socket)
        
        # Client interaction loop as long as client is still connected to the server
        while connectedWithServer:
            
            # server_response = client_socket.recv(RECV_SIZE).decode()
            # print(server_response)
            
            input_string = input()
            
            if (input_string == "@bamboo"):
                print("randome panda fact fro server...")
            elif (input_string == "@grove"):
                print("list of users: (only print to this user)")
            elif (input_string == "@leaves:"):
                print("Exiting...")
                break
                
            # send `message` and check for timeout errors
            numTimeOuts = 0
            while (numTimeOuts < 3):
                try:
                    message = f"{USER_NAME}|{input_string}"     
                    client_socket.send(message.encode())
                    
                    # Wait for and display the server response
                    response = client_socket.recv(RECV_SIZE).decode()
                    
                    print(response)
                    break
                except socket.timeout:      # checking client timeout
                    numTimeOuts += 1
                    print(f"Server timeout ({numTimeOuts} timeouts)...")
                    if (numTimeOuts < 3):   # print `retying` to let client know another attempt is being made
                        print("Retrying...")
                except ConnectionAbortedError:      # if the server closes the connection due to the client taking too long
                    print("Took too long to respond, server closed connection...\nExiting....")
                    connectedWithServer = False     # the client took to long to send a message and the server closed the connection
                    break
            
            # print server timeout if we've attempted 3 times sending a message 
            if (numTimeOuts >= 3):
                print("Server timed out, exiting the client....")
                return

            
if __name__ == "__main__":
    start_client()

