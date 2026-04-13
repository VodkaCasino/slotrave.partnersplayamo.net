#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import webbrowser
import http.server
import socketserver
import threading
import time
from pathlib import Path
PORT = 8000
class BrotliIndexHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path in ("/", "/index.html"):
            base_dir = Path(os.getcwd())
            br_path = base_dir / "index.html"
            if br_path.exists():
                try:
                    with br_path.open("rb") as f:
                        data = f.read()
                    self.send_response(200)
                    self.send_header("Content-Type", "text/html; charset=utf-8")
                    self.send_header("Content-Encoding", "")
                    self.send_header("Content-Length", str(len(data)))
                    self.end_headers()
                    self.wfile.write(data)
                    return
                except Exception as e:
                    print(f"NO: {e}")
        super().do_GET()
def start_server(directory: str) -> None:
    os.chdir(directory)
    handler = BrotliIndexHandler
    httpd = socketserver.TCPServer(("", PORT), handler)
    print(f"FRANCE http://localhost:{PORT}")
    httpd.serve_forever()
def open_html_in_browser() -> None:
    script_dir = Path(__file__).parent
    html_file = script_dir / "index.html"
    br_file = script_dir / "index.html."
    if not html_file.exists() and not br_file.exists():
        print(f"ERROR: NO {html_file.name}, NO {br_file.name} YES {script_dir}!")
        return
    server_thread = threading.Thread(
        target=start_server,
        args=(str(script_dir),),
        daemon=True,
    )
    server_thread.start()
    time.sleep(1)
    url = f"http://localhost:{PORT}/index.html"
    print("OPEN")
    print(f"URL: {url}")
    print("\n.YES.")
    webbrowser.open(url)
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\NO")
if __name__ == "__main__":
    open_html_in_browser()