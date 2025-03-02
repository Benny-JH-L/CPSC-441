import re

def parse_http_response(response: bytes):
    """
    Parses an HTTP response, extracting headers and handling chunked transfer encoding.
    :param response: The raw HTTP response as bytes.
    :return: A tuple (headers: dict, body: bytes)
    """
    # Split headers and body
    header_end = response.find(b"\r\n\r\n")
    if header_end == -1:
        raise ValueError("Invalid HTTP response: No header-body separator found.")
    
    header_section = response[:header_end].decode("utf-8")
    body_section = response[header_end + 4:]
    
    # Parse headers into a dictionary
    headers = {}
    header_lines = header_section.split("\r\n")
    status_line = header_lines[0]  # Example: "HTTP/1.1 200 OK"
    headers["Status-Line"] = status_line
    
    for line in header_lines[1:]:
        key, value = line.split(": ", 1)
        headers[key] = value
    
    # Handle chunked transfer encoding
    if headers.get("Transfer-Encoding") == "chunked":
        body = decode_chunked_body(body_section)
    else:
        body = body_section
    
    return headers, body

def decode_chunked_body(body: bytes):
    """
    Decodes a chunked transfer-encoded body.
    :param body: The chunked response body as bytes.
    :return: The decoded body as bytes.
    """
    decoded_body = b""
    while body:
        # Get the chunk size
        chunk_size_end = body.find(b"\r\n")
        if chunk_size_end == -1:
            raise ValueError("Invalid chunked encoding: No chunk size delimiter found.")
        
        chunk_size = int(body[:chunk_size_end].decode("utf-8"), 16)
        if chunk_size == 0:
            break  # Last chunk (0) means end of message
        
        # Extract the chunk data
        chunk_start = chunk_size_end + 2
        chunk_end = chunk_start + chunk_size
        decoded_body += body[chunk_start:chunk_end]
        
        # Move to the next chunk (skip trailing \r\n)
        body = body[chunk_end + 2:]
    
    return decoded_body

# Example usage
raw_response = (
    b"HTTP/1.1 200 OK\r\n"
    b"Date: Sun, 02 Mar 2025 05:28:04 GMT\r\n"
    b"Content-Type: text/html; charset=UTF-8\r\n"
    b"Transfer-Encoding: chunked\r\n"
    b"Connection: keep-alive\r\n"
    b"Server: Apache\r\n"
    b"X-Powered-By: PHP/7.4.33\r\n"
    b"Access-Control-Allow-Origin: *\r\n"
    b"\r\n"
    b"5\r\nHello\r\n"
    b"6\r\n World\r\n"
    b"0\r\n\r\n"
)

headers, body = parse_http_response(raw_response)
print("Headers:", headers)
print("Body:", body.decode("utf-8"))
