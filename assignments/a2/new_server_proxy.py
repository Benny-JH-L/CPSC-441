

# # takes in the entire message that was send from the site (ie the whole site),
# # and replaces half of the images to memes
# def injectMeme(wholeMessage):
    
#     pass

# def parse_http_responses(raw_response):
#     responses = []
#     parts = raw_response.split("\r\n\r\n", 1)  # First split (Headers/Body boundary)
#     print("Checking:",parts)
#     while parts:
#         headers_part, rest = parts  # Extract headers
#         header_lines = headers_part.split("\r\n")  # Split headers into lines
        
#         # First line is the status line
#         status_line = header_lines[0]
#         headers = {}
        
#         for line in header_lines[1:]:
#             if ": " in line:
#                 key, value = line.split(": ", 1)
#                 headers[key] = value

#         # Determine body length if Content-Length is set
#         content_length = int(headers.get("Content-Length", 0))
        
#         if content_length > 0:
#             body = rest[:content_length]
#             rest = rest[content_length:]  # Remove the extracted body from the remaining string
#         else:
#             body = ""

#         responses.append({"status": status_line, "headers": headers, "body": body})

#         # Look for the next response (if present)
#         parts = rest.split("\r\n\r\n", 1) if rest else []
#         print("Checking: ",parts)

#     return responses

# # Example usage with combined HTTP responses
# raw_data = (
#     "HTTP/1.1 200 OK\r\n"
#     "Content-Type: text/html\r\n"
#     "Content-Length: 27\r\n"
#     "\r\n"
#     "<html><body>Hello</body></html>\r\n"
#     "\r\n"
#     "HTTP/1.1 302 Found\r\n"
#     "Location: https://example.com/login\r\n"
#     "Content-Length: 0\r\n"
#     "\r\n"
# )

# parsed_responses = parse_http_responses(raw_data)

# for i, response in enumerate(parsed_responses, 1):
#     print(f"Response {i}:")
#     print(f"Status: {response['status']}")
#     print(f"Headers: {response['headers']}")
#     print(f"Body: {response['body']}\n")


# def split_http_responses(raw_response):
#     headers_list = []
#     bodies_list = []

#     parts = raw_response.split("\r\n\r\n", 1)  # Split first at the header-body boundary
    
#     while parts:
#         headers_part, rest = parts  # Extract headers
#         header_lines = headers_part.split("\r\n")  # Split headers into lines
        
#         # First line is the status line
#         status_line = header_lines[0]
#         headers = {"Status": status_line}

#         for line in header_lines[1:]:
#             if ": " in line:
#                 key, value = line.split(": ", 1)
#                 headers[key] = value

#         # Determine body length if Content-Length is set
#         content_length = int(headers.get("Content-Length", 0))
        
#         if content_length > 0:
#             body = rest[:content_length]
#             rest = rest[content_length:]  # Remove extracted body from remaining string
#         else:
#             body = ""

#         headers_list.append(headers)  # Store headers
#         bodies_list.append(body)  # Store body

#         # Look for the next response (if present)
#         parts = rest.split("\r\n\r\n", 1) if rest else []

#     return headers_list, bodies_list

# # Example combined HTTP response data
# raw_http_data = (
#     "HTTP/1.1 200 OK\r\n"
#     "Content-Type: text/html\r\n"
#     "Content-Length: 27\r\n"
#     "\r\n"
#     "<html><body>Hello</body></html>\r\n"
#     "\r\n"
#     "HTTP/1.1 302 Found\r\n"
#     "Location: https://example.com/login\r\n"
#     "Content-Length: 0\r\n"
#     "\r\n"
# )

# # Process response
# headers_list, bodies_list = split_http_responses(raw_http_data)

# # Print results
# for i in range(len(headers_list)):
#     print(f"Response {i + 1}:")
#     print(f"Headers: {headers_list[i]}")
#     print(f"Body: {bodies_list[i]}\n")


# Example combined HTTP response data
raw_http_data = (
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

def process(message):
    
    splitted = message.split("\r\n\r\n")
    print("\nSplitted message:\n", splitted) # debug
    
    # store the header-body pairs in lists, index of list will determine pair.
    listOfHeaders = []
    listOfBodys = []
    
    # Pair each header with its associated body
    for index in range(0, len(splitted), 2):   # will be pairing `index` (Header) with `index + 1` (Body)
        listOfHeaders.append(splitted[index])
        listOfBodys.append(splitted[index+1])
        
    #debug
    print("\nList of Headers:\n",listOfHeaders)
    print("\nList of Bodies:\n",listOfBodys)
    
    # Check if the header contains an image
    indexOfBody = 0
    for headers in listOfHeaders:
        header_values = headers.split("\r\n")
        
        lengthOfBody = 0
        # Go through eacher header value
        for aHeader in header_values: 
            
            # check if the header contains an image, if it does replace data
            if "Content-Type: image/" in aHeader:
                
                # find the "Content-Length" and replace the old data with the meme's data
                aHeader.split(": ", 1)  # get the header string and header length number
                    
                
                # replace image's randomly 
                pass
        
        print("\nHeader values:\n",header_values)
        print("\tBody length (in bytes): ", lengthOfBody)
        print("\tBody length (encoded): ", listOfBodys[indexOfBody].encode())

        indexOfBody = indexOfBody + 1
    
    
process(raw_http_data)


