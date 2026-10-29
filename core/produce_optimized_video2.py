import os
import sys
import subprocess
import asyncio
import edge_tts

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

async def generate_sentence_audio(text: str, out_path: str, voice: str = "vi-VN-NamMinhNeural", rate: str = "+3%"):
    comm = edge_tts.Communicate(text, voice, rate=rate)
    await comm.save(out_path)
    
    cmd = [
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        out_path
    ]
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return float(res.stdout.strip())

async def produce():
    out_dir = "d:/KENH GEHIHI/outputs/video_2"
    temp_dir = os.path.join(out_dir, "temp_clean")
    os.makedirs(temp_dir, exist_ok=True)

    scenes = [
        {
            "sentence": "Năm 1997, hệ thống cảm biến của quân đội Mỹ dưới đáy Thái Bình Dương bỗng bắt được một âm thanh bí ẩn cực lớn mang tên The Bloop.",
            "image": "d:/KENH GEHIHI/outputs/video_2/scene_1.jpg"
        },
        {
            "sentence": "Âm thanh này vang xa tới hơn 5.000 cây số, vượt xa tiếng kêu của cá voi xanh - sinh vật lớn nhất hành tinh.",
            "image": "d:/KENH GEHIHI/outputs/video_2/scene_2.jpg"
        },
        {
            "sentence": "Thời điểm đó, rất nhiều nhà khoa học rùng mình suy đoán đây có thể là tiếng gầm của một loài thủy quái khổng lồ chưa từng được biết đến.",
            "image": "d:/KENH GEHIHI/outputs/video_2/scene_3.jpg"
        },
        {
            "sentence": "Mãi tới năm 2002, cơ quan khí quyển đại dương Mỹ mới đưa ra lời giải thích: đó là một vụ nứt gãy kinh hoàng của tảng băng trôi khổng lồ ở Nam Cực.",
            "image": "d:/KENH GEHIHI/outputs/video_2/scene_4.jpg"
        },
        {
            "sentence": "Nhưng liệu một tảng băng có thể phát ra âm thanh kỳ dị đến vậy, hay dưới đáy đại dương vẫn đang che giấu một bí mật kinh hoàng?",
            "image": "d:/KENH GEHIHI/outputs/video_2/scene_5.jpg"
        }
    ]

    print("\n" + "=" * 65)
    print("[*] SẢN XUẤT LẠI VIDEO 2 CHUẨN TRIỆU VIEW (SUBTITLE SẠCH 100%)")
    print("=" * 65)

    # 1. Tạo audio chuẩn từng câu và đo duration chính xác
    sentence_audios = []
    sentence_durations = []
    for idx, sc in enumerate(scenes):
        s_path = os.path.join(temp_dir, f"s_{idx+1}.mp3")
        dur = await generate_sentence_audio(sc["sentence"], s_path)
        sentence_audios.append(s_path)
        sentence_durations.append(dur)
        print(f"  + Câu {idx+1} ({dur:.2f}s): {sc['sentence'][:50]}...")

    # Ghép toàn bộ audio câu thành 1 master voice
    concat_audio_txt = os.path.join(temp_dir, "audio_concat.txt")
    with open(concat_audio_txt, "w", encoding="utf-8") as f:
        for sa in sentence_audios:
            clean_p = os.path.abspath(sa).replace("\\", "/")
            f.write(f"file '{clean_p}'\n")

    master_voice = os.path.join(out_dir, "voice_clean.mp3")
    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", concat_audio_txt,
        "-c", "copy", master_voice
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    total_voice_dur = sum(sentence_durations)
    print(f"\n[+] Tổng thời lượng Voice: {total_voice_dur:.2f}s")

    # 2. Xây dựng phụ đề ASS chuẩn 100% không lỗi chính tả
    clean_ass = os.path.join(out_dir, "subtitles_clean.ass")
    build_perfect_subtitles(scenes, sentence_durations, clean_ass, is_shorts=True)

    # 3. Render video chất lượng cao
    print("\n[*] Đang render video điện ảnh chuẩn 1080x1920...")
    image_paths = [sc["image"] for sc in scenes]
    final_clean_video = os.path.join(out_dir, "final_video_2_clean.mp4")
    
    renderer = VideoRenderer(width=1080, height=1920, fps=30)
    renderer.render(
        image_paths=image_paths,
        voice_audio_path=master_voice,
        output_video_path=final_clean_video,
        subtitle_path=clean_ass,
        bg_music_path="d:/KENH GEHIHI/assets/music/deep_ocean_drone.mp3",
        music_volume=0.18
    )
    print(f"\n[+] VIDEO THÀNH PHẨM SẠCH 100%: {final_clean_video}")

    # 4. Upload & Lên lịch phát sóng 18:45 tối nay (27/10/2026)
    title = "Âm Thanh 5.000KM Dưới Đáy Biển: Quân Đội Mỹ Đã Giấu Thứ Gì? 😱 #shorts"
    description = f"""🔥 {title}

📌 Năm 1997, hệ thống cảm biến âm thanh dưới đáy Thái Bình Dương bỗng ghi lại âm thanh The Bloop bí ẩn vang xa 5.000km, lớn hơn cả tiếng cá voi xanh!

⏱️ TIMESTAMPS:
00:00 - Âm thanh The Bloop bí ẩn 5.000km
00:07 - Lớn hơn cá voi xanh
00:15 - Nghi vấn siêu thủy quái đáy biển
00:23 - Lời giải thích của NOAA
00:30 - Bí mật kinh hoàng chưa có lời giải?

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
    print(f"\n[*] Đang upload video mới và LÊN LỊCH PHÁT SÓNG LÚC 18:45 TỐI NAY...")
    new_vid_id = uploader.upload_video(
        video_file_path=final_clean_video,
        title=title,
        description=description,
        tags=tags,
        category_id="27",
        publish_at_iso=publish_time_iso
    )
    print(f"\n[HOÀN TẤT] Video 2 chuẩn Triệu View đã sẵn sàng: https://youtu.be/{new_vid_id}")

if __name__ == "__main__":
    asyncio.run(produce())
