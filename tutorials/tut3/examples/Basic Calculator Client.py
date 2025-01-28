import socket

def main():
    host = '127.0.0.1'
    port = 12345

    # with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    # or
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    with client_socket:
        try:
            client_socket.connect((host, port))
            print(f"Connected to calculator server at {host}:{port}")
            
            while True:
                user_input = input("Enter calculation (<number1> <operator> <number2>) or 'exit' to quit: ")
                if user_input.lower() == 'exit':
                    print("Exiting...")
                    break
                
                # Send the input to the server
                client_socket.sendall(user_input.encode())
                
                # Receive and display the result
                response = client_socket.recv(1024).decode()
                print(response)
        except ConnectionRefusedError:
            print(f"Connection to {host}:{port} failed. Ensure the server is running.")
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()