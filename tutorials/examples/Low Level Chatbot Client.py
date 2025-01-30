import socket

def main():
    host = '127.0.0.1'  # Server's hostname or IP address
    port = 12345        # Server's port

    try:
        # Step 1: Create a socket
        print("Creating socket...")
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            # Step 2: Connect to the server
            print(f"Connecting to server at {host}:{port}...")
            client_socket.connect((host, port))
            print(f"Connected to server at {host}:{port}")

            while True:
                # Step 3: Get input from the user
                user_input = input("You: ")
                if user_input.lower() == "exit":
                    print("Exiting...")
                    client_socket.sendall("exit".encode()) # not necessary to send
                    break

                # Step 4: Send the message to the server
                print(f"Sending: {user_input}")
                client_socket.sendall(user_input.encode())

                # Step 5: Receive the response from the server
                response = client_socket.recv(1024).decode()
                print(f"Server: {response}")
    except ConnectionRefusedError:
        print(f"Connection to {host}:{port} failed. Ensure the server is running.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
