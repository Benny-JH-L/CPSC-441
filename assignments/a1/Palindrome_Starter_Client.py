
# Assignment 1: Advanced Palindrome Check Server-Client Application
#     CPSC 441 Winter 2025 | Benny Liang | 30192142

import socket

# config for caeser cipher
SHIFT = 7

# Server configuration
SERVER_HOST = 'localhost'
SERVER_PORT = 12345

# handle connection, data transmisson (issues during data send/recieve, such as broken pipes or timeouts), and invalid input (ex. NO NUMBERS, empty string), errors 
# display messages to enhance user experience 
# (for both serve/client?) -> see assignment details
def start_client():
    """ Start the client and connect to the server. """
    # client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
       
        client_socket.settimeout(5) # set 5 second timeout
        numConnectionTries = 0
        connectedWithServer = False
        
        # attempt a connection to the server
        print("Connecting to server...")
        while(numConnectionTries < 3 and not connectedWithServer):    # try 3 connection attempts
            try:
                client_socket.connect((SERVER_HOST, SERVER_PORT))
                connectedWithServer = True  # server connected
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
        # Client interaction loop as long as client is still connected to the server
        while connectedWithServer:
            # Display the menu and get user input
            print("\nMenu:")
            print("1. Simple Palindrome Check")
            print("2. Complex Palindrome Check")
            print("3. Exit")
            choice = input("Enter choice (1/2/3): ").strip()

            checkType = ""
            input_string = ""

            if choice == '1':
                input_string = input("Enter the string to check: ")
                checkType = "simple"
                # message = f"simple|{input_string}"
                
            elif choice == '2':
                input_string = input("Enter the string to check: ")
                checkType = "complex"
                # message = f"complex|{input_string}"
                
            elif choice == '3':
                print("Exiting the client...")
                break
            
            else:   # invalid choice, ask for another input
                print(f"`{choice}` is an invalid choice...")
                continue
            
            # send `message` and check for timeout errors
            numTimeOuts = 0
            while (numTimeOuts < 3):
                try:
                    input_string = caesar_cipher(input_string)  # encrypt `input_string``
                    message = f"{checkType}|{input_string}"     
                    client_socket.send(message.encode())
                    
                    # Wait for and display the server response
                    response = client_socket.recv(1024).decode()
                    response = caesar_cipher(response)  # decrypt `response` from server
                    
                    print(f"---Server response---\n{response}")
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

# simple cipher to encrypt/decrypt text
def caesar_cipher(text):
    result = ""
    for char in text:
        if char.isalpha():  # Check if it's a letter
            shift_base = ord('A') if char.isupper() else ord('a')
            result += chr((ord(char) - shift_base + SHIFT) % 26 + shift_base)
        else:
            result += char  # Keep non-alphabet characters unchanged
    
    return result
            
if __name__ == "__main__":
    start_client()

