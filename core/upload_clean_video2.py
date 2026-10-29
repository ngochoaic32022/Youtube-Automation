import sys
sys.path.insert(0, "d:/KENH GEHIHI")
from core.youtube_uploader import YouTubeUploader

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

video_path = "d:/KENH GEHIHI/outputs/video_2/final_video_2_clean.mp4"
title = "Âm Thanh 5.000KM Dưới Đáy Biển: Quân Đội Mỹ Đã Giấu Thứ Gì? 😱 #shorts"
description = """🔥 Âm Thanh 5.000KM Dưới Đáy Biển: Quân Đội Mỹ Đã Giấu Thứ Gì? 😱 #shorts

📌 Năm 1997, hệ thống cảm biến âm thanh dưới đáy Thái Bình Dương bỗng ghi lại âm thanh The Bloop bí ẩn vang xa 5.000km, lớn hơn cả tiếng cá voi xanh!

⏱️ TIMESTAMPS:
00:00 - Âm thanh The Bloop bí ẩn 5.000km
00:07 - Tiếng vang lớn hơn cá voi xanh
00:15 - Nghi vấn siêu thủy quái đáy biển
00:23 - Lời giải thích của NOAA
00:30 - Bí mật kinh hoàng dưới đáy biển sâu?

🔔 Bấm ĐĂNG KÝ KÊNH Kỳ Thú Khám Phá để đón xem video mới lúc 11:30 và 18:45 hàng ngày!

#shorts #thebloop #kienthuc #khampha #bian #suthat #khoahoc #ocean
"""
tags = [
    "the bloop", "âm thanh the bloop", "quái vật biển", "bí ẩn đại dương",
    "thủy quái", "quân đội mỹ", "khoa học bí ẩn", "khám phá", "kiến thức thú vị",
    "sự thật thú vị", "shorts", "youtube shorts"
]

publish_time_iso = "2026-10-27T11:45:00.000Z"  # 18:45 VN Time

uploader = YouTubeUploader(channel_id="channel_1")
print("[*] Đang upload video thành phẩm sạch lên YouTube...")
vid_id = uploader.upload_video(
    video_file_path=video_path,
    title=title,
    description=description,
    tags=tags,
    category_id="27",
    publish_at_iso=publish_time_iso
)
print(f"[THÀNH CÔNG] Video ID mới: {vid_id}")
print(f"URL: https://youtu.be/{vid_id}")
