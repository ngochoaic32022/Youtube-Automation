import os
import sys
import json
import urllib.parse
import requests

sys.stdout.reconfigure(encoding='utf-8')

VERIFIER = 'a_very_long_secure_code_verifier_1234567890_abcdefghijklmnopqrstuvwxyz'
CLIENT_SECRETS_FILE = 'd:/KENH GEHIHI/config/client_secrets_channel_3.json'
TOKEN_FILE = 'd:/KENH GEHIHI/config/tokens/token_channel_3.json'

with open(CLIENT_SECRETS_FILE, 'r', encoding='utf-8') as f:
    cfg = json.load(f)['installed']

def exchange(code_or_url: str):
    code = code_or_url.strip()
    if 'code=' in code:
        parsed = urllib.parse.urlparse(code)
        qs = urllib.parse.parse_qs(parsed.query)
        code = qs.get('code', [code])[0]

    print(f"[*] Exchanging code: {code[:15]}...")
    payload = {
        'code': code,
        'client_id': cfg['client_id'],
        'client_secret': cfg['client_secret'],
        'redirect_uri': 'http://localhost:8082/',
        'grant_type': 'authorization_code',
        'code_verifier': VERIFIER
    }

    r = requests.post('https://oauth2.googleapis.com/token', data=payload, timeout=15)
    if r.status_code != 200:
        print("[!] Token exchange failed:", r.status_code, r.text)
        return False

    tok_data = r.json()
    # Format credentials for google.oauth2.credentials.Credentials
    creds_format = {
        "token": tok_data.get("access_token"),
        "refresh_token": tok_data.get("refresh_token"),
        "token_uri": "https://oauth2.googleapis.com/token",
        "client_id": cfg['client_id'],
        "client_secret": cfg['client_secret'],
        "scopes": [
            "https://www.googleapis.com/auth/youtube",
            "https://www.googleapis.com/auth/youtube.force-ssl",
            "https://www.googleapis.com/auth/youtube.upload",
            "https://www.googleapis.com/auth/youtube.readonly"
        ],
        "universe_domain": "googleapis.com",
        "account": "",
        "expiry": None
    }

    os.makedirs(os.path.dirname(TOKEN_FILE), exist_ok=True)
    with open(TOKEN_FILE, 'w', encoding='utf-8') as f:
        json.dump(creds_format, f, indent=2)

    print("\n" + "=" * 60)
    print("[SUCCESS] TOKEN KÊNH 3 ĐÃ ĐƯỢC LƯU THÀNH CÔNG VĨNH VIỄN!")
    print(f"[+] Token file: {TOKEN_FILE}")
    print("=" * 60)
    return True

if __name__ == "__main__":
    if len(sys.argv) > 1:
        exchange(sys.argv[1])
    else:
        print("Usage: python exchange_token.py <code_or_url>")
