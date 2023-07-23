import http.server
import socketserver

class MyRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Content-type", "text/plain")
        self.end_headers()

        content_length = int(self.headers['Content-Length'])
        data = self.rfile.read(content_length).decode('utf-8')
        if data == "marco":
            self.wfile.write("polo".encode('utf-8'))

PORT = 8888
Handler = MyRequestHandler
httpd = socketserver.TCPServer(("", PORT), Handler)

print("Server is listening on port", PORT)
httpd.serve_forever()