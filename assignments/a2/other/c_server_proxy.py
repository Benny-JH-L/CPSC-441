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
LIST_OF_MEME_NAMES = []  # List of meme file names inside the `MEME_FOLDER_NAME`
LIST_OF_MEME_PATHS = []  # Path to the meme files


def find_memes_folder(start_path="."):
    for root, dirs, files in os.walk(start_path):
        if MEME_FOLDER_NAME in dirs:  # Found the "memes" folder
            return os.path.join(root, MEME_FOLDER_NAME)
    return None  # Return None if not found


# Gives the whole image path
def get_images_paths_from_folder(folder_path):
    if not folder_path:
        return []
    image_extensions = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp"}
    return [
        os.path.join(folder_path, file)
        for file in os.listdir(folder_path)
        if os.path.splitext(file)[1].lower() in image_extensions
    ]


def get_image_names_from_folder(folder_path):
    if not folder_path:
        return []
    image_extensions = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp"}
    return [
        file for file in os.listdir(folder_path)
        if os.path.splitext(file)[1].lower() in image_extensions
    ]


def get_content_type_from_extension(filename):
    """Get MIME type based on file extension"""
    ext = os.path.splitext(filename)[1].lower()
    content_types = {
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg',
        '.png': 'image/png',
        '.gif': 'image/gif',
        '.bmp': 'image/bmp',
        '.webp': 'image/webp'
    }
    return content_types.get(ext, 'image/jpeg')  # Default to jpeg if unknown


def injectMeme(message, replace_chance=0.5):
    """Replace image with meme with a 50% chance"""
    if not message.startswith(b'HTTP'):
        return message
    
    try:
        # Split into header and body
        parts = message.split(b'\r\n\r\n', 1)
        if len(parts) < 2:
            return message  # No body found, return original
        
        header, body = parts
        
        # Check if this is an image response
        content_type_line = None
        header_lines = header.split(b'\r\n')
        
        for i, line in enumerate(header_lines):
            if line.lower().startswith(b'content-type:') and b'image/' in line.lower():
                content_type_line = i
                # Found an image, decide whether to replace it
                if random.random() < replace_chance and LIST_OF_MEME_PATHS:
                    # Choose a random meme
                    meme_path = random.choice(LIST_OF_MEME_PATHS)
                    meme_name = os.path.basename(meme_path)
                    meme_content_type = get_content_type_from_extension(meme_name)
                    
                    # Read the meme file
                    with open(meme_path, 'rb') as f:
                        meme_data = f.read()
                    
                    # Replace the content type in the header
                    header_lines[content_type_line] = f'Content-Type: {meme_content_type}'.encode()
                    
                    # Update content length
                    for j, line in enumerate(header_lines):
                        if line.lower().startswith(b'content-length:'):
                            header_lines[j] = f'Content-Length: {len(meme_data)}'.encode()
                            break
                    
                    # Log the replacement
                    print(f"Replacing image with meme: {meme_name}")
                    
                    # Reconstruct the message with the meme
                    new_header = b'\r\n'.join(header_lines)
                    return new_header + b'\r\n\r\n' + meme_data
        
        # If we get here, either it wasn't an image or we decided not to replace it
        return message
    
    except Exception as e:
        print(f"Error in injectMeme: {e}")
        return message  # Return original message if any error occurs


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

        print(f"Connecting to {host}:{port}{path}")
        
        remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        remote_socket.connect((host, port))
        remote_socket.send(request)  # Forward the original request

        # Buffer to collect full HTTP responses
        response_buffer = b''
        
        while True:
            response_chunk = remote_socket.recv(CHUNK_SIZE)
            if not response_chunk:
                break
            
            response_buffer += response_chunk
            
            # Check if we have a complete HTTP message
            if b'\r\n\r\n' in response_buffer:
                # If there's a redirect, handle it
                if b'HTTP/1.1 301' in response_buffer or b'HTTP/1.1 302' in response_buffer:
                    headers = response_buffer.split(b'\r\n')
                    for header in headers:
                        if b'Location: ' in header:
                            client_socket.send(response_buffer)  # Forward the redirect
                            response_buffer = b''
                            break
                
                # Process the response if it contains content type header
                if b'Content-Type:' in response_buffer or b'content-type:' in response_buffer:
                    # Process and potentially inject meme
                    modified_response = injectMeme(response_buffer)
                    client_socket.send(modified_response)
                    response_buffer = b''
            
            # If buffer is getting large, just send it without processing
            if len(response_buffer) > CHUNK_SIZE * 10:
                client_socket.send(response_buffer)
                response_buffer = b''
                
            # time.sleep(DELAY)  # Apply the configured delay
        
        # Send any remaining data
        if response_buffer:
            client_socket.send(response_buffer)
            
        remote_socket.close()
        
    except Exception as e:
        print(f"Error handling client: {e}")
    finally:
        client_socket.close()


def start_proxy():
    print(f"Proxy running on {HOST}:{PORT}, with a delay of {DELAY} seconds per chunk")
    print(f"Will replace 50% of images with memes from folder: {MEME_FOLDER_PATH}")
    print(f"Available memes: {LIST_OF_MEME_NAMES}")

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)

    print("Waiting for connections...")
    
    try:
        while True:
            client_socket, addr = server_socket.accept()
            print(f"Connection from {addr}")
            client_handler = threading.Thread(target=handle_client, args=(client_socket,))
            client_handler.daemon = True  # Make thread exit when main thread exits
            client_handler.start()
    except KeyboardInterrupt:
        print("Shutting down proxy server...")
    finally:
        server_socket.close()


if __name__ == "__main__":
    # Find the "memes" folder starting from the current directory
    MEME_FOLDER_PATH = find_memes_folder(".")
    if not MEME_FOLDER_PATH:
        print(f"Warning: '{MEME_FOLDER_NAME}' folder not found. No images will be replaced.")
    
    LIST_OF_MEME_NAMES = get_image_names_from_folder(MEME_FOLDER_PATH)
    LIST_OF_MEME_PATHS = get_images_paths_from_folder(MEME_FOLDER_PATH)
    
    if LIST_OF_MEME_PATHS:
        print(f"Found {len(LIST_OF_MEME_PATHS)} memes in {MEME_FOLDER_PATH}")
    else:
        print("No meme images found. No images will be replaced.")
    
    start_proxy()
    