import os
import sys

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT_DIR)

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

import json
from datetime import datetime
from core.proxy_manager import get_proxy_youtube_client

CHANNELS = [
    ("channel_1", "Kỳ Thú Khám Phá", "171.241.66.158"),
    ("channel_2", "Vintage Holiday Classics", "14.250.193.244"),
    ("channel_3", "Stoic Echoes", "171.245.160.235")
]

def report_all():
    print(f"\n{'='*75}")
    print(f"📊 BÁO CÁO TOÀN DIỆN 3 KÊNH YOUTUBE AUTOMATION")
    print(f"⏰ Thời điểm đối soát: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')} (GMT+7)")
    print(f"{'='*75}\n")

    for ch_id, ch_name, expected_ip in CHANNELS:
        print(f"\n>>> 🔹 ĐANG ĐỐI SOÁT: {ch_name} (ID: {ch_id})")
        print(f"    Proxy bắt buộc: {expected_ip}")

        try:
            youtube = get_proxy_youtube_client(ch_id)
            print("    ✅ Đã xác thực Proxy & Google OAuth thành công.")

            # 1. Channel stats
            c_res = youtube.channels().list(mine=True, part="snippet,contentDetails,statistics").execute()
            items = c_res.get("items", [])
            if not items:
                print(f"    ❌ Không tìm thấy thông tin kênh.")
                continue

            item = items[0]
            title = item["snippet"]["title"]
            custom_url = item["snippet"].get("customUrl", "")
            stats = item["statistics"]
            uploads_id = item["contentDetails"]["relatedPlaylists"]["uploads"]

            print(f"    📌 Tên hiển thị: {title} ({custom_url})")
            print(f"    📈 Subscribers: {stats.get('subscriberCount', '0')}")
            print(f"    👀 Tổng lượt xem: {int(stats.get('viewCount', 0)):,}")
            print(f"    🎬 Tổng số video: {stats.get('videoCount', '0')}")

            # 2. Latest 3 videos
            p_res = youtube.playlistItems().list(
                playlistId=uploads_id,
                part="snippet,contentDetails",
                maxResults=3
            ).execute()

            v_ids = [p["contentDetails"]["videoId"] for p in p_res.get("items", [])]
            if v_ids:
                v_res = youtube.videos().list(
                    id=",".join(v_ids),
                    part="snippet,statistics,status,contentDetails"
                ).execute()

                print(f"    📽️ Video gần đây nhất:")
                for v in v_res.get("items", []):
                    vid = v["id"]
                    v_title = v["snippet"]["title"]
                    pub_at = v["snippet"]["publishedAt"]
                    status = v.get("status", {}).get("privacyStatus", "unknown")
                    views = int(v.get("statistics", {}).get("viewCount", 0))
                    likes = int(v.get("statistics", {}).get("likeCount", 0))
                    print(f"       • [{status.upper()}] {v_title[:65]}...")
                    print(f"         ID: {vid} | Views: {views} | Likes: {likes} | Link: https://youtu.be/{vid}")
            else:
                print("    (Chưa có video nào trên kênh)")

        except Exception as e:
            print(f"    ❌ Lỗi kết nối kênh {ch_id}: {e}")

    print(f"\n{'='*75}")
    print("🏁 KẾT THÚC BÁO CÁO")
    print(f"{'='*75}\n")

if __name__ == "__main__":
    report_all()
