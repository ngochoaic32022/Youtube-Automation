import os
import sys
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

CLIENT_SECRETS_FILE = "d:/KENH GEHIHI/config/client_secrets_channel_2.json"

def authenticate_channel_2(port=8081):
    token_dir = "d:/KENH GEHIHI/config/tokens"
    os.makedirs(token_dir, exist_ok=True)
    token_file = os.path.join(token_dir, "token_channel_2.json")

    print("=" * 65, flush=True)
    print(f"[*] BẮT ĐẦU XÁC THỰC QUYỀN TỐI ƯU HÓA CHO KÊNH 2", flush=True)
    print("=" * 65, flush=True)

    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
    flow.redirect_uri = f"http://localhost:{port}/"
    auth_url, _ = flow.authorization_url(prompt='consent', access_type='offline')

    print("\n👉 BƯỚC 1: Hãy COPY đường link xác thực bên dưới:", flush=True)
    print("-" * 65, flush=True)
    print(auth_url, flush=True)
    print("-" * 65, flush=True)
    print("👉 BƯỚC 2: Dán vào trình duyệt Antidesk đang đăng nhập Kênh 2.", flush=True)
    print("👉 BƯỚC 3: Bấm 'Tiếp tục' -> 'Cho phép (Allow)'.", flush=True)
    print("\n[*] Đang lắng nghe phản hồi xác nhận trên port 8081...", flush=True)

    creds = flow.run_local_server(port=port, open_browser=False)

    with open(token_file, "w") as token:
        token.write(creds.to_json())

    print("\n" + "=" * 65, flush=True)
    print("[SUCCESS] ĐÃ KẾT NỐI VĨNH VIỄN VỚI KÊNH 2!", flush=True)
    print(f"[+] Token file: {token_file}", flush=True)
    print("=" * 65, flush=True)

if __name__ == "__main__":
    authenticate_channel_2(8081)
