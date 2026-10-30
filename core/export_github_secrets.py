# Helper script to print GitHub Secrets for copy-pasting
import os
import sys

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

SECRETS = [
    ("TOKEN_CHANNEL_1", "config/tokens/token_channel_1.json"),
    ("TOKEN_CHANNEL_2", "config/tokens/token_channel_2.json"),
    ("TOKEN_CHANNEL_3", "config/tokens/token_channel_3.json"),
    ("PROXIES_JSON", "config/proxies.json"),
    ("PEXELS_API_KEY", "config/api_keys.json"),
    ("GEMINI_API_KEY", "config/api_keys.json"),
]

print("=" * 60)
print("GITHUB REPOSITORY SECRETS DATA")
print("Truy cập: Repo GitHub -> Settings -> Secrets and variables -> Actions")
print("Bấm 'New repository secret' và thêm các giá trị sau:")
print("=" * 60)

for secret_name, file_path in SECRETS:
    print(f"\n>>> TÊN SECRET: {secret_name}")
    print("-" * 40)
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read().strip()
            if secret_name in ("PEXELS_API_KEY", "GEMINI_API_KEY"):
                import json
                try:
                    data = json.loads(content)
                    print(data.get(secret_name, ""))
                except Exception:
                    print(content)
            else:
                print(content)
    else:
        print(f"[ERROR: Không tìm thấy {file_path}]")
    print("-" * 40)
