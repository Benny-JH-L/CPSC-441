import socket
import threading
import random
import os
import base64

# Configuration
HOST = '127.0.0.1'  # Localhost
PORT = 8080  # Proxy server port
MEME_FOLDER_NAME = "memes"
MEME_FOLDER_PATH = ""  # Folder containing meme images
EASTER_EGG_URL = "http://google.ca"
MEMES = []

def find_memes_folder(start_path="."):
    for root, dirs, files in os.walk(start_path):
        if MEME_FOLDER_NAME in dirs:  # Found the "memes" folder
            return os.path.join(root, MEME_FOLDER_NAME)
    return None  # Return None if not found

def handle_client(client_socket):
    request = client_socket.recv(4096)
    if not request:
        client_socket.close()
        return

    # Extract requested URL
    first_line = request.decode().split('\r\n')[0]
    url = first_line.split(' ')[1]

    if url == EASTER_EGG_URL:
        send_easter_egg(client_socket)
        return
    
    # Connect to target server
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host, path = extract_host_path(url)
    try:
        server_socket.connect((host, 80))
        server_socket.sendall(request)
        response = server_socket.recv(4096)
    except:
        client_socket.close()
        return

    # Modify response if it's an image
    if is_image_response(response):
        if random.random() < 0.5 and MEMES:  # 50% chance to replace
            response = replace_with_meme()
    
    client_socket.sendall(response)
    client_socket.close()
    server_socket.close()

def extract_host_path(url):
    if url.startswith("http://"):
        url = url[7:]
    parts = url.split("/")
    return parts[0], "/" + "/".join(parts[1:])

def is_image_response(response):
    return b"Content-Type: image" in response

def replace_with_meme():
    meme_path = random.choice(MEMES)
    with open(meme_path, "rb") as meme_file:
        meme_data = meme_file.read()
    encoded_meme = base64.b64encode(meme_data).decode('utf-8')
    return f"HTTP/1.1 200 OK\r\nContent-Type: image/jpeg\r\n\r\n{encoded_meme}".encode()

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
    meme_path = random.choice(MEMES)
    with open(meme_path, "rb") as meme_file:
        encoded_meme = base64.b64encode(meme_file.read()).decode('utf-8')
    client_socket.sendall(html.format(encoded_meme).encode())
    client_socket.close()

def start_proxy():
    proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    proxy_socket.bind((HOST, PORT))
    proxy_socket.listen(5)
    print(f"[*] Proxy server listening on {HOST}:{PORT}")
    
    while True:
        client_socket, _ = proxy_socket.accept()
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == "__main__":
    MEME_FOLDER_PATH = find_memes_folder(".")
    # Load memes
    MEMES = [os.path.join(MEME_FOLDER_PATH, f) for f in os.listdir(MEME_FOLDER_PATH) if f.endswith(('jpg', 'png', 'gif'))]

    start_proxy()
