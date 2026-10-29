import os
import sys

sys.path.insert(0, "d:/KENH GEHIHI")

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

SCOPES = [
    "https://www.googleapis.com/auth/youtube",
    "https://www.googleapis.com/auth/youtube.force-ssl",
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/youtube.readonly"
]
TOKEN_FILE = "d:/KENH GEHIHI/config/tokens/token_channel_2.json"

def get_service():
    creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    return build("youtube", "v3", credentials=creds)

def optimize_videos():
    youtube = get_service()

    # Optimized metadata for Video 1 (FVjOfcIBzp0)
    v1_id = "FVjOfcIBzp0"
    v1_title = "Traditional Christmas Carols from the Golden Era 🔔 Cozy Holiday Music (Silent Night, Joy to the World)"
    v1_desc = """🎄 Step into the warm, timeless nostalgia of Traditional Christmas Carols from the Golden Era. 

Featuring peaceful choral harmonies and acoustic warmth, this collection brings the true spirit of Christmas into your home, perfect for relaxing by the fireplace, holiday dinners, and peaceful winter evenings.

🔔 FEATURED CLASSIC CAROLS:
- Silent Night
- Joy to the World
- O Holy Night
- Hark! The Herald Angels Sing
- O Little Town of Bethlehem
- The First Noel

✨ If you love vintage holiday music, please LIKE, SUBSCRIBE, and turn on notifications for more timeless Christmas classics throughout this festive season!

#vintagechristmas #christmascarols #traditionalchristmas #holidaymusic #silentnight #cozychristmas #peacefulchristmas
"""
    v1_tags = [
        "traditional christmas carols", "classic christmas carols", "vintage christmas music",
        "silent night", "o holy night", "joy to the world", "peaceful christmas music",
        "cozy christmas ambience", "golden era christmas", "old fashioned christmas",
        "christmas choir", "holiday carols", "relaxing christmas music"
    ]

    # Optimized metadata for Video 2 (1-6gOvgoQHw)
    v2_id = "1-6gOvgoQHw"
    v2_title = "Vintage Christmas Songs from a 1950s Radio 🎄 Cozy Holiday Music & Old Christmas Carols (100 Mins)"
    v2_desc = """🎄 Vintage Christmas Songs Playing from a Cozy 1950s Radio (Over 100 Minutes of Pure Holiday Nostalgia).

Gather around the warm, crackling fireplace and immerse yourself in the golden age of Christmas music. These timeless holiday classics, nostalgic carols, and gentle jazz tunes are perfect for holiday decorating, unwinding with hot cocoa, family dinners, and deep winter relaxation.

❄️ HIGHLIGHTS IN THIS 100-MINUTE PLAYLIST:
- Timeless 1940s & 1950s Golden Era holiday melodies
- Soothing classic carols and vintage acoustic arrangements
- Warm, comforting crackling fireplace ambience

🎁 Subscribe to Vintage Holiday Classics to fill your home with nostalgic holiday warmth all season long!

#vintagechristmas #1950schristmas #oldchristmasmusic #cozychristmas #holidayplaylist #classicchristmas #winterambience #fireplacemusic
"""
    v2_tags = [
        "vintage christmas songs", "1950s christmas music", "old christmas songs",
        "classic holiday music", "vintage christmas playlist", "cozy christmas music",
        "crackling fireplace christmas", "old fashioned christmas carols", "1940s christmas",
        "christmas jazz vintage", "silent night vintage", "white christmas style",
        "peaceful holiday ambience", "relaxing christmas music", "traditional christmas songs"
    ]

    updates = [
        {"id": v1_id, "title": v1_title, "desc": v1_desc, "tags": v1_tags, "cat": "10"},
        {"id": v2_id, "title": v2_title, "desc": v2_desc, "tags": v2_tags, "cat": "10"}
    ]

    print("=" * 65)
    print("[*] BẮT ĐẦU TỰ ĐỘNG TỐI ƯU HÓA METADATA CHO CÁC VIDEO KÊNH 2")
    print("=" * 65)

    for up in updates:
        # Fetch current snippet to keep categoryId
        curr = youtube.videos().list(part="snippet", id=up["id"]).execute()
        if not curr.get("items"):
            print(f"[-] Không tìm thấy video {up['id']}")
            continue
        cat_id = curr["items"][0]["snippet"].get("categoryId", "10") # 10 is Music

        body = {
            "id": up["id"],
            "snippet": {
                "title": up["title"][:100],
                "description": up["desc"][:5000],
                "tags": up["tags"],
                "categoryId": cat_id
            }
        }
        res = youtube.videos().update(part="snippet", body=body).execute()
        print(f"[+] ĐÃ TỐI ƯU THÀNH CÔNG VIDEO [{up['id']}]:")
        print(f"    Tiêu đề mới: {res['snippet']['title']}")
        print(f"    Số tags: {len(res['snippet'].get('tags', []))} tags")
        print("-" * 65)

    print("\n[SUCCESS] TOÀN BỘ VIDEO TRÊN KÊNH 2 ĐÃ ĐƯỢC TỐI ƯU SEO VÀ CTR!")

if __name__ == "__main__":
    optimize_videos()
