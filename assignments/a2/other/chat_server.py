import socket
import threading
import os
import random
import time
from pathlib import Path
from urllib.parse import urlparse

# Configuration
HOST = '127.0.0.1'  # Localhost
PORT = 8080         # Port to run the proxy on
DELAY = 1.0         # Delay in seconds per chunk of data
CHUNK_SIZE = 1024   # Size of data chunks to send

MEME_FOLDER_NAME = 'memes'
MEME_FOLDER_PATH = ""
EASTER_EGG_URL = 'http://google.ca'
LIST_OF_MEME_NAMES = [] # List of meme file names inside the `MEME_FOLDER_NAME`
LIST_OF_MEME_PATHS = [] # Path to the meme (not sure if needed)

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

# Injects a meme into image responses roughly 50% of the time
def injectMeme(response):
    if not (b'HTTP' in response and b'Content-Type: image' in response):
        return response
    
    if random.choice([True, False]):  # Replace ~50% of images
        meme_path = random.choice(LIST_OF_MEME_PATHS)
        with open(meme_path, 'rb') as f:
            meme_data = f.read()
    
        header, body = response.split(b'\r\n\r\n', 1)
        headers = header.split(b'\r\n')
        new_headers = []
        
        for h in headers:
            if h.startswith(b'Content-Type:'):
                ext = os.path.splitext(meme_path)[1][1:]
                new_headers.append(f'Content-Type: image/{ext}'.encode())
            elif h.startswith(b'Content-Length:'):
                new_headers.append(f'Content-Length: {len(meme_data)}'.encode())
            else:
                new_headers.append(h)
        
        new_header = b'\r\n'.join(new_headers)
        return new_header + b'\r\n\r\n' + meme_data
    
    return response

def handle_client(client_socket):
    request = client_socket.recv(4096)
    try:
        first_line = request.split(b'\r\n')[0]
        url = first_line.split(b' ')[1]
        parsed_url = urlparse(url.decode('utf-8'))

        host = parsed_url.hostname
        path = parsed_url.path + '?' + parsed_url.query if parsed_url.query else parsed_url.path
        if not path:
            path = '/'
        
        port = parsed_url.port if parsed_url.port else 80

        remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        remote_socket.connect((host, port))
        remote_socket.send(request)  # Forward the original request

        while True:
            response = remote_socket.recv(CHUNK_SIZE)
            if not response:
                break
            
            response = injectMeme(response)
            client_socket.send(response)  # Forward to client
            time.sleep(DELAY)  # Slow down response

        remote_socket.close()
    except Exception as e:
        print(f"Error: {e}")

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

if __name__ == "__main__":
    MEME_FOLDER_PATH = find_memes_folder(".")
    LIST_OF_MEME_NAMES = get_image_names_from_folder(MEME_FOLDER_PATH)
    LIST_OF_MEME_PATHS = get_images_paths_from_folder(MEME_FOLDER_PATH)
    print("\nImage names:\n", LIST_OF_MEME_NAMES)  # debug
    print("\nImage paths:\n", LIST_OF_MEME_PATHS)  # debug
    start_proxy()
