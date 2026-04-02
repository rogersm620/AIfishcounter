import os
import base64
import json
import urllib.request
import urllib.error
from http.server import HTTPServer, BaseHTTPRequestHandler

API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
PORT = int(os.environ.get("PORT", 8000))


def count_fry(image_b64):
    payload = json.dumps({
        "model": "claude-sonnet-4-20250514",
        "max_tokens": 300,
        "messages": [{
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": "image/jpeg",
                        "data": image_b64
                    }
                },
                {
                    "type": "text",
                    "text": (
                        "This is a top-down photo of juvenile fish fry in a container or bucket. "
                        "Count every individual fish fry you can see. "
                        "Reply ONLY with valid JSON, no markdown, no extra text. "
                        'Format exactly: {"count": 42, "confidence": "high", "note": "brief observation"}. '
                        "Confidence must be high, medium, or low."
                    )
                }
            ]
        }]
    }).encode("utf-8")

    req = urllib.request.Request(
        "https://api.anthropic.com/v1/messages",
        data=payload,
        headers={
            "Content-Type": "application/json",
            "x-api-key": API_KEY,
            "anthropic-version": "2023-06-01"
        },
        method="POST"
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    text = next((b["text"] for b in data.get("content", []) if b.get("type") == "text"), "{}")
    text = text.replace("```json", "").replace("```", "").strip()
    return json.loads(text)


class Handler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass  # suppress default logging noise

    def send_json(self, code, obj):
        body = json.dumps(obj).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def send_file(self, path, content_type):
        with open(path, "rb") as f:
            body = f.read()
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        if self.path in ("/", "/index.html"):
            self.send_file(os.path.join(os.path.dirname(__file__), "static", "index.html"), "text/html")
        else:
            self.send_json(404, {"error": "not found"})

    def do_POST(self):
        if self.path != "/count":
            self.send_json(404, {"error": "not found"})
            return

        if not API_KEY:
            self.send_json(500, {"error": "ANTHROPIC_API_KEY not set on server"})
            return

        length = int(self.headers.get("Content-Length", 0))
        body = json.loads(self.rfile.read(length).decode("utf-8"))
        image_b64 = body.get("image")

        if not image_b64:
            self.send_json(400, {"error": "missing image field"})
            return

        try:
            result = count_fry(image_b64)
            self.send_json(200, result)
        except urllib.error.HTTPError as e:
            err_body = e.read().decode("utf-8")
            self.send_json(500, {"error": f"Anthropic API error {e.code}: {err_body}"})
        except Exception as e:
            self.send_json(500, {"error": str(e)})


if __name__ == "__main__":
    if not API_KEY:
        print("WARNING: ANTHROPIC_API_KEY environment variable is not set.")
    print(f"Starting fry counter server on port {PORT}...")
    server = HTTPServer(("0.0.0.0", PORT), Handler)
    server.serve_forever()
