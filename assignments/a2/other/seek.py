import socket
import threading
import os
import random
import base64
from urllib.parse import urlparse

# Configuration
PROXY_HOST = '127.0.0.1'
PROXY_PORT = 8080
MEME_FOLDER = 'memes'
EASTER_EGG_URL = 'http://google.ca'

# Load memes from the folder
MEMES = [os.path.join(MEME_FOLDER, f) for f in os.listdir(MEME_FOLDER) if f.endswith(('.jpg', '.png', '.gif'))]

def handle_client(client_socket):
    
    response = b''
    try:    
        # Receive the request from the client
        request = client_socket.recv(4096)
        if not request:
            client_socket.close()
            return

        # Parse the request to get the target host and path
        try:
            request_lines = request.split(b'\r\n')
            first_line = request_lines[0].decode('utf-8')
            url = first_line.split(' ')[1]
            parsed_url = urlparse(url)
            target_host = parsed_url.netloc
            target_path = parsed_url.path if parsed_url.path else '/'
        except UnicodeDecodeError:
            # If the request is not valid UTF-8, close the connection
            client_socket.close()
            return

        # Check for Easter egg URL
        if url == EASTER_EGG_URL:
            with open('easter_egg.html', 'r') as f:
                response = f.read()
            client_socket.send(response.encode('utf-8'))
            client_socket.close()
            return

        # Forward the request to the target server
        target_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        target_socket.connect((target_host, 80))
        target_socket.send(f"GET {target_path} HTTP/1.1\r\nHost: {target_host}\r\n\r\n".encode('utf-8'))

        # Receive the response from the target server
        while True:
            data = target_socket.recv(1024)
            if not data:
                break
            response += data
            print("Adding")

        # Check if the response contains an image
        headers, body = response.split(b'\r\n\r\n', 1)
        if b'Content-Type: image' in headers:
            if random.choice([True, False]):  # Replace 50% of images
                meme = random.choice(MEMES)
                with open(meme, 'rb') as f:
                    meme_data = f.read()
                meme_base64 = base64.b64encode(meme_data).decode('utf-8')
                headers = headers.replace(b'Content-Length: ', b'Content-Length: ' + str(len(meme_data)).encode('utf-8'))
                response = headers + b'\r\n\r\n' + meme_data
        else:
            # Replace image URLs in HTML content
            if b'Content-Type: text/html' in headers:
                html_content = body.decode('utf-8', errors='ignore')
                # Replace image URLs with memes
                # This is a simple example, you might need a more sophisticated HTML parser
                html_content = html_content.replace('<img', '<img style="border: 5px solid red;"')
                response = headers + b'\r\n\r\n' + html_content.encode('utf-8')
    except Exception as e:
        print(f"Error: {e}")
    # Send the modified response back to the client
    client_socket.send(response)
    client_socket.close()
    target_socket.close()

def start_proxy():
    proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    proxy_socket.bind((PROXY_HOST, PROXY_PORT))
    proxy_socket.listen(5)
    print(f"Proxy server started on {PROXY_HOST}:{PROXY_PORT}")

    while True:
        client_socket, addr = proxy_socket.accept()
        print(f"Accepted connection from {addr}")
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == '__main__':
    if not os.path.exists(MEME_FOLDER):
        os.makedirs(MEME_FOLDER)
        print(f"Created meme folder at {MEME_FOLDER}. Please add some memes!")
    else:
        start_proxy()
