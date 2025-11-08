# Placeholder for LIRA API
import http.server
import socketserver
import yaml
import os

# --- Configuration Loading ---
def load_config():
    """Loads the configuration from config/lira.yaml"""
    # The script is in core/, so we go one level up to find the config
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'lira.yaml')
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

config = load_config()
PORT = config.get('api', {}).get('port', 1312)
MODEL_NAME = config.get('model', {}).get('main_model', 'gemma2:9b')

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(f"LIRA API is running!\n".encode('utf-8'))
        self.wfile.write(f"Using model: {MODEL_NAME}".encode('utf-8'))

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"LIRA API server started at port {PORT}")
    print(f"Core model configured: {MODEL_NAME}")
    httpd.serve_forever()