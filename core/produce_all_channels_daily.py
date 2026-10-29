import os
import sys
import json
import time
import asyncio
import subprocess
import random
from datetime import datetime, timedelta, timezone

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, ROOT_DIR)

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

import edge_tts
from core.tts_engine import TTSEngine
from core.clean_subtitle_builder import build_perfect_subtitles
from core.video_renderer import VideoRenderer
from core.youtube_uploader import YouTubeUploader
from core.stock_video_fetcher import fetch_stock_video_clip

# =====================================================================
# TASK 1: CHANNEL 1 - KỲ THÚ KHÁM PHÁ (SHORTS)
# =====================================================================
async def produce_channel_1():
    print("\n" + "=" * 70)
    print("🚀 [BƯỚC 1/3] SẢN XUẤT SHORTS KÊNH 1 (KỲ THÚ KHÁM PHÁ)")
    print("=" * 70)

    out_dir = os.path.join(ROOT_DIR, "outputs", "channel_1")
    os.makedirs(out_dir, exist_ok=True)

    scenes_data = [
        {
            "sentence": "Bạn có biết, ngay lúc này, một thiên thạch khổng lồ đang lao qua không gian với vận tốc 40.000 km một giờ?",
            "keyword": "asteroid flying in space",
            "fallback": "galaxy space universe"
        },
        {
            "sentence": "Nếu nó đâm vào Trái Đất, năng lượng giải phóng sẽ tương đương với hàng triệu quả bom nguyên tử phát nổ cùng lúc.",
            "keyword": "huge explosion earth destruction",
            "fallback": "fire fiery magma explosion"
        },
        {
            "sentence": "Thế nhưng, chính lực hấp dẫn khổng lồ của Sao Mộc đã như một lá chắn vô hình, hút lệch quỹ đạo của hàng ngàn quái vật không gian này.",
            "keyword": "planet jupiter space",
            "fallback": "planets solar system"
        },
        {
            "sentence": "Nhân loại vẫn đang an toàn sống sót mỗi ngày nhờ sự che chở kỳ diệu của vũ trụ. Bấm đăng ký kênh Kỳ Thú Khám Phá để khám phá thêm nhé!",
            "keyword": "earth rotating from space",
            "fallback": "beautiful planet earth"
        }
    ]

    # 1. Generate Voice
    voice_audio = os.path.join(out_dir, "voice_ch1.mp3")
    full_script = " ".join([s["sentence"] for s in scenes_data])
    print(f"  [+] Đang tạo giọng đọc Nam Minh AI (vi-VN-NamMinhNeural)...")
    comm = edge_tts.Communicate(full_script, "vi-VN-NamMinhNeural", rate="+4%")
    await comm.save(voice_audio)

    # 2. Get Audio Duration
    renderer = VideoRenderer(width=1080, height=1920)
    tot_dur = renderer._get_audio_duration(voice_audio)
    print(f"      Thời lượng voiceover: {tot_dur:.2f}s")

    # 3. Fetch Stock Video Clips (Motion Visuals)
    clips = []
    for idx, sc in enumerate(scenes_data, 1):
        clip_path = os.path.join(out_dir, f"motion_clip_{idx}.mp4")
        if not os.path.exists(clip_path):
            print(f"  [+] Tải video stock cảnh {idx} cho từ khóa '{sc['keyword']}'...")
            ok = fetch_stock_video_clip(sc["keyword"], clip_path, orientation="portrait", fallback_keywords=[sc["fallback"], "mysterious space"])
            if not ok:
                # If download failed, use test clip or loop
                clip_path = os.path.join(ROOT_DIR, "outputs", "test_stock_short.mp4")
        if os.path.exists(clip_path):
            clips.append(clip_path)

    # 4. Generate Subtitles
    ass_path = os.path.join(out_dir, "subtitles_ch1.ass")
    sentence_durs = [tot_dur / len(scenes_data)] * len(scenes_data)
    build_perfect_subtitles(scenes_data, sentence_durs, ass_path, is_shorts=True)

    # 5. Render Final Motion Short
    final_video = os.path.join(out_dir, "short_ch1_master.mp4")
    bg_music = os.path.join(ROOT_DIR, "assets", "music", "deep_ocean_drone.mp3")
    if not os.path.exists(bg_music):
        bg_music = None

    print("  [+] Đang render video chuyển động Full HD 9:16...")
    if clips:
        renderer.render_from_video_clips(
            video_clip_paths=clips,
            voice_audio_path=voice_audio,
            output_video_path=final_video,
            subtitle_path=ass_path,
            bg_music_path=bg_music,
            music_volume=0.12
        )
    else:
        print("  [!] Không có clip, bỏ qua render.")
        return None

    # 6. Upload
    print("  [+] Đang tải lên YouTube (Kênh 1)...")
    uploader = YouTubeUploader("channel_1")
    title = "Lá Chắn Bí Ẩn: Thứ Gì Đang Bảo Vệ Trái Đất Khỏi Tuyệt Chủng? 😱 #shorts"
    desc = """Bí ẩn vũ trụ: Thứ gì đang âm thầm bảo vệ sự sống trên Trái Đất suốt hàng tỷ năm qua?

🔔 Đăng ký kênh Kỳ Thú Khám Phá để không bỏ lỡ những sự thật chấn động!

#shorts #khoahoc #khampha #vutru #bian #traidat #saohoa #saomoc"""
    tags = ["shorts", "khoa hoc", "kham pha", "bi an", "vu tru", "thien thach", "sao moc", "trai dat", "ky thu kham pha"]

    res = uploader.upload_video(
        video_file_path=final_video,
        title=title,
        description=desc,
        tags=tags,
        category_id="28",
        privacy_status="public"
    )
    video_id = res if isinstance(res, str) else res.get("id")
    print(f"  🎉 [THÀNH CÔNG KÊNH 1] Video ID: {video_id} | https://youtu.be/{video_id}")
    return video_id


# =====================================================================
# TASK 2: CHANNEL 2 - VINTAGE HOLIDAY CLASSICS
# =====================================================================
async def produce_channel_2():
    print("\n" + "=" * 70)
    print("🎄 [BƯỚC 2/3] SẢN XUẤT SHORTS KÊNH 2 (VINTAGE HOLIDAY)")
    print("=" * 70)

    out_dir = os.path.join(ROOT_DIR, "outputs", "channel_2", "shorts")
    os.makedirs(out_dir, exist_ok=True)

    # Fetch vintage holiday stock video (e.g. cozy fireplace, Christmas market, snow)
    stock_clip = os.path.join(out_dir, "vintage_christmas_bg.mp4")
    if not os.path.exists(stock_clip):
        print("  [+] Tải video stock chuyển động Giáng sinh ấm cúng...")
        fetch_stock_video_clip("cozy fireplace christmas snow", stock_clip, orientation="portrait", fallback_keywords=["christmas tree lights", "winter snowfall"])

    # Generate audio: Generate a short voice intro or ambient
    intro_audio = os.path.join(out_dir, "intro_audio.mp3")
    script = "Step into the warmth of a 1950s Christmas. Tap the related video below for the full vintage holiday playlist."
    comm = edge_tts.Communicate(script, "en-US-ChristopherNeural", rate="-2%")
    await comm.save(intro_audio)

    renderer = VideoRenderer(width=1080, height=1920)
    final_video = os.path.join(out_dir, "christmas_short_master.mp4")

    # Render video
    if os.path.exists(stock_clip):
        renderer.render_from_video_clips(
            video_clip_paths=[stock_clip],
            voice_audio_path=intro_audio,
            output_video_path=final_video,
            music_volume=0.2
        )
    else:
        print("  [!] Không có clip Giáng sinh, bỏ qua.")
        return None

    # Upload
    print("  [+] Đang tải lên YouTube (Kênh 2)...")
    uploader = YouTubeUploader("channel_2")
    title = "Warm Memories of a 1950s Christmas 🎄 Cozy Fireplace & Vintage Joy #shorts"
    desc = """Relive the nostalgic warmth of classic holiday seasons.
    
🎄 FULL 100-MINUTE PLAYLIST LINKED IN RELATED VIDEO ABOVE!
Tap the Related Video link above to enjoy hours of relaxing vintage Christmas music.

🔔 Subscribe to Vintage Holiday Classics for daily holiday cheer!

#shorts #vintagechristmas #christmasmusic #1950schristmas #holidaynostalgia #cozyfireplace #christmassongs"""
    tags = ["shorts", "vintage christmas", "christmas music", "1950s christmas", "cozy fireplace", "holiday nostalgia", "vintage holiday classics"]

    res = uploader.upload_video(
        video_file_path=final_video,
        title=title,
        description=desc,
        tags=tags,
        category_id="10",
        privacy_status="public"
    )
    video_id = res if isinstance(res, str) else res.get("id")
    print(f"  🎉 [THÀNH CÔNG KÊNH 2] Video ID: {video_id} | https://youtu.be/{video_id}")
    return video_id


# =====================================================================
# TASK 3: CHANNEL 3 - STOIC ECHOES
# =====================================================================
async def produce_channel_3():
    print("\n" + "=" * 70)
    print("🏛️ [BƯỚC 3/3] SẢN XUẤT VIDEO SHORTS CHO KÊNH 3 (STOIC ECHOES)")
    print("=" * 70)

    shorts_dir = os.path.join(ROOT_DIR, "outputs", "channel_3", "shorts")
    os.makedirs(shorts_dir, exist_ok=True)

    script_text = """You have power over your mind—not outside events. Realize this, and you will find quiet strength.
Roman Emperor Marcus Aurelius woke up each morning with one simple truth:
Most of what you worry about has never happened, and will never happen.
You suffer far more in imagination than in reality.
Whenever anxiety threatens your peace, ask yourself:
"Is this within my control, or is it beyond my control?"
If it is beyond your control... let it go.
Clinging to what you cannot change is the ultimate form of self-torture.
Watch the full 7 Stoic Rules in the related video linked below."""

    voice_audio = os.path.join(shorts_dir, "stoic_voice.mp3")
    print("  [+] Đang tạo voiceover tiếng Anh (en-US-ChristopherNeural)...")
    comm = edge_tts.Communicate(script_text, 'en-US-ChristopherNeural', rate='-3%', pitch='-2Hz')
    await comm.save(voice_audio)

    renderer = VideoRenderer(width=1080, height=1920)
    tot_dur = renderer._get_audio_duration(voice_audio)
    print(f"      Thời lượng giọng đọc: {tot_dur:.2f}s")

    # Download Roman statue / Greek temple stock clips
    clip_1 = os.path.join(shorts_dir, "stoic_statue_clip.mp4")
    if not os.path.exists(clip_1):
        print("  [+] Tải video stock tượng La Mã / đền Hy Lạp...")
        fetch_stock_video_clip("ancient roman statue marble", clip_1, orientation="portrait", fallback_keywords=["greek sculpture temple", "dark rainy architecture"])

    # Subtitles
    ass_path = os.path.join(shorts_dir, "stoic_sub.ass")
    scenes = [{"sentence": s.strip()} for s in script_text.split("\n") if s.strip()]
    sentence_durs = [tot_dur / len(scenes)] * len(scenes)
    build_perfect_subtitles(scenes, sentence_durs, ass_path, is_shorts=True)

    # Render
    final_video = os.path.join(shorts_dir, "stoic_short_master.mp4")
    clips = [clip_1] if os.path.exists(clip_1) else []
    if clips:
        renderer.render_from_video_clips(
            video_clip_paths=clips,
            voice_audio_path=voice_audio,
            output_video_path=final_video,
            subtitle_path=ass_path,
            music_volume=0.1
        )
    else:
        print("  [!] Không có clip Stoic, bỏ qua.")
        return None

    # Upload
    print("  [+] Đang đăng tải lên YouTube (Stoic Echoes)...")
    uploader = YouTubeUploader("channel_3")
    title = "Marcus Aurelius: The 1-Minute Cure for Overthinking 🏛️ #shorts #stoicism"
    desc = """You have power over your mind—not outside events. Realize this, and you will find strength.

🏛️ WATCH THE FULL 10-MINUTE LESSON IN THE RELATED VIDEO ABOVE!
Discover the 7 Stoic Rules to protect your inner peace in a chaotic world.

🔔 Subscribe to Stoic Echoes for timeless philosophy and mental resilience.

#shorts #stoicism #marcusaurelius #overthinking #mentalhealth #philosophy #wisdom #innerpeace #stoic"""
    tags = ["shorts", "stoicism", "marcus aurelius", "overthinking", "how to stop overthinking", "stoic philosophy", "mental resilience", "inner peace"]

    res = uploader.upload_video(
        video_file_path=final_video,
        title=title,
        description=desc,
        tags=tags,
        category_id="27",
        privacy_status="public"
    )
    video_id = res if isinstance(res, str) else res.get("id")
    print(f"  🎉 [THÀNH CÔNG KÊNH 3] Video ID: {video_id} | Link: https://youtu.be/{video_id}")
    return video_id


# =====================================================================
# MASTER RUNNER
# =====================================================================
async def main():
    start_time = time.time()
    print("========================================================================")
    print("🔥 KHỞI ĐỘNG HỆ THỐNG SẢN XUẤT TOÀN DIỆN CHO CẢ 3 KÊNH YOUTUBE")
    print("========================================================================")

    # Run tasks with error handling so one channel failure never breaks others
    try:
        await produce_channel_1()
    except Exception as e:
        print(f"❌ [LỖI KÊNH 1]: {e}")

    try:
        await produce_channel_2()
    except Exception as e:
        print(f"❌ [LỖI KÊNH 2]: {e}")

    try:
        await produce_channel_3()
    except Exception as e:
        print(f"❌ [LỖI KÊNH 3]: {e}")

    total_time = time.time() - start_time
    print("\n" + "=" * 70)
    print(f"🏆 QUY TRÌNH KẾT THÚC TRONG {total_time/60:.1f} PHÚT!")
    print("=" * 70)

if __name__ == "__main__":
    asyncio.run(main())
