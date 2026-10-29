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
]

print("=" * 60)
print("GITHUB REPOSITORY SECRETS DATA")
print("Truy cập: Repo GitHub -> Settings -> Secrets and variables -> Actions")
print("Bấm 'New repository secret' và thêm lần lượt 4 giá trị sau:")
print("=" * 60)

for secret_name, file_path in SECRETS:
    print(f"\n>>> TÊN SECRET: {secret_name}")
    print("-" * 40)
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            print(f.read().strip())
    else:
        print(f"[ERROR: Không tìm thấy {file_path}]")
    print("-" * 40)
