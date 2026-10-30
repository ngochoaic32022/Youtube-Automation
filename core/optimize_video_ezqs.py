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

from core.proxy_manager import get_proxy_youtube_client

def update_metadata():
    print("=" * 70)
    print("🚀 BẮT ĐẦU CẬP NHẬT TỐI ƯU HÓA METADATA CHO VIDEO eZqsNul9qgM (KÊNH 2)")
    print("=" * 70)

    youtube = get_proxy_youtube_client("channel_2")
    vid = "eZqsNul9qgM"

    new_title = "Vintage Christmas Songs from a Cozy 1950s Morning ☕ Classic Holiday Music & Old Christmas Carols"
    
    new_desc = """Start your morning wrapped in the warm, nostalgic glow of timeless 1950s holiday classics ☕️🎄 These gentle, uplifting vintage Christmas songs bring sweet memories, cozy comfort, and peaceful holiday energy to your home.

Whether you're sipping morning coffee, decorating the Christmas tree, baking holiday treats, or simply looking out at the winter snow by the fireplace, this collection is crafted to make your day truly merry and bright. ✨

🔔 Subscribe to Vintage Holiday Classics to fill your season with timeless memories!
💬 What is your absolute favorite classic Christmas carol? Tell us in the comments below! 👇

━━━━━━━━━━━━━━━━━━━━━━━━━━
🎄 TRACKLIST / CHAPTERS:
00:00 - Holly Jolly Christmas
01:59 - Frosty The Snowman
04:53 - Let It Snow!
07:50 - Winter Wonderland
09:16 - Santa Claus Is Coming to Town
11:29 - Deck The Hall
13:09 - Deck The Hall (Joyful Reprise)
14:49 - It's the Most Wonderful Time of the Year
17:34 - Let It Snow! (Festive Encore)
20:32 - Santa Claus Is Coming to Town (Holiday Cheer)
22:44 - Ding Dong Merrily on High (Joyful Acoustic Bells)
25:24 - Angels We Have Heard on High (Cozy Piano Instrumental)
28:23 - Holly Jolly Christmas (Reprise)
30:22 - Joyful Christmas Interlude (Mini Acoustic)
31:37 - It's the Most Wonderful Time of the Year (Encore)
34:22 - It's Beginning To Look A Lot Like Christmas
37:38 - I Wish You A Merry Christmas
39:01 - God Rest Ye Merry Gentlemen (Vintage Holiday Jazz)
41:48 - Winter Wonderland (Reprise)
43:15 - Frosty The Snowman (Holiday Groove)
46:09 - Ding Dong Merrily on High (Joyful Acoustic Bells)
48:49 - I Wish You A Merry Christmas (Festive Chimes)
50:11 - It's Beginning To Look A Lot Like Christmas (Grand Finale)
━━━━━━━━━━━━━━━━━━━━━━━━━━

❄️ Total Duration: 53:27
🎧 Best enjoyed with a warm cup of coffee or hot chocolate.

#VintageChristmasSongs #1950sChristmas #ClassicHolidayMusic #CozyChristmas #OldChristmasSongs #HolidayPlaylist #MorningCoffee"""

    new_tags = [
        "vintage christmas songs",
        "1950s christmas music",
        "old christmas songs",
        "classic christmas music",
        "classic holiday music",
        "cozy christmas morning",
        "peaceful holiday ambience",
        "traditional christmas songs",
        "christmas songs playlist",
        "classic holiday songs",
        "vintage holiday classics",
        "relaxing christmas music",
        "holiday morning coffee",
        "christmas fireplace with music",
        "old fashioned christmas"
    ]

    body = {
        "id": vid,
        "snippet": {
            "title": new_title[:100],
            "description": new_desc[:5000],
            "tags": new_tags,
            "categoryId": "10",
            "defaultLanguage": "en"
        }
    }

    print(f"[*] Đang gửi request update metadata cho video: {vid}...")
    res = youtube.videos().update(part="snippet", body=body).execute()

    print("\n" + "=" * 70)
    print("🎉 CẬP NHẬT METADATA THÀNH CÔNG 100%!")
    print("=" * 70)
    print(f"📌 Tiêu đề mới ({len(res['snippet']['title'])} ký tự):")
    print(f"   -> {res['snippet']['title']}")
    print(f"🏷️ Danh sách Tags ({len(res['snippet'].get('tags', []))} tags):")
    print(f"   -> {', '.join(res['snippet'].get('tags', []))}")
    print(f"🔗 Link xem: https://youtu.be/{vid}")
    print("=" * 70)

if __name__ == "__main__":
    update_metadata()
