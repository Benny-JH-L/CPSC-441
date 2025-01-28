import socket

def main():
    host = '127.0.0.1'  # Server's hostname or IP address
    port = 12345        # Server's port

    # Create a socket and connect to the server
    # client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        try:
            client_socket.connect((host, port))
            print(f"Connected to server at {host}:{port}")
            
            # Send "Hello" message to the server
            client_socket.sendall("Hello".encode())
            
            # Receive and print the response from the server
            response = client_socket.recv(1024).decode()
            print(f"Server response: {response}")
        except ConnectionRefusedError:
            print(f"Connection to {host}:{port} failed. Ensure the server is running.")
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
