import functools
import http.server
import socketserver

DIRECTORY = "/Users/patrycjakaczorowska/Downloads/Vorlagen/claude-workspace-vorlage/outputs"
PORT = 8910

Handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=DIRECTORY)

with socketserver.TCPServer(("127.0.0.1", PORT), Handler) as httpd:
    print(f"Serving {DIRECTORY} at http://127.0.0.1:{PORT}")
    httpd.serve_forever()
