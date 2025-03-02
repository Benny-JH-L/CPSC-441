
Assignment 2: Build a Meme-Generating Proxy Server
    CPSC 441 Winter 2025 | Benny Liang | 30192142

---For the server proxy to detect the user's web browsing, please use the FireFox browser---

In the `Settings` for FireFox:
    - Inside `General` scroll to bottom of the page until you see `Network Settings`.
    - Click on `Settings` to configure the `Network Settings`. 
Inside `Connection Settings` (`Network Settings`)
    - Select `Manual proxy configuration`
    - Next to `HTTP Proxy`, put `127.0.0.1` in the long text area, and for port put `8080`.
    - Lastly hit `OK`.

Now the server proxy will be able to listen to the user browsing in FireFox.

------

---Compile/Running---
Like any Python code, to run the server and client files in the terminal:
`python <client/server file name>.py`
(Note: should run the server file first then any client instances, ie more than one client)

------

