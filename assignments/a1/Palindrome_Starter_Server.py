import socket
import threading
import logging
from collections import Counter

# Set up basic logging configuration
logging.basicConfig(filename='server_log.txt', level=logging.INFO, format='%(asctime)s - %(message)s')

# Constants for the server configuration
HOST = 'localhost'
PORT = 12345

# handle connection, data transmisson (issues during data send/recieve, such as broken pipes or timeouts), and invalid input (ex. NO NUMBERS, empty string), errors 
# display messages to enhance user experience 
# (for both serve/client?) -> see assignment details
def handle_client(client_socket, client_address):
    """ Handle incoming client requests. """
    logging.info(f"Connection from {client_address}")
    print(f"Connection from {client_address}")
    
    try:
        while True:
            # Receive data from the client
            request_data = client_socket.recv(1024).decode()
            if not request_data:  # Client has closed the connection
                break

            logging.info(f"Received request: {request_data}")
            print(f"Received request: {request_data}")
            
            # simple/complex|<message> -> process for simple and complex check for <mesage>
            
            # Here, the request is processed to determine the response
            response = process_request(request_data)
            client_socket.send(response.encode())
            logging.info(f"Sent response: {response}")
            print(f"Sent response: {response}")
            
    # should handle errors -> see assignment details
    finally:
        # Close the client connection
        client_socket.close()
        logging.info(f"Closed connection with {client_address}")
        print(f"Closed connection with {client_address}")

def process_request(request_data):
    """ Process the client's request and generate a response. """

    # simple/complex|<message>
    check_type, input_string = request_data.split('|')  # separate words that have '|' between them -> gives us the 'checktype' -> simple or complex, and the message it self
    input_string = ''.join(e for e in input_string if e.isalnum()).lower()  # removes all special characters, spaces, and makes it all letters lower case
    isPalindrome = is_palindrome(input_string) # check if the input is a palindrome
    
    if check_type == 'simple':
        return f"Is palindrome: {isPalindrome}"
    
    elif check_type == 'complex': 
        # Check if the string is already a palindrome
        if (isPalindrome):
            return f"True (The string is already a palindrome)"

        # If the string is not already a palindrome, compute complexity score
        canFormPalindrome, complexScore = palindrome_complex(input_string).split('|')   # return type will be: "True/False|Complexity Score"
        return f"Can form a palindrome: {canFormPalindrome}\nComplexity score: {complexScore} (number of swaps)"

def is_palindrome(input_string):
    """ Check if the given string is a palindrome. """
    return input_string == input_string[::-1]

def palindrome_complex(input_string):
    """ (COMPLEX) Check if the given string is a palindrome. """
    
    
    
    return "HI|42 :)" # temp

def start_server():
    """ Start the server and listen for incoming connections. """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen(5)
        logging.info(f"Server started and listening on {HOST}:{PORT}")
        
        while True:
            # Accept new client connections and start a thread for each client
            client_socket, client_address = server_socket.accept()
            threading.Thread(target=handle_client, args=(client_socket, client_address)).start() # include error checking for threads -> ex. terminate unexpectedly, or when server shuts down. 

if __name__ == '__main__':
    start_server()
