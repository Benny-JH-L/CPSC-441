
# Assignment 3: Create a Panda-Chat
#     CPSC 441 Winter 2025 | Benny Liang | 30192142

import socket
import threading
import sys
import random

# Server configuration
SERVER_HOST = 'localhost'
SERVER_PORT = 12345

RECV_SIZE = 1024

REQUEST_CHECK_UNIQUE_USERNAME = "CHECK_UNIQUE_USER"
REQUEST_SEND_MESSAGE = "SEND_MESSAGE"
REQUEST_GROVE = "@grove"
REQUEST_BAMBOO = "@bamboo"
REQUEST_EXIT = "EXIT"

LIST_PANDA_THEMED_DECORATIONS = [
    "\U0001F43C", # 🐼
    "\U0001F38D", # 🎍
    "\U0001F43E", # 🐾
    "\U0001F96C"  # 🥬
    ]

LIST_OF_PANDA_FACTS = [
    "Did you know, the scientific name for giant panda's are 'Ailuropoda melanoleuca' which translates to 'black and white cat-foot'",
    "Did you know, giant panda's poop around 100 times a day.",
    "Did you know, giant panda's are considered `living fossils` because they haven't evolved much in their millions of years of life on Earth.",
    "Did you know, panda's have a `pseudo thumb` that helps them grip bamboo.",
    "Did you know, a panda's jaws are so strong they similar to that of a lion.",
    "Did you know, giant panda mothers will breathe heavily on their cubs to keep them warm and humid.",
    "Pandas spend around 14 hours a day eating bamboo! ",
    "Baby pandas are born pink and weigh only about 100 grams! ",
    "A group of pandas is called an embarrassment! ",
    "Pandas can swim and are excellent tree climbers! ",
    "There are only about 1,800 giant pandas left in the wild. "
]
# Citations:
# https://www.ifaw.org/ca-en/journal/15-fascinating-facts-giant-pandas 
# https://nationalzoo.si.edu/animals/news/50-panda-facts-celebrate-50-years-giant-pandas-smithsonians-national-zoo


ASCII_PANDA_ART = '''
                               -|-_
                                | _
                               <|/
                                | |,
                               |-|-o
                               |<|.
                _,..._,m,      |,
             ,/'      '"";     | |,
            /             ".
          ,'mmmMMMMmm.      \  -|-_"
        _/-"^^^^^"""%#%mm,   ;  | _ o
  ,m,_,'              "###)  ;,
 (###%                 \#/  ;##mm.
  ^#/  __        ___    ;  (######)
   ;  //.\\     //.\\   ;   \####/
  _; (#\"//     \\"/#)  ;  ,/
 @##\ \##/   =   `"=" ,;mm/
 `\##>.____,...,____,<####@
                       ""'     m1a   
'''
# Art obtained from: https://ascii.co.uk/art/panda

def display_messages(client_socket, username):
    """
    Receives and displays messages while keeping the user prompt at the bottom of the terminal.
    """
    
    print("[DEBUG] Entered display chat room messages") # debug
    
    while True:
        try:
            response = client_socket.recv(RECV_SIZE).decode()
            if not response:
                break
                        
            # keep "<username> > " at the bottom of the screen
            sys.stdout.write("\r" + " " * 100 + "\r")  # clear current input line
            sys.stdout.write(response + "\n")  
            sys.stdout.write(f"\r{username} > ")    # print "username > "
            sys.stdout.flush()
        except: # if the client leaves, break.
            # print("[Exception in display messages] exiting...")     # debug
            print("Exiting...")     # debug
            break

def is_unique_username(client_socket, username_to_check):
    """
    [Client] Checks if the user name is unique, ie. if there is no client already with this username.
    Sends the `username_to_check` to the server, and the server checks if it is unique.
    """
    
    print("Entered username checker...")
    
    message = f"{REQUEST_CHECK_UNIQUE_USERNAME}|{username_to_check}|{""}"
    
    client_socket.send(message.encode())
    response = client_socket.recv(RECV_SIZE).decode()
    
    if (response.lower() == "true"):
        print(f"{username_to_check} is a unique username")  # debug
        return True
    
    print(f"{username_to_check} is NOT a unique username")  # debug
    return False

def start_client():
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        
        try:
            # establish a connection to the server
            client_socket.connect((SERVER_HOST, SERVER_PORT))
                        
            # ask the user for a unique username 
            print ("Welcome to Panda Chat!")
            print(ASCII_PANDA_ART)
            username = ""
            while(username == ""): 
                username_to_check = input("Please choose a username: ")
                
                # check if the entered username is unique
                if (is_unique_username(client_socket, username_to_check)):
                    username = username_to_check                    # set the user name
                    print(f" Username set to: {username}")  # debug
                    break
            
            # thread to update the chat room messages for this client
            try:
                thread = threading.Thread(target=display_messages, args=(client_socket, username,))
                thread.start()
            except:
                print("[CLIENT] Thread exception...")
                return
            
            # asking the user for mesages
            while(True):
                # ask the user for an input, ie message
                sys.stdout.write(f"{username} > ")
                sys.stdout.flush()
                message = input()
                
                # sent message will be in the form of (excluding the spaces): "<request type> | <user name> | <message>"
                if (message == "@leaves"):  # leave chat room
                    leave_message = f"{REQUEST_EXIT}|{username}|{""}"
                    client_socket.send(leave_message.encode())      # tell the server this user wants to leave the chat room
                    print("Leaving the chat room...")
                    break
                
                elif (message == "@bamboo"):  # random panda-related fact
                    randIndex = random.randint(0, len(LIST_OF_PANDA_FACTS) - 1)
                    randFact = LIST_OF_PANDA_FACTS[randIndex]
                    print(f"@bamboo > {randFact}")
                    
                elif (message == "@grove"):   # lists all current connected users
                    request = f"{REQUEST_GROVE}|{username}|{""}"
                    client_socket.send(request.encode())
                    
                # send message to the chat room
                else:
                    # get randome panda-themed decor
                    randIndex = random.randint(0, len(LIST_PANDA_THEMED_DECORATIONS) - 1)
                    randEmoji = LIST_PANDA_THEMED_DECORATIONS[randIndex]
                    message = message + " " + randEmoji                     # add the decor
                    message = f"{REQUEST_SEND_MESSAGE}|{username}|{message}"
                    client_socket.send(message.encode())
            
        except:
            print("EXCEPTION HAPPENED IN CLIENT")     
        
        client_socket.close()
        
if __name__ == "__main__":
    # debug
    # print(ASCII_PANDA_ART)
    # print("\U0001F43C") # panda
    # print("\U0001F38D") # bamboo
    # print("\U0001F43E") # paws 🐾
    # print("\U0001F96C") # leaves 🥬
    start_client()
