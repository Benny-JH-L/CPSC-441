s = "Accept-Ranges: bytes\r\nContent-Length: 2652\r\n"
position = s.find("\r\n")
print("pos of `\-r\-n`:", position)     # where the `\r\n` is located

position_of_content_length = s.find("Content-Length:")  # it gets the starting position of the string we find, then using the length of the
                                     # string we know we can get the whole thing
print('`s` at pos 5:', s[5])  


# sub_string = s[2 : 5]
print(s[1:2])

print('\ns =',repr(s))
content_length_str = "`Content-Length:`"
position_of_content_length = s.find("Content-Length:") 
print(f"pos of {content_length_str}:", position_of_content_length)
print(f"Starting char of {content_length_str}",s[position_of_content_length])
sub_string = s[position_of_content_length : position_of_content_length + len(content_length_str)]

print(f'getting the substring {content_length_str} from `s`:', sub_string)
s_length = len(s)
str_injection = " <injection> "
new_s = s[:position_of_content_length] + str_injection + s[position_of_content_length + len(content_length_str)-1:]
print(f'removing the sub string {content_length_str} from `s` and injecting some value:',repr(new_s))



raw_http_data2 = (
    "HTTP/1.1 200 OK\r\n"
    "Date: YYYY-MM-DD\r\n"
    "Content-Type: image/jpg\r\n"
    "Content-Length: 4242\r\n"
    "Another value :)\r\n"
    "\r\n"
    "<html><body>IMAGE DATA</body></html>"
    
    "HTTP/1.1 302 Found\r\n"
    "Location: https://example.com/login\r\n"
    "Content-Length: 0\r\n"
    "\r\n"
)

raw_http_data3 = (
    "HTTP/1.1 200 OK\r\n"
    "Date: YYYY-MM-DD\r\n"
    "Content-Type: image/jpg\r\n"
    "Content-Length: 4242\r\n"
    "Another value :)\r\n"
    "\r\n"
    "<html><body>IMAGE DATA</body></html>HTTP/1.1 302 Found\r\n"
    "Location: https://example.com/login\r\n"
    "Content-Length: 0\r\n"
    "\r\n"
)

# takes an entire response from a website and get's the separate replies and injects memes
def inject(message):
    list_of_responses = []
    # new_message = b''
    
    while message != b'':
        new_message = b'' # for when we are adding all the different responses to a list 
        pos_content_type = message.find(b'Content-Type: image/')  # find `Content-Type: image/``
        
        if pos_content_type == -1:    # can't find a header
            new_message += message
            list_of_responses.append(message)
            break
        
        # get meme extention, length, and data
        # with open(meme_path, 'rb') as file:
            # memeData = file.read()
            # memeExtention =  os.path.splitext(meme_path)[1][1:]    # get meme extention
            # newContentLength = len(memeData)
            
        # for this test i will use this 
        memeData = b'<MEME DATA :D>'
        memeExtention = b'png'
        newContentLength = len(memeData)
        
        newContentType = b'Content-Type: image/' + memeExtention
        newContentLength = b'Content-Length: ' + str(newContentLength).encode()
        
        # new_message += message[:pos_content_type] + newContentType + message[pos_content_type + len(newContentType):]            # replace the old content type with new content type by inserting it
        # pos_content_length = message.find(b'Content-Length: ')    # find `Content-Length:`
        # new_message += message[:pos_content_length] + newContentLength + message[pos_content_length + len(newContentLength):]     # replace the old content length with new content length by inserting it
        
        # replace content stuff
        # message = message[:pos_content_type] + newContentType + message[pos_content_type + len(newContentType):]            # replace the old content type with new content type by inserting it
        # print("\nreplaced content-type:\n",message) # debug
        # pos_content_length = message.find(b'Content-Length: ')    # find where `Content-Length:` is located
        # message = message[:pos_content_length] + newContentLength + message[pos_content_length + len(newContentLength):]    # replace the old content length with new content length by inserting it
        # print("\nreplaced content-length:\n",message) # debug
        
        new_message += message[:pos_content_type] + newContentType        # replace the old content type with new content type by inserting it
        
        print("\nreplaced content-type (new message is now):\n",new_message) # debug
        pos_content_length = message.find(b'Content-Length: ')    # find where `Content-Length:` is located
        new_message += message[pos_content_type + len(newContentType) :pos_content_length] + newContentLength   
        print("\nreplaced content-length(new message is now):\n",new_message) # debug
       
        pos_header_data_separator = message.find(b'\r\n\r\n')    # find the separator '\r\n\r\n`, that separates the header values and the data
    
        new_message += message[pos_content_length + len(newContentLength):pos_header_data_separator] # add all other header data after `content-length` to the new message that are before the separator '\r\n\r\n`
        print("\nAdding other:\n",new_message)
        pos_start_of_separator = pos_header_data_separator + 4
        
        # remove the data we went through in original message (header stuff)
        message = message[pos_start_of_separator:]
        print("\nRemoved header values (updated message is now):\n",message)
        
        # set new data
        new_message += b'\r\n\r\n' + memeData
        print("\nAdded memeData (to new message):\n",new_message)
        
        # update `message` by removing the old data
        print("\nmessage before removing old data:\n",message)
        pos_HTTP = message.find(b'HTTP/')   # find the next `HTTP`
        
        # case, this is not the last HTTP response, remove the data
        if (pos_HTTP != -1):    
            message = message[pos_HTTP:]
        # case, this is the last HTTP response, use location of '\r\n\r\n' separator and replace the old data
        else:
            print("\nmessage has not more repsonses (current message):",message)
            break
        
        # pos_HTTP = message.find(b'HTTP/')   # find the next `HTTP`
        # if (pos_HTTP == -1):    # case, this is the last HTTP response, use location of '\r\n\r\n' separator and replace the old data
        #     new_message += message[pos_before_old_data:] + memeData
        # else:                   # case, this is not the last HTTP response, replace old data
        #     # new_message += message[pos_before_old_data:] + memeData + message[pos_before_old_data + len(memeData):]
        #     new_message += message[pos_before_old_data:] + memeData


        print("\nmessage after removing old data:\n",message)
        print("\n`new message` currently:\n",new_message)
        list_of_responses.append(new_message) # when `new_message` is cleared for each loop
        
    # return new_message
    return list_of_responses

response_copy = raw_http_data2.encode()
injected_message = inject(response_copy)
print("\nbefore injection:\n",response_copy.decode())
print("\ninjected:\n",str(injected_message))
