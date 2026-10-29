import sys
from datetime import datetime
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

SCOPES = [
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/youtube.readonly"
]
TOKEN_FILE = "d:/KENH GEHIHI/config/tokens/token_channel_1.json"

class DailyReporter:
    def __init__(self, token_path=TOKEN_FILE):
        self.creds = Credentials.from_authorized_user_file(token_path, SCOPES)
        self.youtube = build("youtube", "v3", credentials=self.creds)

    def get_channel_stats(self):
        resp = self.youtube.channels().list(part="snippet,statistics", mine=True).execute()
        if not resp.get("items"):
            return None
        item = resp["items"][0]
        stats = item["statistics"]
        snippet = item["snippet"]
        return {
            "title": snippet["title"],
            "customUrl": snippet.get("customUrl", ""),
            "subscribers": int(stats.get("subscriberCount", 0)),
            "views": int(stats.get("viewCount", 0)),
            "videos": int(stats.get("videoCount", 0)),
            "time": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        }

    def get_latest_videos(self, max_results=5):
        # List latest uploaded videos
        resp = self.youtube.search().list(
            part="snippet",
            forMine=True,
            type="video",
            order="date",
            maxResults=max_results
        ).execute()

        video_ids = [item["id"]["videoId"] for item in resp.get("items", [])]
        if not video_ids:
            return []

        stats_resp = self.youtube.videos().list(
            part="snippet,statistics",
            id=",".join(video_ids)
        ).execute()

        videos = []
        for v in stats_resp.get("items", []):
            st = v["statistics"]
            sn = v["snippet"]
            videos.append({
                "id": v["id"],
                "title": sn["title"],
                "publishedAt": sn["publishedAt"],
                "views": int(st.get("viewCount", 0)),
                "likes": int(st.get("likeCount", 0)),
                "comments": int(st.get("commentCount", 0))
            })
        return videos

    def generate_report_text(self):
        channel = self.get_channel_stats()
        if not channel:
            return "Không lấy được thông tin kênh."

        videos = self.get_latest_videos(5)

        report = f"""📊 [BÁO CÁO KÊNH HÀNG NGÀY - {channel['title']}]
⏰ Cập nhật lúc: {channel['time']}
--------------------------------------------------
📈 CHỈ SỐ TỔNG QUAN:
- Tổng số Người đăng ký (Subscribers): {channel['subscribers']:,}
- Tổng số Lượt xem (Total Views):     {channel['views']:,}
- Tổng số Video đã đăng:             {channel['videos']}

🎬 HIỆU SUẤT CÁC VIDEO GẦN NHẤT:
"""
        for i, v in enumerate(videos, 1):
            report += f"{i}. {v['title'][:45]}...\n   👉 Views: {v['views']:,} | Likes: {v['likes']} | https://youtube.com/shorts/{v['id']}\n"

        report += "--------------------------------------------------\n"
        return report

if __name__ == "__main__":
    rep = DailyReporter()
    print(rep.generate_report_text())
