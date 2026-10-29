import os
import sys
import json
import requests
import httplib2
import socks
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import google_auth_httplib2

sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PROXIES_FILE = os.path.join(ROOT_DIR, "config", "proxies.json")
TOKEN_DIR = os.path.join(ROOT_DIR, "config", "tokens")

def load_proxy_config(channel_id: str) -> dict:
    with open(PROXIES_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
    if channel_id not in data:
        raise ValueError(f"No proxy configured for {channel_id}")
    return data[channel_id]

def verify_proxy_ip(channel_id: str) -> str:
    """Kiểm tra IP thực tế qua Proxy trước khi cho phép gọi API"""
    cfg = load_proxy_config(channel_id)
    proxy_url = f"socks5://{cfg['user']}:{cfg['pass']}@{cfg['host']}:{cfg['port']}"
    
    endpoints = [
        "http://api.ipify.org",
        "http://checkip.amazonaws.com",
        "http://icanhazip.com"
    ]
    out_ip = None
    for ep in endpoints:
        try:
            resp = requests.get(ep, proxies={"http": proxy_url, "https": proxy_url}, timeout=8)
            out_ip = resp.text.strip()
            if out_ip:
                break
        except Exception:
            continue
            
    if not out_ip:
        raise RuntimeError(f"CRITICAL: Proxy check failed for {channel_id}: Unable to connect to IP check endpoints. ABORTING.")
        
    if out_ip != cfg["expected_ip"]:
        raise RuntimeError(f"CRITICAL: Proxy IP mismatch for {channel_id}! Expected {cfg['expected_ip']}, got {out_ip}. ABORTING.")
        
    print(f"[+] Proxy verified for {channel_id}: Outbound IP = {out_ip} (MATCH 100%)")
    return out_ip

def get_proxy_youtube_client(channel_id: str):
    """Tạo YouTube API Client đã được HARD-LOCK định tuyến qua Proxy riêng của kênh"""
    cfg = load_proxy_config(channel_id)
    
    # 1. Bắt buộc kiểm tra IP trước (Pre-flight Hard Check)
    verify_proxy_ip(channel_id)
    
    # 2. Đọc token xác thực
    token_file = os.path.join(TOKEN_DIR, f"token_{channel_id}.json")
    with open(token_file, 'r', encoding='utf-8') as f:
        token_info = json.load(f)
    creds = Credentials.from_authorized_user_info(token_info)

    # 3. Tạo kết nối mạng bị khóa chặt vào Proxy SOCKS5
    proxy_info = httplib2.ProxyInfo(
        proxy_type=httplib2.socks.PROXY_TYPE_SOCKS5,
        proxy_host=cfg['host'],
        proxy_port=cfg['port'],
        proxy_user=cfg['user'],
        proxy_pass=cfg['pass']
    )
    http = httplib2.Http(proxy_info=proxy_info, timeout=60)
    authed_http = google_auth_httplib2.AuthorizedHttp(creds, http=http)

    # 4. Trả về client YouTube chỉ giao tiếp qua Proxy
    yt = build('youtube', 'v3', http=authed_http)
    return yt

if __name__ == '__main__':
    for ch in ['channel_1', 'channel_2']:
        print(f"\n--- Testing Hard-Lock Proxy for {ch} ---")
        yt = get_proxy_youtube_client(ch)
        resp = yt.channels().list(part='snippet', mine=True).execute()
        print(f"[✓] {ch} Connected via Proxy! Channel: {resp['items'][0]['snippet']['title']}")
