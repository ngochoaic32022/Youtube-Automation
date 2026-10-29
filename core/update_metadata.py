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

token_file = "d:/KENH GEHIHI/config/tokens/token_channel_1.json"
creds = Credentials.from_authorized_user_file(token_file, SCOPES)
youtube = build("youtube", "v3", credentials=creds)

updates = [
    {
        "id": "ENs4lnEr5Lg",
        "title": "Âm Thanh 5.000KM Dưới Đáy Biển: Quân Đội Mỹ Đã Giấu Thứ Gì? 😱 #shorts",
        "tags": [
            "the bloop", "âm thanh the bloop", "quái vật biển", "bí ẩn đại dương",
            "thủy quái", "quân đội mỹ", "khoa học bí ẩn", "khám phá", "kiến thức thú vị",
            "sự thật thú vị", "shorts", "youtube shorts"
        ],
        "highlight": "Năm 1997, hệ thống cảm biến âm thanh dưới đáy Thái Bình Dương bỗng ghi lại âm thanh The Bloop bí ẩn vang xa 5.000km, lớn hơn cả tiếng cá voi xanh!"
    },
    {
        "id": "GQ_yQoLgjj4",
        "title": "Cơ Thể Bị Kéo Giãn Như Thế Nào Khi Rơi Vào HỐ ĐEN? 😱 (Rùng Mình) #shorts",
        "tags": [
            "hố đen vũ trụ", "black hole", "khoa học vũ trụ", "chân trời sự kiện",
            "vật lý thiên văn", "khám phá vũ trụ", "kéo giãn mì ống", "bí ẩn vũ trụ", "shorts"
        ],
        "highlight": "Điều gì sẽ xảy ra nếu bạn không may bị hút vào một hố đen vũ trụ? Hiện tượng Spaghettification (mì ống hoá) sẽ bẻ cong cơ thể và thời gian như thế nào?"
    },
    {
        "id": "HypEjaTo3KY",
        "title": "Tại Sao Bước Vào Khu Rừng Này, Kim La Bàn Đều Bị 'ĐIÊN LOẠN'? 🧭 #shorts",
        "tags": [
            "rừng aokigahara", "núi phú sĩ", "bí ẩn nhật bản", "khoa học giải mã",
            "từ trường trái đất", "la bàn", "khám phá bí ẩn", "shorts"
        ],
        "highlight": "Nằm ngay dưới chân núi Phú Sĩ là khu rừng Aokigahara kỳ bí, nơi kim la bàn quay cuồng mất kiểm soát. Sự thật đằng sau là hiện tượng vật lý hay lời nguyền siêu nhiên?"
    }
]

for u in updates:
    vid = u["id"]
    res = youtube.videos().list(id=vid, part="snippet").execute()
    items = res.get("items", [])
    if not items:
        print(f"[-] Video ID {vid} không tìm thấy.")
        continue

    snippet = items[0]["snippet"]
    old_title = snippet["title"]
    snippet["title"] = u["title"]
    snippet["tags"] = u["tags"]

    # Cập nhật thêm dòng mô tả hook hấp dẫn
    new_desc = f"""🔥 {u['title']}

📌 {u['highlight']}

🔔 Bấm ĐĂNG KÝ KÊNH Kỳ Thú Khám Phá để đón xem video mới lúc 11:30 và 18:45 hàng ngày!

#shorts #{u['tags'][0].replace(' ', '')} #kienthuc #khampha #bian #khoahoc
"""
    snippet["description"] = new_desc

    up_res = youtube.videos().update(
        part="snippet",
        body={
            "id": vid,
            "snippet": snippet
        }
    ).execute()

    print(f"[+] CẬP NHẬT THÀNH CÔNG Video {vid}:")
    print(f"    - Tiêu đề cũ:  {old_title}")
    print(f"    - Tiêu đề mới: {up_res['snippet']['title']}")
    print(f"    - Tags: {len(up_res['snippet'].get('tags', []))} thẻ tags")
