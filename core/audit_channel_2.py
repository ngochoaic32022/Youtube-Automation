import os
import sys
import json
from datetime import datetime

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT_DIR)

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

from core.proxy_manager import get_proxy_youtube_client

def audit():
    youtube = get_proxy_youtube_client("channel_2")
    c_res = youtube.channels().list(mine=True, part="snippet,contentDetails,statistics").execute()
    uploads_id = c_res["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]

    p_res = youtube.playlistItems().list(playlistId=uploads_id, part="snippet,contentDetails", maxResults=15).execute()
    v_ids = [p["contentDetails"]["videoId"] for p in p_res.get("items", [])]

    v_res = youtube.videos().list(id=",".join(v_ids), part="snippet,statistics,status,contentDetails").execute()
    
    print("\n" + "=" * 80)
    print("AUDIT TOÀN BỘ VIDEO KÊNH 2 (VINTAGE HOLIDAY CLASSICS)")
    print("=" * 80)

    for v in v_res.get("items", []):
        vid = v["id"]
        s = v["snippet"]
        st = v.get("statistics", {})
        status = v.get("status", {})
        cd = v.get("contentDetails", {})
        
        print(f"\n[ID: {vid}] {s['title']}")
        print(f"  • Đăng lúc: {s['publishedAt']}")
        print(f"  • Lượt xem: {st.get('viewCount', 0)} | Like: {st.get('likeCount', 0)} | Comment: {st.get('commentCount', 0)}")
        print(f"  • Thời lượng: {cd.get('duration')} | Định dạng: {cd.get('definition')} | Caption: {cd.get('caption')}")
        print(f"  • Trạng thái: {status.get('privacyStatus')} | UploadStatus: {status.get('uploadStatus')} | MadeForKids: {status.get('madeForKids')}")
        print(f"  • CategoryId: {s.get('categoryId')}")
        print(f"  • DefaultLanguage: {s.get('defaultLanguage')} | DefaultAudioLanguage: {s.get('defaultAudioLanguage')}")
        print(f"  • Tags ({len(s.get('tags', []))}): {s.get('tags', [])[:8]}")
        print(f"  • Description (100 ký tự đầu): {repr(s.get('description', '')[:100])}")

if __name__ == "__main__":
    audit()
