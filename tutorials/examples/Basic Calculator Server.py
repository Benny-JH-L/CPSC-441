import socket

def calculate(expression):
    """
    Perform the calculation based on the client's input.
    Supported format: "<number1> <operator> <number2>"
    Operators: +, -, *, /
    """
    try:
        # Split the input expression
        num1, operator, num2 = expression.split()
        num1, num2 = float(num1), float(num2)       # convert the string representaion of the number into an actual number
        
        # Perform the operation
        if operator == '+':
            return f"Result: {num1 + num2}"
        elif operator == '-':
            return f"Result: {num1 - num2}"
        elif operator == '*':
            return f"Result: {num1 * num2}"
        elif operator == '/':
            if num2 == 0:
                return "Error: Division by zero is not allowed."
            return f"Result: {num1 / num2}"
        else:
            return "Error: Unsupported operator. Use +, -, *, or /."
    except ValueError:
        return "Error: Invalid input format. Use '<number1> <operator> <number2>'."
    except Exception as e:
        return f"Error: {str(e)}"

def main():
    host = '127.0.0.1'
    port = 12345

    # Create a socket and bind it to the address
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen(1)  # Listen for incoming connections
        print(f"Calculator server is running on {host}:{port}...")
        
        while True:
            conn, addr = server_socket.accept()
            with conn:
                print(f"Connected by {addr}")
                while True:
                    data = conn.recv(1024).decode() # mathematical expression form user
                    if not data:
                        break
                    print(f"Received: {data}")
                    result = calculate(data)
                    conn.sendall(result.encode())

if __name__ == "__main__":
    main()