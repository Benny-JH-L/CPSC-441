
import socket
import threading
import os
import random
from urllib.parse import urlparse

# Configuration
HOST = '127.0.0.1'  # Localhost
PORT = 8080         # Port to run the proxy on
DELAY = 1.0         # Delay in seconds per chunk of data
CHUNK_SIZE = 1024   # Size of data chunks to send

MEME_FOLDER_NAME = 'memes'
MEME_FOLDER_PATH = ""
EASTER_EGG_URL = b'http://google.ca/'
LIST_OF_MEME_NAMES = [] # List of meme file names inside the `MEME_FOLDER_NAME`
LIST_OF_MEME_PATHS = [] # Path to the meme (not sure if needed)
REPLACE_WITH_MEME = True


def find_memes_folder(start_path="."):
    for root, dirs, files in os.walk(start_path):
        if MEME_FOLDER_NAME in dirs:  # Found the "memes" folder
            return os.path.join(root, MEME_FOLDER_NAME)
    return None  # Return None if not found

# Gives the whole image path
def get_images_paths_from_folder(folder_path):
    image_extensions = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp"}
    return [
        os.path.join(folder_path, file)
        for file in os.listdir(folder_path)
        if os.path.splitext(file)[1].lower() in image_extensions
    ]

def get_image_names_from_folder(folder_path):
    image_extensions = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp"}
    return [
        file for file in os.listdir(folder_path)
        if os.path.splitext(file)[1].lower() in image_extensions
    ]


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

        # buffer = "" # stores the entire response from the site
        buffer = b'' # stores the entire response from the site
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
            
            # buffer += response.decode() # use .decode('utf-8') - ?
            # buffer += response.decode('utf-8') # nope?
            buffer += response
            # print(response)

        # proccessedMessage = processWholeSiteInfo(buffer)
        # client_socket.send(proccessedMessage)
        
        # client_socket.send(proccessedMessage.encode())
        # client_socket.sendall(proccessedMessage)
        print(buffer)
        client_socket.sendall(buffer)
        remote_socket.close()
    except Exception as e:
        print(f"Error: {e}")

    client_socket.close()


def processWholeSiteInfo(message):
    '''
    Proccesses the entire response from the site.
    Replaces 50% of images, with memes as well.
    '''
    global REPLACE_WITH_MEME
    
    print("\nOriginal Message:\n",message)  # debug
    
    splitted = message.split(b'\r\n\r\n')
    # splitted = message.split("\r\n\r\n")
    
    # print("\nSplitted message:\n", splitted) # debug
    
    # store the header-body pairs in lists, index of list will determine pair.
    listOfHeaders = []
    listOfBodys = []
    
    # Pair each header with its associated body
    for index in range(0, len(splitted), 2):   # will be pairing `index` (Header) with `index + 1` (Body)
        listOfHeaders.append(splitted[index])
        listOfBodys.append(splitted[index+1])
        
    #debug
    # print("\nList of Headers:\n",listOfHeaders)
    # for x in range(0, len(listOfHeaders)):
    #     print("\nUnchanged Header:\n" + listOfHeaders[x])
    
    #debug
    # print("\nList of Headers:\n",listOfHeaders)
    # for x in range(0, len(listOfHeaders)):
    #     print("\nUnchanged Header:\n" + str(listOfHeaders[x]))
        
    # print("\nList of Bodies:\n",listOfBodys)
    # print("\nEntered header checker:")
    
    # Check if the header contains an image
    indexOfHeader = 0
    indexOfBody = 0
    # for headers in listOfHeaders:
    for indexOfCurrentHeader in range(0, len(listOfHeaders)):
        # header_values = headers.split("\r\n")
        currentHeader = listOfHeaders[indexOfCurrentHeader]
        # listOfHeaderValues = currentHeader.split("\r\n")
        listOfHeaderValues = currentHeader.split(b'\r\n')
        
        
        # debug
        # print("\nCurrent header:\n" + currentHeader)
        # print("\tList of header values: ", listOfHeaderValues)
        # print("\nCurrent header:\n" + str(currentHeader))
        # print("\tList of header values: ", str(listOfHeaderValues))
        
        
        # Go through eacher header value
        # newConstructedHeader = ""
        newConstructedHeader = b''
        replacedContentType = False
        for headerValue in listOfHeaderValues: 
            # check if the header contains an image, if it does replace data
            # if "Content-Type: image/" in headerValue:
            if b'Content-Type: image/' in headerValue:
                # Alternate replaceing site's images (will replace half the sites images)
                if not REPLACE_WITH_MEME:
                    REPLACE_WITH_MEME = True
                    continue
                
                # get meme image
                randIndex = random.randint(0, len(LIST_OF_MEME_PATHS) - 1)
                meme_path = LIST_OF_MEME_PATHS[randIndex]
                
                print(f"Replacing image with meme: {meme_path}")  # Debug
                
                # memeExtention = ""
                memeExtention = b''
                newContentLength = 0
                memeData = 0
                with open(meme_path, 'rb') as file:
                    memeData = file.read()
                    # memeData = "MEME_DATA :D".encode()   # for debugging
                    memeExtention =  os.path.splitext(meme_path)[1][1:]    # get meme extention
                    newContentLength = len(memeData)
                # newContentType = "Content-Type: image/" + memeExtention + "\r\n"
                # newContentLengthStr = "Content-Length: " + str(newContentLength) + "\r\n"
                
                # newContentType = b'Content-Type: image/' + memeExtention + b'\r\n'
                newContentType = b'Content-Type: image/' + memeExtention.encode() + b'\r\n'
                # newContentLengthStr = b'Content-Length: ' + str(newContentLength) + b'\r\n'
                newContentLengthStr = b'Content-Length: ' + str(newContentLength).encode() + b'\r\n'
                
                # replace the old header values for content type and length
                newConstructedHeader += newContentType
                newConstructedHeader += newContentLengthStr
                # listOfBodys[indexOfCurrentHeader] = memeData   # replace the body data with the meme data (decode to get string)
                listOfBodys[indexOfCurrentHeader] = memeData + b'\r\n\r\n'   # replace the body data with the meme data (decode to get string)
                
                REPLACE_WITH_MEME = False
                replacedContentType = True
            # Add the old header value to the construction
            # elif "Content-Length: " in headerValue:  # skip content-length since i already replaced its data
            elif b'Content-Length: ' in headerValue:  
                if replacedContentType: # skip content-length since i already replaced its data
                    replacedContentType = False # reset switch
                    continue
                else:
                    newConstructedHeader += headerValue + b'\r\n'
            else:
                # newConstructedHeader += headerValue + "\r\n"
                newConstructedHeader += headerValue + b'\r\n'
        
        # Set new construction of header
        # listOfHeaders[indexOfCurrentHeader] = newConstructedHeader + "\r\n"
        listOfHeaders[indexOfCurrentHeader] = newConstructedHeader + b'\r\n'
        
        indexOfBody = indexOfBody + 1
        indexOfHeader = indexOfHeader + 1
        
    # debug
    # print("\nNew Header values:\n", listOfHeaders)
    # print("\nNew header values:\n")
    # for x in range(0, len(listOfHeaders)):
    #     print("------------\n" + listOfHeaders[x])
    #     # print("Body val:", str(listOfBodys[x]) + "\n------------")
    #     print("Body val: <thing :), string of byte data is too large> \n------------")
    
    # return the processed message
    # newMessage = ""
    newMessage = b''
    for index in range(0, len(listOfHeaders)):
        # newMessage += listOfHeaders[index] + "\r\n" + str(listOfBodys[index]) + "\r\n\r\n"
        # newMessage += listOfHeaders[index] + b'\r\n' + listOfBodys[index] + b'\r\n\r\n'
        # newMessage += listOfHeaders[index] + b'\r\n' + listOfBodys[index]
        newMessage += listOfHeaders[index] + listOfBodys[index]
        
    return newMessage
    
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


# Example HTTP response data
raw_http_data1 = (
    "HTTP/1.1 200 OK\r\n"
    "Content-Type: text/html\r\n"
    "Content-Length: 27\r\n"
    "\r\n"
    "<html><body>Hello</body></html>\r\n"
    "\r\n"
    "HTTP/1.1 302 Found\r\n"
    "Location: https://example.com/login\r\n"
    "Content-Length: 0\r\n"
    "\r\n"
)

raw_http_data2 = (
    "HTTP/1.1 200 OK\r\n"
    "Content-Type: image/jpg\r\n"
    "Content-Length: 4242\r\n"
    "\r\n"
    "<html><body>IMAGE DATA</body></html>\r\n"
    "\r\n"
    "HTTP/1.1 302 Found\r\n"
    "Location: https://example.com/login\r\n"
    "Content-Length: 0\r\n"
    "\r\n"
)

if __name__ == "__main__":# Find the "memes" folder starting from the current directory
    MEME_FOLDER_PATH = find_memes_folder(".")
    LIST_OF_MEME_NAMES = get_image_names_from_folder(MEME_FOLDER_PATH)
    LIST_OF_MEME_PATHS = get_images_paths_from_folder(MEME_FOLDER_PATH)
    print("\nImage names:\n", LIST_OF_MEME_NAMES) # debug
    print("\nImage paths:\n",LIST_OF_MEME_PATHS) # debug
    start_proxy()

    # debugging
    # m = processWholeSiteInfo(raw_http_data2)
    # print("\nBefore processed:\n" + raw_http_data2)
    # print("\nProccessed:\n" + m)  
    # m2 = process(raw_http_data1)
    # print("\nBefore processed:\n" + raw_http_data1)
    # print("\nProccessed:\n" + m2)  
    # m = processWholeSiteInfo(raw_http_data2.encode())
    # print("\nBefore processed:\n" + raw_http_data2)
    # print("\nProccessed:\n",m)  

