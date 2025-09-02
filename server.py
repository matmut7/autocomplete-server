import json
import logging
import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse

from files import load_words_from_directory
from strings import search_with_prefix

RESULT_MAX_LENGTH = int(os.environ.get("RESULT_MAX_LENGTH", "20"))
DICTIONARIES_DIR = os.environ.get("DICTIONARIES_DIR", "./dictionaries")

HOST = os.environ.get("HOST", "0.0.0.0")
PORT = int(os.environ.get("PORT", "8000"))
LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")

logging.basicConfig(level=getattr(logging, LOG_LEVEL, logging.INFO))

words = load_words_from_directory(DICTIONARIES_DIR)
logging.info("Loaded %d words from %s", len(words), DICTIONARIES_DIR)


class AutocompleteHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)

        if parsed.path == "/healthz":
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"ok")
            return

        if parsed.path != "/autocomplete":
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Not Found")
            return

        qs = parse_qs(parsed.query)
        query = (qs.get("query") or [""])[0]

        if not query:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b'Missing "query" parameter')
            return

        result = search_with_prefix(words=words, prefix=query, limit=RESULT_MAX_LENGTH)
        payload = json.dumps(result, ensure_ascii=False).encode(encoding="utf-8")

        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def log_message(self, format, *args):
        logging.info("%s - %s", self.client_address[0], format % args)


def main():
    server = HTTPServer((HOST, PORT), AutocompleteHandler)
    logging.info("Server running on http://%s:%d", HOST, PORT)
    server.serve_forever()


if __name__ == "__main__":
    main()
