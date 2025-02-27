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
EASTER_EGG_URL = 'http://google.ca'
LIST_OF_MEME_NAMES = [] # List of meme file names inside the `MEME_FOLDER_NAME`
LIST_OF_MEME_PATHS = [] # Path to the meme

# Load memes from the folder
# # MEMES = [os.path.join(MEME_FOLDER, f) for f in os.listdir(MEME_FOLDER) if f.endswith(('.jpg', '.png', '.gif'))]
# MEMES = [os.path.join(MEME_FOLDER, item) for item in os.listdir()]
# # MEMES = [item.resolve() for item in MEME_FOLDER.iterdir()]

def find_memes_folder(start_path="."):
    for root, dirs, files in os.walk(start_path):
        if MEME_FOLDER_NAME in dirs:  # Found the "memes" folder
            return os.path.join(root, MEME_FOLDER_NAME)
    return None  # Return None if not found

# Gives the whole image path
# def get_images_from_folder(folder_path):
#     image_extensions = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp"}
#     return [
#         os.path.join(folder_path, file)
#         for file in os.listdir(folder_path)
#         if os.path.splitext(file)[1].lower() in image_extensions
#     ]

# Find the "memes" folder starting from the current directory
# memes_folder = find_memes_folder(".")
# print(get_images_from_folder(memes_folder))

def get_image_names(folder_path):
    image_extensions = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp"}
    return [
        file for file in os.listdir(folder_path)
        if os.path.splitext(file)[1].lower() in image_extensions
    ]

# Find the "memes" folder starting from the current directory
memes_folder = find_memes_folder(".")
print(get_image_names(memes_folder))



# def find_memes_folder(start_path=Path(".")):
#     for folder in start_path.rglob("memes"):
#         if folder.is_dir():
#             return folder
#     return None

# def get_images_from_folder(folder_path):
#     image_extensions = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp"}
#     return [file.resolve() for file in folder_path.iterdir() if file.suffix.lower() in image_extensions]

# # Find the "memes" folder
# memes_folder = find_memes_folder()

# if memes_folder:
#     images = get_images_from_folder(memes_folder)
#     print("Images found:", images)
# else:
#     print("Memes folder not found.")


# checks if b`message` is a header with an Content-Type: image, 
# if it is then it injects the meme
def injectMeme(message):
    if not (b'HTTP' in message):
        return message
    
    headerValues, body = message.split(b'\r\n\r\n', 1)

    # headerValues = message.split(b'\r\n')
    
    print(f"\nHeader values:\n{headerValues}")    # debug
    
    if random.choice([True, False]):  # Replace 50% of images
        meme = random.choice(MEMES)
        with open(meme, 'rb') as f:
            meme_data = f.read()
    
            injected_content_type = b'Content-Type: image/' + b'png'
            injected_content_length = b'' + str(len(meme_data))
            headerValues.replace(headerValues[1], injected_content_type)        # replace the `Content-Type`
            headerValues.replace(headerValues[3], injected_content_length)      # replace the `Content-Length`
            
            print(f'\nheader value[1] = \n{headerValues[1].decode()}')
            print(f'header value[3] = \n{headerValues[3].decode()}')
            
        print(f"\n--Inject header values:\n{headerValues}") # debug
    
    return headerValues + b'\r\n\r\n' + body
    

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
            client_socket.send(response)  # Forward to client
            
            # time.sleep(DELAY)  # Slow down response

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
    start_proxy()

