import json
from http.server import BaseHTTPRequestHandler, HTTPServer

# In-memory database for storing products
products = []

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            # Handle root path
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            # Simple HTML response for the root path
            self.wfile.write(b"<h1>Welcome to the Product API</h1><p>Use <code>/products</code> to interact with the API.</p>")
        elif self.path == '/products':
            # Respond with the list of products
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(products).encode('utf-8'))
        else:
            # Respond with 404 for unknown paths
            self.send_response(404)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'error': 'Not Found'}).encode('utf-8'))

    def do_POST(self):
        if self.path == '/products':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            try:
                # Parse the JSON data
                data = json.loads(post_data)

                # Validate required fields
                if not all(key in data for key in ('name', 'description', 'price')):
                    self.send_response(400)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({'error': 'Invalid data'}).encode('utf-8'))
                    return
                
                # Add product to the in-memory database
                product = {
                    'id': len(products) + 1,
                    'name': data['name'],
                    'description': data['description'],
                    'price': float(data['price'])
                }
                products.append(product)

                # Respond with 201 Created
                self.send_response(201)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(product).encode('utf-8'))
            except (json.JSONDecodeError, ValueError):
                self.send_response(400)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'error': 'Invalid JSON or price format'}).encode('utf-8'))

def run_server():
    server_address = ('', 5000)  # Listen on all interfaces, port 5000
    httpd = HTTPServer(server_address, RequestHandler)
    print("Server running on http://127.0.0.1:5000")
    httpd.serve_forever()

if __name__ == '__main__':
    run_server()
