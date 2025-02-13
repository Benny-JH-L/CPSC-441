
# Assignment 1: Advanced Palindrome Check Server-Client Application
#     CPSC 441 Winter 2025 | Benny Liang | 30192142

import socket
import threading
import logging
from collections import Counter

# config for caeser cipher
SHIFT = -7  # negate the `shift` value from client

# Set up basic logging configuration
logging.basicConfig(filename='server_log.txt', level=logging.INFO, format='%(asctime)s - %(message)s')

# Constants for the server configuration
HOST = 'localhost'
PORT = 12345

def handle_client(client_socket, client_address):
    """ Handle incoming client requests. """
    logging.info(f"Connection from {client_address}")
    print(f"Connection from {client_address}")
    
    client_socket.settimeout(5)  # Set timeout for receiving data (5 seconds)
    numTimeouts = 0  # Initialize timeout counter

    try:
        while numTimeouts < 3:  # Allow up to 3 timeouts before closing connection
            try:
                # Receive data from the client
                request_data = client_socket.recv(1024).decode()
                # log data recieved from specific client
                logging.info(f"Data recieved: <{request_data}> from {client_address}")
                print(f"Data recieved: <{request_data}> from {client_address}")
                
                if not request_data:  # Client has closed the connection
                    logging.info(f"Client {client_address} disconnected...")
                    print(f"Client {client_address} disconnected...")
                    break

                numTimeouts = 0 # reset count 
                
                response = process_request(request_data)
                response = caesar_cipher(response)          # encrypt `response` before sending it to the client
                client_socket.send(response.encode())
                
                logging.info(f"Sent response (encrypted): <{response}> to {client_address}")
                print(f"Sent response (encrypted): <{response}> to {client_address}")

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
    

def process_request(request_data):
    """ Process the client's request and generate a response. """
    
    # testing time out on client side
    # while True:
    #     n = 0
    
    # `request_data`` in the form of: simple/complex|<message>
    check_type, input_string = request_data.split('|')  # separate words that have '|' between them -> gives us the 'checktype' -> simple or complex, and the message it self
    input_string = caesar_cipher(input_string)          # decrypt the `input_string`
    input_string = ''.join(e for e in input_string if e.isalnum()).lower()  # removes all special characters, spaces, and makes it all letters lower case
    isPalindrome = is_palindrome(input_string)          # check if the input is a palindrome
    
    if check_type == 'simple':
        return f"Is palindrome: {isPalindrome}"
    
    elif check_type == 'complex': 
        # Check if the string is already a palindrome
        if (isPalindrome):
            return f"True (The string is already a palindrome)"

        # If the string is not already a palindrome, compute complexity score
        canFormPalindrome, complexScore = palindrome_complex(input_string).split('|')   # return type will be: "True/False|Complexity Score"
        if (canFormPalindrome == "True"):   # return a message with the `input_str` being able to turn into a palindrome, and its complexity score
            return f"Can form a palindrome: {canFormPalindrome}\nComplexity score: {complexScore} (number of swaps)"
        else:
            return f"Impossible to form a palindrome with `{input_string}`"

def is_palindrome(input_string):
    """ Check if the given string is a palindrome. """
    return input_string == input_string[::-1]

# finds the minimum number of swaps needed to convert `input_str` to a palindrome.
# returns the number of swaps needed and if the `input_str` can be turned in to a palindrome,
# in the form of a string: "<True/False>|<number of swaps>"
def palindrome_complex(input_str):
    countOfCharactersMap = {}
    numSwaps = 0
    
    # count the characters (letters) in the input
    for char in input_str:
        if char in countOfCharactersMap:
            countOfCharactersMap[char] += 1
        else:
            countOfCharactersMap[char] = 1 
    
    foundOdd = False
    palindromePossible = True
    oddInstancedChar = ' '      # save the character with an odd number of occurances
    
    # Go through letters and see if we have multiple letters with odd numbered occurances (a character has an odd number of instances).
    # (check if its possible to turn the input into a palindrome)
    for chara, instances in countOfCharactersMap.items():
        
        if (instances % 2 == 1 and not foundOdd):
            foundOdd = True
            oddInstancedChar = chara
        # if found a `chara` that has odd occurances and there is already 
        # another `chara` found with odd numbered occurances, then this `input` cannot be made into a palindrome.
        elif (instances % 2 == 1 and foundOdd):
            palindromePossible = False
            break
    
    if (not palindromePossible):
        return "False|-1"       # return, can't turn `input` into a palindrome
            
    # find the index of all odd instanced character that are not in an optimal position
    indiciesOfOddNumberedChars = []
    left = 0                        # "points" to the left of the string and will move inwards (moves right)
    right = len(input_str) - 1      # "points" to the right of the string and will move inwards (moves left)
    while(left < right):
        
        if (input_str[left] != input_str[right]):
            if (input_str[left] == oddInstancedChar):
                indiciesOfOddNumberedChars.append(left)
            elif (input_str[right] == oddInstancedChar):
                indiciesOfOddNumberedChars.append(right)
            elif (left + 1 == right - 1 and input_str[left+1] == oddInstancedChar):    # case where the middle contains a odd instanced character
                indiciesOfOddNumberedChars.append(left+1)
        
        left += 1
        right -= 1
        
    # If the input has a character with an odd number of instances
    if (foundOdd):
        middleIndex = int(len(input_str) / 2)
        middleCharToSwap = input_str[middleIndex]
        foundOptimal = False
        # Find the optimal index to swap one of the odd letters
        # such that the, odd instanced character is in the middle of the string.
        # And the swapped middle character is in a optimal position
        left = 0                        # "points" to the left of the string and will move inwards (moves right)
        right = len(input_str) - 1      # "points" to the right of the string and will move inwards (moves left)
        while (right > left and not foundOptimal):
            
            if ((input_str[left] == middleCharToSwap or input_str[right] == middleCharToSwap) and input_str[left] != input_str[right]):
                for indexOfOdd in indiciesOfOddNumberedChars:
                    # Do Swap
                    input_str = swapAtIndex(input_str, indexOfOdd, middleIndex)
                    
                    if (input_str[left] != input_str[right]):    # did swap, and it was not the most optimal, undo swap and check next
                        input_str = swapAtIndex(input_str, indexOfOdd, middleIndex)
                        
                    elif (input_str[left] == input_str[right]):  # was an optimal swap, break
                        numSwaps += 1
                        foundOptimal = True
                        break
            left += 1
            right -= 1
        
        # Case where we could not find the most optimal swap, swap arbitrarily the middle letter 
        # with an odd number of instances character that is not in an optimal position.
        # (Don't swap if middleIndex is already one of the odd instanced letters)
        if (not foundOptimal and input_str[middleIndex] != oddInstancedChar):
            input_str = swapAtIndex(input_str, indiciesOfOddNumberedChars[0], middleIndex)
            numSwaps += 1

    # Compute possible palindrome
    # `left` is the index of the left pointer for the input
    # `right` is the index of the right pointer for the input 
    left = 0
    right = len(input_str) - 1
    while (right > left):
        if (input_str[left] == input_str[right]):   # letter's at input[left] is the same at input[right]
            left += 1
            right -= 1
            continue                                # keep checking
        
        # letters at index `left` and `right` are not equal,
        # find a letter at index `tmp` that is equal to the letter at index `left`, starting from index `right-1`
        tmp = right - 1
        while (tmp > left):
            if (input_str[tmp] == input_str[left]):  # swap letters at input[tmp] and input[right], so input[left] == input[right]
                input_str = swapAtIndex(input_str, right, tmp)  # swap the characters at indicies `right` and `tmp`, then update `input`
                numSwaps += 1                                   # increment numSwaps by 1
                break                                           # exit loop
            tmp -= 1
        
        left += 1
        right -= 1
    
    return f"True|{numSwaps}"

# Helper function to swap 2 characters in a string with given indicies 
def swapAtIndex(input_str, index1, index2):
    input_str_list = list(input_str)        # turn string into a list
    input_str_list[index1], input_str_list[index2] = input_str_list[index2], input_str_list[index1]     # swap elements at indices
    return ''.join(input_str_list)          # return a string with swapped characters

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

if __name__ == '__main__':
    start_server()
