import socket

def main():
    host = '127.0.0.1'  # Localhost
    port = 12345        # Port to listen on

    # Create a socket and bind it to the host and port
    # server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen(1)  # Listen for 1 connection at a time
        # if you are listening for more than 1 connection (client) should use threading
        print(f"Server is running on {host}:{port}...")

        while True:
            conn, addr = server_socket.accept()  # Accept incoming connections
            with conn:  # used as exception handling, but nothing is being catched, so it can be removed
                print(f"Connected by {addr}")
                data = conn.recv(1024).decode()  # Receive data from the client
                if not data:
                    break
                print(f"Received: {data}")
                conn.sendall("Hello, Client!".encode())  # Send a response
                # conn.send("Hello, Client!".encode())  # Send a response

if __name__ == "__main__":
    main()