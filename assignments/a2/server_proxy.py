import socket
import threading
import os
import random
import time
from pathlib import Path
from urllib.parse import urlparse
import base64

# Configuration
HOST = '127.0.0.1'  # Localhost
PORT = 8080         # Port to run the proxy on
DELAY = 1.0         # Delay in seconds per chunk of data
CHUNK_SIZE = 1024   # Size of data chunks to send

MEME_FOLDER_NAME = 'memes'
MEME_FOLDER_PATH = ""
EASTER_EGG_URL = b'http://google.ca/'
LIST_OF_MEME_NAMES = [] # List of meme file names inside the `MEME_FOLDER_NAME`
LIST_OF_MEME_PATHS = [] # Path to the meme (not sure if needed)
SHOULD_REPLACE = True

def find_memes_folder(start_path="."):
    for root, dirs, files in os.walk(start_path):
        if MEME_FOLDER_NAME in dirs:  # Found the "memes" folder
            return os.path.join(root, MEME_FOLDER_NAME)
    return None  # Return None if not found

# Gives the whole image path
def get_images_paths_from_folder(folder_path):
    image_extensions = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp"}
    return [
        os.path.join(folder_path, file)
        for file in os.listdir(folder_path)
        if os.path.splitext(file)[1].lower() in image_extensions
    ]

def get_image_names_from_folder(folder_path):
    image_extensions = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp"}
    return [
        file for file in os.listdir(folder_path)
        if os.path.splitext(file)[1].lower() in image_extensions
    ]

# checks if b`message` is a header with an Content-Type: image, 
# if it is then it injects the meme
def injectMeme(message):
    if not (b'HTTP' in message):
        return message
    
    header, body = message.split(b'\r\n\r\n', 1)
    headerValues = header.split(b'\r\n')
    
    print(f"\nHeader:\n{header.decode()}")    # debug
    print(f"\nBody:\n{body.decode()}")
    
    try:
        if b'Content-Type: image' in header: #and random.choice([True, False]):  # Replace 50% of images
            # should_replace = random.choice([True, False])
            # print(f"Should replace image: {should_replace}")  # Debug
            if SHOULD_REPLACE:
                SHOULD_REPLACE = False 
            # if random.random() < 0.5:
                randIndex = random.randint(0, len(LIST_OF_MEME_PATHS))
                # meme_path = random.choice(LIST_OF_MEME_PATHS)
                meme_path = LIST_OF_MEME_PATHS[randIndex]
                print(f"Replacing with meme: {meme_path}")  # Debug
                
                with open(meme_path, 'rb') as f:
                    meme_data = f.read()
            
                    injected_content_type = b'Content-Type: image/' + os.path.splitext(meme_path)[1][1:].encode()  # Get the extension
                    injected_content_length = b'Content-Length: ' + str(len(meme_data)).encode()
                    
                    # Replace the `Content-Type` and `Content-Length` headers
                    headerValues = [injected_content_type if b'Content-Type:' in line else line for line in headerValues]
                    headerValues = [injected_content_length if b'Content-Length:' in line else line for line in headerValues]
                    
                    header = b'\r\n'.join(headerValues)
                    
                    print(f'\nheader value[2] = \n{headerValues[2].decode()}')
                    print(f'header value[3] = \n{headerValues[3].decode()}')
                    
                    print(f"\n--Inject header values:\n{header.decode()}") # debug
                    print(f"\n--Inject Body:\n{meme_data.decode()}")
                    
                    return header + b'\r\n\r\n' + meme_data
            else:
                SHOULD_REPLACE = True   # Set replace next image
                
    except Exception as e:
        print("[ERROR IN INJECT MEME]", e)
        
    return header + b'\r\n\r\n' + body

def handle_client(client_socket):
    request = client_socket.recv(4096)
    try:
        first_line = request.split(b'\r\n')[0]
        url = first_line.split(b' ')[1]
        parsed_url = urlparse(url.decode('utf-8'))

        if url == EASTER_EGG_URL:
            send_easter_egg(client_socket)
            return

        host = parsed_url.hostname
        path = parsed_url.path + '?' + parsed_url.query if parsed_url.query else parsed_url.path
        if not path:
            path = '/'
        
        port = parsed_url.port if parsed_url.port else 80

        remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        remote_socket.connect((host, port))
        remote_socket.send(request)  # Forward the original request

        buffered = b''
        while True:
            response = remote_socket.recv(CHUNK_SIZE)
            if not response:
                break

            if b'HTTP/1.1 301' in response:
                headers = response.split(b'\r\n')
                for header in headers:
                    if b'Location: ' in header:
                        new_url = header.split(b'Location: ')[1].strip()
                        print(f"Redirecting to {new_url.decode('utf-8')}")
                        return handle_client(client_socket)  # Recursive call with new URL
                        
            # if (b'Content-Type' in response):
            #     print(f"\n---Content-Type: \n{response}")
            
            response = injectMeme(response)
            buffered += response
            # client_socket.send(response)  # Forward to client
            
        client_socket.send(buffered)  # Forward to client
        remote_socket.close()
    except Exception as e:
        print(f"Error: {e}")

    client_socket.close()

def send_easter_egg(client_socket):
    html = """
    HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n
    <html>
    <head><title>Surprise!</title></head>
    <body>
        <h1>You've discovered the Easter Egg!</h1>
        <img src='data:image/png;base64,{0}' width='100%' />
    </body>
    </html>
    """
    meme_path = random.choice(LIST_OF_MEME_PATHS)
    with open(meme_path, "rb") as meme_file:
        encoded_meme = base64.b64encode(meme_file.read()).decode('utf-8')
    client_socket.sendall(html.format(encoded_meme).encode())
    client_socket.close()


def start_proxy():
    print(f"Sloxy running on {HOST}:{PORT}, with a delay of {DELAY} seconds per {CHUNK_SIZE} bytes.")

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connection from {addr}")
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == "__main__":# Find the "memes" folder starting from the current directory
    MEME_FOLDER_PATH = find_memes_folder(".")
    LIST_OF_MEME_NAMES = get_image_names_from_folder(MEME_FOLDER_PATH)
    LIST_OF_MEME_PATHS = get_images_paths_from_folder(MEME_FOLDER_PATH)
    print("\nImage names:\n", LIST_OF_MEME_NAMES) # debug
    print("\nImage paths:\n",LIST_OF_MEME_PATHS) # debug
    start_proxy()

