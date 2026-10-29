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

class AudienceFeedbackAuditor:
    def __init__(self, token_path=TOKEN_FILE):
        self.creds = Credentials.from_authorized_user_file(token_path, SCOPES)
        self.youtube = build("youtube", "v3", credentials=self.creds)

    def audit_comments(self, max_videos=10):
        # 1. Fetch recent uploaded videos
        resp = self.youtube.search().list(
            part="snippet",
            forMine=True,
            type="video",
            order="date",
            maxResults=max_videos
        ).execute()

        video_ids = [item["id"]["videoId"] for item in resp.get("items", [])]
        feedback_report = []

        for vid in video_ids:
            # Fetch video details
            v_meta = self.youtube.videos().list(part="snippet,statistics", id=vid).execute()
            if not v_meta.get("items"):
                continue
            v_item = v_meta["items"][0]
            title = v_item["snippet"]["title"]
            stats = v_item["statistics"]
            views = int(stats.get("viewCount", 0))
            likes = int(stats.get("likeCount", 0))

            # Fetch top comments
            comments = []
            try:
                c_resp = self.youtube.commentThreads().list(
                    part="snippet",
                    videoId=vid,
                    maxResults=10,
                    textFormat="plainText"
                ).execute()
                for c_item in c_resp.get("items", []):
                    top = c_item["snippet"]["topLevelComment"]["snippet"]
                    comments.append({
                        "author": top["authorDisplayName"],
                        "text": top["textDisplay"],
                        "likes": top["likeCount"]
                    })
            except Exception:
                # Comments might be disabled or empty
                pass

            feedback_report.append({
                "id": vid,
                "title": title,
                "views": views,
                "likes": likes,
                "comments": comments
            })

        return feedback_report

    def generate_feedback_summary(self):
        reports = self.audit_comments(5)
        text = "=" * 60 + "\n"
        text += "🔍 [PHÂN TÍCH BÌNH LUẬN & ĐỀ XUẤT CẢI THIỆN TỪ KHÁN GIẢ]\n"
        text += f"⏰ Thời gian quét: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n"
        text += "=" * 60 + "\n\n"

        total_comments = 0
        all_comments_text = []

        for r in reports:
            text += f"📹 Video: {r['title'][:50]}...\n"
            text += f"   📊 Lượt xem: {r['views']:,} | Lượt like: {r['likes']}\n"
            if r['comments']:
                text += f"   💬 Ý kiến khán giả ({len(r['comments'])} bình luận):\n"
                for c in r['comments']:
                    text += f"      - [{c['author']}]: \"{c['text']}\"\n"
                    all_comments_text.append(c['text'])
                    total_comments += 1
            else:
                text += "   💬 Chưa có bình luận mới.\n"
            text += "-" * 50 + "\n"

        # Insight and action recommendation
        text += "\n💡 ĐÁNH GIÁ & ĐỊNH HƯỚNG CẢI THIỆN CHO MẺ VIDEO TIẾP THEO:\n"
        if total_comments == 0:
            text += "1. Tương tác: Kênh mới đang trong giai đoạn 'Seed Testing' thu hút traffic ban đầu.\n"
            text += "2. Tối ưu: Đẩy mạnh câu hỏi gây tranh cãi/tò mò ở 5s cuối để kích thích khán giả comment.\n"
            text += "3. Giữ chân (Retention): Giữ nhịp cắt dưới 3 giây/cảnh và phụ đề karaoke màu neon để duy trì APV > 85%.\n"
        else:
            text += f"1. Đã ghi nhận {total_comments} phản hồi từ khán giả thực tế.\n"
            text += "2. Tự động gom các chủ đề được khán giả yêu cầu nhiều nhất để đưa vào kịch bản ưu tiên.\n"

        return text

if __name__ == "__main__":
    auditor = AudienceFeedbackAuditor()
    print(auditor.generate_feedback_summary())
