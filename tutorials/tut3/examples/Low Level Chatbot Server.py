import socket

def chatbot_response(message):
    """Generate a chatbot-like response based on the received message."""
    message = message.lower().strip() # strips white spaces before and after the string

    # Predefined responses
    responses = {
        "hello": "Hi there! How can I assist you today?",
        "hi": "Hi there! How can I assist you today?",
        "how are you?": "I'm just a server, but I'm doing great! How about you?",
        "what's your name?": "I'm ChatServer, your friendly chatbot server!",
        "bye": "Goodbye! Have a great day!",
        "what can you do?": "I can chat with you, answer simple questions, and make your day better!",
        "tell me a joke": "Why don't programmers like nature? It has too many bugs!",
        "what is the meaning of life?": "42. That's according to Douglas Adams, at least!",
        "how old are you?": "I was created just a moment ago, but I feel timeless!",
        "where are you?": "I'm right here, running on your local server.",
        "what's the time?": "I'm not wearing a watch, but your system clock might help!",
        "tell me a fun fact": "Did you know? Honey never spoils. Archaeologists have found pots of honey in ancient tombs that are over 3,000 years old!",
        "do you like music?": "I can't listen to music, but I hear binary beats are amazing!",
        "can you help me?": "Of course! Tell me what you need help with.",
        "who created you?": "I was created by a programmer who loves helping others!",
        "what's your favorite color?": "I like all colors! But I mostly deal in black and white (code)."
    }

    # Default response if no match is found
    return responses.get(message, "I'm sorry, I didn't understand that. Can you try rephrasing?")

def main():
    host = '127.0.0.1'  # Localhost
    port = 12345        # Port to listen on

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen(1)  # Listen for 1 connection at a time
        print(f"Chatbot server is running on {host}:{port}...")

        while True:
            conn, addr = server_socket.accept()  # Accept incoming connections
            print(f"Connected by {addr}")
            with conn:
                while True:
                    # Step 1: Receive data from the client
                    data = conn.recv(1024).decode()
                    if not data or data.lower() == "exit":
                        print("Client disconnected.")
                        break

                    # Step 2: Generate a chatbot response
                    response = chatbot_response(data)

                    # Step 3: Send the response to the client
                    conn.sendall(response.encode())

if __name__ == "__main__":
    main()
