# For the hosting

import os
from http.server import BaseHTTPRequestHandler, HTTPServer

from dotenv import load_dotenv

load_dotenv()
class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_HEAD(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Server "MicroMightyBot" is online!')

def start_http_server():
    server_address = ('', int(os.getenv("PORT")))
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    print(f"Serving on port {os.getenv('PORT')}...")
    httpd.serve_forever()

if __name__ == "__main__":
    start_http_server()