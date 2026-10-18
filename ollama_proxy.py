import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

TOKEN = os.environ.get("OLLAMA_PROXY_TOKEN")
HOST = "127.0.0.1"
PORT = 8765

if not TOKEN:
    raise SystemExit("Missing OLLAMA_PROXY_TOKEN environment variable")

class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path != "/api/chat":
            self.send_error(404)
            return

        if self.headers.get("Authorization") != f"Bearer {TOKEN}":
            self.send_error(401, "Unauthorized")
            return

        try:
            length = int(self.headers.get("Content-Length", "0"))
            if length <= 0 or length > 1_000_000:
                self.send_error(413, "Invalid request size")
                return

            body = self.rfile.read(length)
            payload = json.loads(body)

            if payload.get("model") != "llama3.2:1b":
                self.send_error(400, "Model not allowed")
                return

            request = Request(
                "http://127.0.0.1:11434/api/chat",
                data=json.dumps(payload).encode(),
                headers={"Content-Type": "application/json"},
                method="POST",
            )

            with urlopen(request, timeout=300) as response:
                result = response.read()

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(result)))
            self.end_headers()
            self.wfile.write(result)

        except HTTPError as exc:
            self.send_error(exc.code)
        except (ValueError, URLError, TimeoutError) as exc:
            self.send_error(502, "Local Ollama request failed")
        except Exception:
            self.send_error(500, "Proxy error")

    def log_message(self, format, *args):
        print("Proxy request:", args[0])

server = ThreadingHTTPServer((HOST, PORT), Handler)
print(f"Protected Ollama proxy listening on {HOST}:{PORT}")
server.serve_forever()
