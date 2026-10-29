import os
import sys

# Add project root to sys.path
sys.path.insert(0, "d:/KENH GEHIHI")

import asyncio
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

async def main():
    out_dir = "d:/KENH GEHIHI/outputs/video_2"
    topic = "Bí Mật Âm Thanh Quái Vật The Bloop Dưới Đáy Biển Sâu"
    
    script_sentences = [
        "Năm 1997, hệ thống cảm biến âm thanh của quân đội Mỹ dưới đáy Thái Bình Dương bỗng ghi lại một âm thanh bí ẩn cực lớn có tên là The Bloop.",
        "Âm thanh này vang xa tới hơn 5.000 km, lớn hơn nhiều lần tiếng kêu của cá voi xanh - sinh vật lớn nhất hành tinh.",
        "Thời điểm đó, rất nhiều nhà khoa học rùng mình suy đoán đây có thể là tiếng gầm của một loài thủy quái khổng lồ chưa từng được biết đến.",
        "Mãi tới năm 2002, cơ quan khí quyển đại dương Mỹ mới đưa ra lời giải thích: đó là một vụ nứt gãy kinh hoàng của tảng băng trôi khổng lồ ở Nam Cực.",
        "Nhưng liệu đó có phải là toàn bộ sự thật, hay đáy biển sâu còn thứ gì đó đáng sợ hơn? Bạn nghĩ sao, hãy để lại bình luận nhé!"
    ]
    full_script = " ".join(script_sentences)

    print(f"\n[*] BẮT ĐẦU SẢN XUẤT VIDEO 2: {topic}")

    # 1. Voiceover
    tts = TTSEngine(voice="vi-VN-NamMinhNeural")
    voice_path = f"{out_dir}/voice.mp3"
    raw_srt = f"{out_dir}/voice.srt"
    dur = await tts.generate_speech(full_script, voice_path, raw_srt)
    print(f"  -> Voiceover: {dur:.2f}s")

    # 2. Dynamic Karaoke Subtitles (Montserrat Black)
    sub_gen = SubtitleGenerator(model_size="tiny", device="cpu")
    ass_path = f"{out_dir}/subtitles.ass"
    sub_gen.generate_srt_and_ass(voice_path, raw_srt, ass_path, format_type="shorts")
    print(f"  -> Dynamic ASS Subtitles created.")

    # 3. Video Rendering
    image_paths = [f"{out_dir}/scene_{i+1}.jpg" for i in range(5)]
    final_video = f"{out_dir}/final_video_2.mp4"
    renderer = VideoRenderer(width=1080, height=1920, fps=30)
    renderer.render(
        image_paths=image_paths,
        voice_audio_path=voice_path,
        output_video_path=final_video,
        subtitle_path=ass_path,
        bg_music_path="d:/KENH GEHIHI/assets/music/deep_ocean_drone.mp3",
        music_volume=0.18
    )
    print(f"  -> Video rendered: {final_video}")

    # 4. SEO
    seo = SEOPackager.package(
        topic="Âm Thanh Bí Ẩn The Bloop",
        script_summary=full_script[:200],
        niche="Khoa học, Bí ẩn đại dương",
        language="vi",
        is_shorts=True
    )
    title = "Âm Thanh Quái Vật 'The Bloop' Dưới Đáy Biển Khiến Cả Thế Giới Rùng Mình! 😱 #shorts"
    description = f"""🔥 {title}

📌 Năm 1997, hệ thống cảm biến âm thanh dưới đáy Thái Bình Dương bỗng ghi lại âm thanh The Bloop bí ẩn vang xa 5.000km, lớn hơn cả tiếng cá voi xanh!

⏱️ TIMESTAMPS:
00:00 - Âm thanh The Bloop bí ẩn
00:07 - Tiếng vang 5.000km
00:15 - Nghi vấn quái vật biển sâu
00:23 - Lời giải thích của NOAA
00:30 - Lời kết & Đăng ký kênh

🔔 Bấm ĐĂNG KÝ KÊNH Kỳ Thú Khám Phá để đón xem video mới lúc 11:30 và 18:45 hàng ngày!

#shorts #thebloop #kienthuc #khampha #bian #suthat #khoahoc #ocean
"""
    tags = [
        "the bloop", "âm thanh the bloop", "quái vật biển", "bí ẩn đại dương",
        "thủy quái", "khoa học kỳ thú", "khám phá", "kiến thức thú vị",
        "sự thật thú vị", "shorts", "youtube shorts"
    ]

    # 5. Upload & Schedule for 18:45 VN time (11:45 UTC) today (2026-10-27)
    publish_time_iso = "2026-10-27T11:45:00.000Z"
    uploader = YouTubeUploader(channel_id="channel_1")
    print(f"\n[*] Đang upload và LÊN LỊCH TỰ ĐỘNG phát sóng lúc 18:45 hôm nay...")
    vid_id = uploader.upload_video(
        video_file_path=final_video,
        title=title,
        description=description,
        tags=tags,
        category_id="28",
        privacy_status="private",
        publish_at_iso=publish_time_iso
    )
    print(f"[SUCCESS] Đã lên lịch phát sóng thành công! Video ID: {vid_id}")
    print(f"Video sẽ tự động công khai vào lúc 18:45 hôm nay!")

if __name__ == "__main__":
    asyncio.run(main())
