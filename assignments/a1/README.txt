
Assignment 1: Advanced Palindrome Check Server-Client Application
    CPSC 441 Winter 2025 | Benny Liang | 30192142

---Compile/Running---
Like any Python code, to run the server and client files in the terminal:
`python <client/server file name>.py`
(Note: should run the server file first then any client instances, ie more than one client)

------


---Example inputs/outputs---

--Complex palindrome check
    "cbbici" -> return can form palindrome true and complexity score of 2
    "ivicc" -> return can form palindrome true and complexity score of 2
    "erbwerhwh" -> return can form palindrome true and complexity score of 3
    "iiikckaacc" -> return impossible to form palindrome

--Simple palindrome check
    "cbbici" -> Is palindrome: False
    "erbwerhwh" -> Is palindrome: False
    "civic" -> Is palindrome: True
 
------


---About Bonus (Encryption)---
I chose to implement a simple cipher, a caeser cipher specifically (with a shift of 7, shifts each letter over 7 letters).
Before the `input_string` is sent from the client to the server it is encryped with this cipher, and
the server decrypts (using the caesar cipher with a -7 shift) the sent message. After the server finishes computing the task specified in the message, it is encrypted
and sent back to the client. On the client side, the recieved message is decrypted and displayed to the user.

(Note: On the server side, the sent/recieved messages are logged in their encryped forms)
------


---Difficulties faced---
Implementing the complex palindrome check

