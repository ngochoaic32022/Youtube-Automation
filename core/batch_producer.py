import os
import sys

sys.path.insert(0, "d:/KENH GEHIHI")

import json
import asyncio
import urllib.request
from core.tts_engine import TTSEngine
from core.subtitle_gen import SubtitleGenerator
from core.video_renderer import VideoRenderer
from core.seo_packager import SEOPackager
from core.youtube_uploader import YouTubeUploader

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Master plan of 10 high-value, tightly-matched educational videos
VIDEO_CATALOG = [
    {
        "id": "video_3",
        "topic": "Điều Gì Sẽ Xảy Ra Nếu Bạn Rơi Vào Hố Đen Vũ Trụ?",
        "publish_iso": "2026-10-28T04:30:00.000Z", # 11:30 AM VN time on 28/10
        "publish_display": "11:30 ngày 28/10/2026",
        "scenes": [
            {
                "sentence": "Nếu không may bị hút vào một hố đen vũ trụ, khoảnh khắc đầu tiên bạn thấy là một đĩa bồi tụ khí nóng hàng triệu độ sáng chói.",
                "url": "https://images-assets.nasa.gov/image/PIA23687/PIA23687~medium.jpg", # NASA black hole accretion disk
                "desc": "Đĩa bồi tụ khí nóng sáng rực quanh hố đen (NASA Black Hole)"
            },
            {
                "sentence": "Khi chạm tới Chân trời sự kiện, bạn chính thức vượt qua ranh giới một đi không trở lại, nơi ngay cả ánh sáng cũng bị giam cầm.",
                "url": "https://images-assets.nasa.gov/image/GSFC_20171208_Archive_e000492/GSFC_20171208_Archive_e000492~medium.jpg",
                "desc": "Chân trời sự kiện (Event Horizon) nuốt chửng ánh sáng"
            },
            {
                "sentence": "Lực hấp dẫn chênh lệch giữa đầu và chân lớn tới mức kéo giãn cơ thể bạn ra như một sợi mì, hiện tượng này được khoa học gọi là Mì ống hóa.",
                "url": "https://images.unsplash.com/photo-1506703719100-a0f3a48c0f86?w=1080&q=80",
                "desc": "Không gian bị bẻ cong cực hạn và hiện tượng kéo giãn Spaghettification"
            },
            {
                "sentence": "Kỳ lạ hơn, do thời gian bị bẻ cong, người đứng ngoài nhìn vào sẽ thấy bạn di chuyển chậm dần rồi đóng băng vĩnh viễn ở ranh giới.",
                "url": "https://images.unsplash.com/photo-1501139083538-0139583c060f?w=1080&q=80",
                "desc": "Hiện tượng giãn nở thời gian (Time Dilation) và đồng hồ vô tận"
            },
            {
                "sentence": "Và ở tận cùng của hố đen là Điểm kỳ dị, nơi toàn bộ các định luật vật lý của loài người hoàn toàn sụp đổ.",
                "url": "https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=1080&q=80",
                "desc": "Điểm kỳ dị (Singularity) - nơi tri thức vũ trụ chạm giới hạn"
            }
        ],
        "seo_title": "Điều Gì Xảy Ra Nếu Bạn Bị Hút Vào HỐ ĐEN Vũ Trụ? 😱 #shorts",
        "tags": ["hố đen vũ trụ", "black hole", "khoa học vũ trụ", "chân trời sự kiện", "vật lý thiên văn", "khám phá vũ trụ", "shorts"]
    },
    {
        "id": "video_4",
        "topic": "Bí Mật Hiện Tượng La Bàn Mất Phương Hướng Tại Rừng Aokigahara",
        "publish_iso": "2026-10-28T11:45:00.000Z", # 18:45 PM VN time on 28/10
        "publish_display": "18:45 ngày 28/10/2026",
        "scenes": [
            {
                "sentence": "Nằm ngay dưới chân núi Phú Sĩ hùng vĩ của Nhật Bản là khu rừng Aokigahara, nơi nổi tiếng với những lời đồn thổi về hiện tượng la bàn bị vô hiệu hóa.",
                "url": "https://images.unsplash.com/photo-1493976040374-85c8e12f0c0e?w=1080&q=80", # Mount Fuji and misty trees
                "desc": "Rừng Aokigahara dưới chân núi Phú Sĩ Nhật Bản"
            },
            {
                "sentence": "Khi bước sâu vào trong rừng, kim la bàn bỗng nhiên quay cuồng mất kiểm soát, khiến bất kỳ ai cũng có thể bị mất phương hướng trong tích tắc.",
                "url": "https://images.unsplash.com/photo-1518709268805-4e9042af9f23?w=1080&q=80", # Compass navigation
                "desc": "Chiếc la bàn cổ quay loạn hướng giữa rừng rậm"
            },
            {
                "sentence": "Các nhà địa chất học đã vào cuộc và phát hiện: nền đất của khu rừng được hình thành từ dung nham núi lửa cổ đại chứa hàm lượng quặng sắt từ tính cực lớn.",
                "url": "https://images.unsplash.com/photo-1448375240586-882707db888b?w=1080&q=80", # Volcanic dark soil and dense roots
                "desc": "Nham thạch núi lửa cổ đại và quặng sắt từ tính tự nhiên"
            },
            {
                "sentence": "Chính từ trường bất thường này đã làm rối loạn từ trường của kim la bàn, hoàn toàn là một hiện tượng vật lý chứ không phải lời nguyền siêu nhiên.",
                "url": "https://images.unsplash.com/photo-1542273917363-3b1817f69a2d?w=1080&q=80", # Scientific forest canopy
                "desc": "Giải mã khoa học đằng sau từ trường bí ẩn"
            },
            {
                "sentence": "Ngoài ra, kết cấu đất xốp còn nuốt chửng âm thanh, tạo nên sự tĩnh lặng rợn người. Bạn có dám một mình bước vào khu rừng này không?",
                "url": "https://images.unsplash.com/photo-1511497584788-87676104235f?w=1080&q=80", # Deep misty silent forest
                "desc": "Sự tĩnh lặng tuyệt đối của khu rừng và lời kêu gọi tương tác"
            }
        ],
        "seo_title": "Sự Thật Khoa Học Đằng Sau LA BÀN BỊ LIỆT Ở Rừng Aokigahara! 🧭 #shorts",
        "tags": ["rừng aokigahara", "núi phú sĩ", "bí ẩn nhật bản", "khoa học giải mã", "từ trường trái đất", "la bàn", "khám phá", "shorts"]
    }
]

async def produce_single_video(item: dict, uploader: YouTubeUploader):
    vid_id = item["id"]
    out_dir = f"d:/KENH GEHIHI/outputs/{vid_id}"
    os.makedirs(out_dir, exist_ok=True)

    print("\n" + "=" * 65)
    print(f"[*] SẢN XUẤT CHUẨN GIÁ TRỊ: {item['topic']}")
    print(f"[*] Lịch phát sóng: {item['publish_display']}")
    print("=" * 65)

    # 1. Download verified matching visual assets
    image_paths = []
    for idx, sc in enumerate(item["scenes"], 1):
        img_path = f"{out_dir}/scene_{idx}.jpg"
        if not os.path.exists(img_path):
            print(f"  [+] Tải tư liệu khớp cảnh {idx}: {sc['desc'][:40]}...")
            req = urllib.request.Request(sc["url"], headers={"User-Agent": "Mozilla/5.0"})
            try:
                with urllib.request.urlopen(req, timeout=12) as resp:
                    with open(img_path, "wb") as f:
                        f.write(resp.read())
            except Exception as e:
                print(f"      Lỗi tải ảnh {idx}: {e}, dùng ảnh fallback...")
                import shutil
                if idx > 1 and os.path.exists(f"{out_dir}/scene_{idx-1}.jpg"):
                    shutil.copy2(f"{out_dir}/scene_{idx-1}.jpg", img_path)
                elif os.path.exists(f"{out_dir}/scene_1.jpg"):
                    shutil.copy2(f"{out_dir}/scene_1.jpg", img_path)
        image_paths.append(img_path)

    # 2. Voiceover with natural pacing
    full_script = " ".join([sc["sentence"] for sc in item["scenes"]])
    tts = TTSEngine(voice="vi-VN-NamMinhNeural")
    voice_audio = f"{out_dir}/voice.mp3"
    raw_srt = f"{out_dir}/voice.srt"
    dur = await tts.generate_speech(full_script, voice_audio, raw_srt)
    print(f"  [+] Voiceover AI hoàn tất: {dur:.2f}s")

    # 3. Typography Subtitles (Montserrat Black, Word-by-word highlight)
    sub_gen = SubtitleGenerator(model_size="tiny", device="cpu")
    ass_path = f"{out_dir}/subtitles.ass"
    sub_gen.generate_srt_and_ass(voice_audio, raw_srt, ass_path, format_type="shorts")
    print(f"  [+] Phụ đề chữ to Montserrat Black đồng bộ xong.")

    # 4. Render Video with Ken Burns motion & audio ducking
    final_video = f"{out_dir}/final_video.mp4"
    renderer = VideoRenderer(width=1080, height=1920, fps=30)
    renderer.render(
        image_paths=image_paths,
        voice_audio_path=voice_audio,
        output_video_path=final_video,
        subtitle_path=ass_path,
        bg_music_path="d:/KENH GEHIHI/assets/music/deep_ocean_drone.mp3",
        music_volume=0.16
    )
    print(f"  [+] Video hoàn thành chất lượng cao: {final_video}")

    # 5. YouTube Scheduled Upload
    desc = f"""🔥 {item['seo_title']}

📌 {full_script[:220]}...

⏱️ NỘI DUNG CHÍNH:
00:00 - Bí mật khởi đầu
00:10 - Bản chất sự thật
00:20 - Hiện tượng khoa học giải mã
00:30 - Kết luận & Lời khuyên

🔔 Đăng ký kênh Kỳ Thú Khám Phá để mở mang kiến thức mỗi ngày vào 11:30 và 18:45!

{' '.join(['#' + t.replace(' ', '') for t in item['tags'][:6]])}
"""
    print(f"  [+] Đang tải lên và hẹn giờ phát sóng lúc {item['publish_display']}...")
    yt_vid_id = uploader.upload_video(
        video_file_path=final_video,
        title=item["seo_title"],
        description=desc,
        tags=item["tags"],
        category_id="28",
        privacy_status="private",
        publish_at_iso=item["publish_iso"]
    )
    print(f"  [SUCCESS] Đã hẹn giờ phát sóng thành công! Video ID: {yt_vid_id}")
    return yt_vid_id

async def main():
    uploader = YouTubeUploader(channel_id="channel_1")
    for item in VIDEO_CATALOG:
        await produce_single_video(item, uploader)

if __name__ == "__main__":
    asyncio.run(main())
