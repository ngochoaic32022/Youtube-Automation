import sys
import json
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

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

def check_channel(token_file):
    creds = Credentials.from_authorized_user_file(token_file, SCOPES)
    youtube = build("youtube", "v3", credentials=creds)

    res = youtube.channels().list(mine=True, part="snippet,contentDetails,statistics").execute()
    items = res.get("items", [])
    if not items:
        print("Không tìm thấy thông tin kênh.")
        return

    for item in items:
        title = item["snippet"]["title"]
        uploads_id = item["contentDetails"]["relatedPlaylists"]["uploads"]
        stats = item["statistics"]
        print(f"==================================================")
        print(f"KÊNH: {title}")
        print(f"Tổng Sub: {stats.get('subscriberCount')}")
        print(f"Tổng View: {stats.get('viewCount')}")
        print(f"Tổng Video: {stats.get('videoCount')}")
        print(f"==================================================\n")

        playlist_items = youtube.playlistItems().list(
            playlistId=uploads_id,
            part="snippet,contentDetails",
            maxResults=10
        ).execute()

        video_ids = [p["contentDetails"]["videoId"] for p in playlist_items.get("items", [])]
        if not video_ids:
            print("Chưa có video nào được đăng tải.")
            return

        v_res = youtube.videos().list(
            id=",".join(video_ids),
            part="snippet,statistics,status,contentDetails"
        ).execute()

        print(f"DANH SÁCH {len(v_res.get('items', []))} VIDEO MỚI NHẤT:")
        for v in v_res.get("items", []):
            vid = v["id"]
            v_title = v["snippet"]["title"]
            published = v["snippet"]["publishedAt"]
            v_stats = v.get("statistics", {})
            v_status = v.get("status", {})
            duration = v.get("contentDetails", {}).get("duration", "")
            print(f"--------------------------------------------------")
            print(f"Tiêu đề: {v_title}")
            print(f"Link: https://youtu.be/{vid}")
            print(f"Ngày đăng: {published}")
            print(f"Trạng thái: {v_status.get('privacyStatus')}")
            print(f"Lượt xem (Views): {v_stats.get('viewCount', 0)}")
            print(f"Lượt thích (Likes): {v_stats.get('likeCount', 0)}")
            print(f"Bình luận (Comments): {v_stats.get('commentCount', 0)}")

if __name__ == "__main__":
    token_path = "d:/KENH GEHIHI/config/tokens/token_channel_1.json"
    check_channel(token_path)
