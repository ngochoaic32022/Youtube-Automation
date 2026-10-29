import os
import sys
from google_auth_oauthlib.flow import InstalledAppFlow

# Force unbuffered UTF-8
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

SCOPES = [
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/youtube.readonly"
]

CLIENT_SECRETS_FILE = "d:/KENH GEHIHI/config/client_secrets.json"

def authenticate_channel(channel_id="channel_1", port=8080):
    token_dir = "d:/KENH GEHIHI/config/tokens"
    os.makedirs(token_dir, exist_ok=True)
    token_file = os.path.join(token_dir, f"token_{channel_id}.json")

    print("=" * 65, flush=True)
    print(f"[*] BẮT ĐẦU XÁC THỰC QUYỀN YOUTUBE CHO: {channel_id}", flush=True)
    print("=" * 65, flush=True)

    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
    
    # Must explicitly set redirect_uri before generating the authorization url
    flow.redirect_uri = f"http://localhost:{port}/"
    auth_url, _ = flow.authorization_url(prompt='consent', access_type='offline')
    
    print("\n👉 BƯỚC 1: Hãy COPY đường link chuẩn dưới đây (đã fix redirect_uri):", flush=True)
    print("-" * 65, flush=True)
    print(auth_url, flush=True)
    print("-" * 65, flush=True)
    print("👉 BƯỚC 2: Dán đường link trên vào trình duyệt Antidesk.", flush=True)
    print("👉 BƯỚC 3: Chọn tài khoản và bấm 'Tiếp tục' -> 'Cho phép (Allow)'.", flush=True)
    print("\n[*] Đang mở server cục bộ đón mã xác nhận...", flush=True)

    creds = flow.run_local_server(port=port, open_browser=False)

    with open(token_file, "w") as token:
        token.write(creds.to_json())

    print("\n" + "=" * 65, flush=True)
    print(f"[XÁC THỰC THÀNH CÔNG] ĐÃ KẾT NỐI VĨNH VIỄN VỚI KÊNH {channel_id}!", flush=True)
    print(f"[+] Token file: {token_file}", flush=True)
    print("=" * 65, flush=True)

if __name__ == "__main__":
    cid = sys.argv[1] if len(sys.argv) > 1 else "channel_1"
    authenticate_channel(cid)
