import os
import sys
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from google_auth_oauthlib.flow import InstalledAppFlow

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

SCOPES = [
    "https://www.googleapis.com/auth/youtube",
    "https://www.googleapis.com/auth/youtube.force-ssl",
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/youtube.readonly"
]

CLIENT_SECRETS_FILE = "d:/KENH GEHIHI/config/client_secrets_channel_3.json"
TOKEN_DIR = "d:/KENH GEHIHI/config/tokens"
TOKEN_FILE = os.path.join(TOKEN_DIR, "token_channel_3.json")
PORT = 8082

flow = None
creds_saved = False

class OAuthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global creds_saved
        try:
            full_url = f"http://localhost:{PORT}{self.path}"
            flow.fetch_token(authorization_response=full_url)
            creds = flow.credentials
            os.makedirs(TOKEN_DIR, exist_ok=True)
            with open(TOKEN_FILE, "w", encoding="utf-8") as f:
                f.write(creds.to_json())
            creds_saved = True

            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            html = "<h1>Xac thuc thanh cong!</h1><p>Ban co the dong tab nay.</p>"
            self.wfile.write(html.encode("utf-8"))
            print("\n[SUCCESS] DA LUU TOKEN KENH 3 THANH CONG!")
            print(f"[+] Token file: {TOKEN_FILE}")
        except Exception as e:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(f"Error: {e}".encode("utf-8"))
            print(f"[!] Error fetching token: {e}")

    def log_message(self, format, *args):
        pass

def start_server():
    global flow
    flow = InstalledAppFlow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=SCOPES,
        redirect_uri=f"http://localhost:{PORT}/"
    )
    auth_url, state = flow.authorization_url(prompt='consent', access_type='offline')

    print("=" * 65, flush=True)
    print(f"[*] SERVER XAC THUC CHO KÊNH 3 DANG CHAY TAI PORT {PORT}", flush=True)
    print("=" * 65, flush=True)
    print("\n👉 LINK XAC THUC:", flush=True)
    print(auth_url, flush=True)
    print("\n[*] Dang cho redirect hoac request...", flush=True)

    server = HTTPServer(("localhost", PORT), OAuthHandler)
    while not creds_saved:
        server.handle_request()

if __name__ == "__main__":
    start_server()
