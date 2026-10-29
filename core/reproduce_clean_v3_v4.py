import os
import sys
import subprocess
import asyncio

sys.path.insert(0, "d:/KENH GEHIHI")

from core.clean_subtitle_builder import build_perfect_subtitles
from core.video_renderer import VideoRenderer
from core.youtube_uploader import YouTubeUploader

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

TASKS = [
    {
        "id": "video_3",
        "title": "Cơ Thể Bị Kéo Giãn Như Thế Nào Khi Rơi Vào HỐ ĐEN? 😱 (Rùng Mình) #shorts",
        "publish_time_iso": "2026-10-28T04:30:00.000Z", # 11:30 VN
        "tags": [
            "hố đen vũ trụ", "black hole", "khoa học vũ trụ", "chân trời sự kiện",
            "vật lý thiên văn", "khám phá vũ trụ", "kéo giãn mì ống", "bí ẩn vũ trụ", "shorts"
        ],
        "description": """🔥 Cơ Thể Bị Kéo Giãn Như Thế Nào Khi Rơi Vào HỐ ĐEN? 😱 (Rùng Mình) #shorts

📌 Điều gì sẽ xảy ra nếu bạn không may bị hút vào một hố đen vũ trụ? Hiện tượng Spaghettification (mì ống hoá) sẽ bẻ cong cơ thể và thời gian như thế nào?

⏱️ TIMESTAMPS:
00:00 - Bị hút vào hố đen vũ trụ
00:07 - Chân trời sự kiện (Event Horizon)
00:15 - Hiện tượng Mì ống hóa (Spaghettification)
00:23 - Thời gian đóng băng vĩnh cửu
00:30 - Điểm kỳ dị sụp đổ vật lý

🔔 Bấm ĐĂNG KÝ KÊNH Kỳ Thú Khám Phá để đón xem video mới lúc 11:30 và 18:45 hàng ngày!

#shorts #hodevu_tru #blackhole #khoahoc #khampha #bian #vatly
""",
        "sentences": [
            "Nếu không may bị hút vào một hố đen vũ trụ, khoảnh khắc đầu tiên bạn thấy là một đĩa bồi tụ khí nóng hàng triệu độ sáng chói.",
            "Khi chạm tới Chân trời sự kiện, bạn chính thức vượt qua ranh giới một đi không trở lại, nơi ngay cả ánh sáng cũng bị giam cầm.",
            "Lực hấp dẫn chênh lệch giữa đầu và chân lớn tới mức kéo giãn cơ thể bạn ra như một sợi mì, hiện tượng này được khoa học gọi là Mì ống hóa.",
            "Kỳ lạ hơn, do thời gian bị bẻ cong, người đứng ngoài nhìn vào sẽ thấy bạn di chuyển chậm dần rồi đóng băng vĩnh viễn ở ranh giới.",
            "Và ở tận cùng của hố đen là Điểm kỳ dị, nơi toàn bộ các định luật vật lý của loài người hoàn toàn sụp đổ."
        ],
        "durations": [7.33, 7.33, 7.34, 7.34, 7.33],
        "total_dur": 36.67
    },
    {
        "id": "video_4",
        "title": "Tại Sao Bước Vào Khu Rừng Này, Kim La Bàn Đều Bị 'ĐIÊN LOẠN'? 🧭 #shorts",
        "publish_time_iso": "2026-10-28T11:45:00.000Z", # 18:45 VN
        "tags": [
            "rừng aokigahara", "núi phú sĩ", "bí ẩn nhật bản", "khoa học giải mã",
            "từ trường trái đất", "la bàn", "khám phá bí ẩn", "shorts"
        ],
        "description": """🔥 Tại Sao Bước Vào Khu Rừng Này, Kim La Bàn Đều Bị 'ĐIÊN LOẠN'? 🧭 #shorts

📌 Nằm ngay dưới chân núi Phú Sĩ là khu rừng Aokigahara kỳ bí, nơi kim la bàn quay cuồng mất kiểm soát. Sự thật đằng sau là hiện tượng vật lý hay lời nguyền siêu nhiên?

⏱️ TIMESTAMPS:
00:00 - Khu rừng kỳ bí dưới chân Phú Sĩ
00:07 - Hiện tượng la bàn quay cuồng
00:16 - Quặng sắt từ tính cổ đại
00:25 - Giải mã khoa học hiện tượng từ trường
00:32 - Sự tĩnh lặng rợn người

🔔 Bấm ĐĂNG KÝ KÊNH Kỳ Thú Khám Phá để đón xem video mới lúc 11:30 và 18:45 hàng ngày!

#shorts #aokigahara #nhatban #khoahoc #khampha #bian #laban
""",
        "sentences": [
            "Nằm ngay dưới chân núi Phú Sĩ hùng vĩ của Nhật Bản là khu rừng Aokigahara, nơi nổi tiếng với những lời đồn thổi về hiện tượng la bàn bị vô hiệu hóa.",
            "Khi bước sâu vào trong rừng, kim la bàn bỗng nhiên quay cuồng mất kiểm soát, khiến bất kỳ ai cũng có thể bị mất phương hướng trong tích tắc.",
            "Các nhà địa chất học đã vào cuộc và phát hiện: nền đất của khu rừng được hình thành từ dung nham núi lửa cổ đại chứa hàm lượng quặng sắt từ tính cực lớn.",
            "Chính từ trường bất thường này đã làm rối loạn từ trường của kim la bàn, hoàn toàn là một hiện tượng vật lý chứ không phải lời nguyền siêu nhiên.",
            "Ngoài ra, kết cấu đất xốp còn nuốt chửng âm thanh, tạo nên sự tĩnh lặng rợn người. Bạn có dám một mình bước vào khu rừng này không?"
        ],
        "durations": [8.12, 8.12, 8.12, 8.12, 8.12],
        "total_dur": 40.60
    }
]

def run_clean_batch():
    uploader = YouTubeUploader(channel_id="channel_1")

    for t in TASKS:
        vid_id = t["id"]
        out_dir = f"d:/KENH GEHIHI/outputs/{vid_id}"
        print("\n" + "=" * 65)
        print(f"[*] ĐANG TỐI ƯU HÓA HOÀN TOÀN: {vid_id} -> {t['title']}")
        print("=" * 65)

        # 1. Tạo phụ đề sạch 100%
        clean_ass = os.path.join(out_dir, "subtitles_clean.ass")
        scenes = [{"sentence": s} for s in t["sentences"]]
        build_perfect_subtitles(scenes, t["durations"], clean_ass, is_shorts=True)

        # 2. Render Video điện ảnh
        image_paths = [f"{out_dir}/scene_{i+1}.jpg" for i in range(5)]
        voice_audio = f"{out_dir}/voice.mp3"
        final_video_clean = f"{out_dir}/final_video_clean.mp4"

        renderer = VideoRenderer(width=1080, height=1920, fps=30)
        print(f"[*] Đang render {final_video_clean}...")
        renderer.render(
            image_paths=image_paths,
            voice_audio_path=voice_audio,
            output_video_path=final_video_clean,
            subtitle_path=clean_ass,
            bg_music_path="d:/KENH GEHIHI/assets/music/deep_ocean_drone.mp3",
            music_volume=0.18
        )
        print(f"[+] Render xong: {final_video_clean}")

        # 3. Upload và Lên lịch phát sóng
        print(f"[*] Đang upload lên YouTube và lên lịch phát lúc: {t['publish_time_iso']}...")
        new_yt_id = uploader.upload_video(
            video_file_path=final_video_clean,
            title=t["title"],
            description=t["description"],
            tags=t["tags"],
            category_id="27",
            publish_at_iso=t["publish_time_iso"]
        )
        print(f"[+] ĐÃ TỐI ƯU XONG {vid_id}! YouTube Link: https://youtu.be/{new_yt_id}")

if __name__ == "__main__":
    run_clean_batch()
