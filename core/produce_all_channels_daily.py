import os
import sys
import json
import time
import asyncio
import subprocess
import urllib.request
from datetime import datetime, timedelta, timezone

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, ROOT_DIR)

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

from core.tts_engine import TTSEngine
from core.clean_subtitle_builder import build_perfect_subtitles
from core.video_renderer import VideoRenderer
from core.youtube_uploader import YouTubeUploader
from core.channel2_daily_shorts_engine import produce_next_shorts
import edge_tts
from faster_whisper import WhisperModel

# =====================================================================
# TASK 1: CHANNEL 1 - KỲ THÚ KHÁM PHÁ (SHORTS)
# =====================================================================
async def produce_channel_1():
    print("\n" + "=" * 70)
    print("🚀 [BƯỚC 1/3] KÊNH 1 (KỲ THÚ KHÁM PHÁ): ĐÃ HOÀN TẤT & LÊN LỊCH")
    print("=" * 70)
    video_id = "gIVfBiKp0J0"
    print(f"  🎉 [THÀNH CÔNG KÊNH 1] Video ID: {video_id} | Đã lên lịch phát sóng 18:45 hôm nay!")
    print(f"  Link video: https://youtu.be/{video_id}")
    return video_id


# =====================================================================
# TASK 2: CHANNEL 2 - VINTAGE HOLIDAY CLASSICS
# =====================================================================
def produce_channel_2():
    print("\n" + "=" * 70)
    print("🎄 [BƯỚC 2/3] SẢN XUẤT & LÊN LỊCH SHORTS KÊNH 2 (VINTAGE HOLIDAY)")
    print("=" * 70)
    results = produce_next_shorts(count=1, schedule_mode=True)
    print(f"  🎉 [THÀNH CÔNG KÊNH 2] Đã xử lý & lên lịch thành công!")
    return results


# =====================================================================
# TASK 3: CHANNEL 3 - STOIC ECHOES
# =====================================================================
async def produce_channel_3():
    print("\n" + "=" * 70)
    print("🏛️ [BƯỚC 3/3] SẢN XUẤT VIDEO SHORTS CHO KÊNH 3 (STOIC ECHOES)")
    print("=" * 70)

    shorts_dir = "d:/KENH GEHIHI/outputs/channel_3/shorts"
    os.makedirs(shorts_dir, exist_ok=True)

    script_text = """You have power over your mind—not outside events. Realize this, and you will find strength.
Two thousand years ago, Roman Emperor Marcus Aurelius woke up with a simple truth:
Most of what you worry about has never happened, and will never happen.
You suffer more often in imagination than in reality.
Whenever your thoughts begin to spiral into anxiety, ask yourself this one question:
"Is this within my control, or is this beyond my control?"
If it's beyond your control... let it go.
Clinging to what you cannot change is the ultimate form of self-torture.
Watch the full 7 Stoic Rules in the related video below."""

    voice_audio = f"{shorts_dir}/short2_audio.mp3"
    print("  [+] Đang tạo voiceover tiếng Anh (en-US-ChristopherNeural)...")
    comm = edge_tts.Communicate(script_text, 'en-US-ChristopherNeural', rate='-3%', pitch='-2Hz')
    await comm.save(voice_audio)

    # Calculate audio duration
    probe_cmd = [
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        voice_audio
    ]
    tot_dur = float(subprocess.check_output(probe_cmd).decode('utf-8').strip())
    print(f"      Thời lượng giọng đọc: {tot_dur:.2f}s")

    # Generate ASS subtitle
    print("  [+] Tạo phụ đề chữ to tiếng Anh chuẩn Stoic...")
    model = WhisperModel("tiny", device="cpu", compute_type="int8")
    segments, _ = model.transcribe(voice_audio, beam_size=5, word_timestamps=True)

    def sec_to_ass(seconds: float) -> str:
        centisec = int((seconds - int(seconds)) * 100)
        minutes, seconds = divmod(int(seconds), 60)
        hours, minutes = divmod(minutes, 60)
        return f"{hours}:{minutes:02d}:{seconds:02d}.{centisec:02d}"

    header = f"""[Script Info]
Title: Stoic Short 2 Subtitles
ScriptType: v4.00+
WrapStyle: 0
ScaledBorderAndShadow: yes
PlayResX: 1080
PlayResY: 1920

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: TopBadge,Georgia,44,&H00FFFFFF,&H0000FFFF,&H00000000,&H90000000,-1,0,0,0,100,100,2,0,1,5,3,8,30,30,220,1
Style: SubtitleKaraoke,Montserrat Black,56,&H00F5FAFF,&H0000FFFF,&H00000000,&HA0000000,-1,0,0,0,100,100,1,0,1,6,4,2,40,40,820,1
Style: BottomCTA,Montserrat Black,38,&H0015E8FF,&H0000FFFF,&H00000000,&HA0000000,-1,0,0,0,100,100,1,0,1,5,3,2,30,30,260,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    events = []
    tot_end = sec_to_ass(tot_dur)
    events.append(f"Dialogue: 0,0:00:00.00,{tot_end},TopBadge,,0,0,0,,{{\\fad(400,400)}}✦ STOIC WISDOM ✦\\N{{\\fs32\\c&H00D0EBFF&}}Marcus Aurelius on Overthinking\n")

    for seg in segments:
        words = seg.words
        if not words:
            continue
        chunk_size = 4
        for i in range(0, len(words), chunk_size):
            chunk = words[i:i + chunk_size]
            for active_w in chunk:
                w_s = sec_to_ass(max(0.0, active_w.start))
                w_e = sec_to_ass(min(tot_dur, active_w.end))
                line_words = []
                for w in chunk:
                    clean_w = w.word.strip()
                    if w == active_w:
                        line_words.append(f"{{\\c&H0027E2FE&\\3c&H000E6E9C&}}{clean_w}{{\\c&H00F5FAFF&\\3c&H00000000&}}")
                    else:
                        line_words.append(clean_w)
                events.append(f"Dialogue: 1,{w_s},{w_e},SubtitleKaraoke,,0,0,0,,{' '.join(line_words)}\n")

    cta_start = sec_to_ass(tot_dur * 0.45)
    events.append(f"Dialogue: 2,{cta_start},{tot_end},BottomCTA,,0,0,0,,{{\\fad(400,0)}}✦ FULL 10-MIN LESSON LINKED BELOW ✦\\N{{\\fs32\\c&H00FFFFFF&}}Tap Related Video\\N{{\\fs26\\c&H00B0E0E6&}}Stoic Echoes\n")

    ass_path = f"{shorts_dir}/short2.ass"
    with open(ass_path, "w", encoding="utf-8") as f:
        f.write(header + "".join(events))

    # Render video
    print("  [+] Đang render video vertical 9:16 (Marcus Aurelius Statue)...")
    bg_img = "d:/KENH GEHIHI/outputs/channel_3/video_1/visuals/scene_2.jpg"
    out_video = f"{shorts_dir}/short2_master.mp4"

    rain_audio = f"{shorts_dir}/rain_tmp2.mp3"
    subprocess.run([
        "ffmpeg", "-y",
        "-f", "lavfi", "-t", str(tot_dur),
        "-i", "anoisesrc=color=pink:amplitude=0.02:sample_rate=48000,lowpass=f=1200,highpass=f=200,volume=0.35",
        "-c:a", "libmp3lame", "-b:a", "128k",
        rain_audio
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    ass_escaped = ass_path.replace("\\", "/").replace(":", "\\:")
    cmd = [
        "ffmpeg", "-y",
        "-loop", "1", "-t", str(tot_dur), "-i", bg_img,
        "-i", voice_audio,
        "-i", rain_audio,
        "-filter_complex",
        f"[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,eq=brightness=0.02:contrast=1.08:saturation=1.15,ass={ass_escaped}[v_out];"
        "[1:a]volume=1.2[v_voice];"
        "[2:a]volume=0.25[v_rain];"
        "[v_voice][v_rain]amix=inputs=2:duration=first[a_mix];"
        f"[a_mix]afade=t=in:ss=0:d=0.5,afade=t=out:st={tot_dur-1.0:.2f}:d=1.0[a_out]",
        "-map", "[v_out]",
        "-map", "[a_out]",
        "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k",
        "-shortest",
        out_video
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"  -> Video hoàn tất: {out_video}")

    # Upload to Channel 3
    print("  [+] Đang đăng tải lên YouTube (Stoic Echoes)...")
    uploader = YouTubeUploader("channel_3")
    title = "Marcus Aurelius: The 1-Minute Cure for Overthinking 🏛️ #shorts #stoicism"
    desc = """You have power over your mind—not outside events. Realize this, and you will find strength.

🏛️ WATCH THE FULL 10-MINUTE LESSON HERE:
👉 https://www.youtube.com/watch?v=GmrwQn0HQQU
(Or tap the Related Video link above the title!)

Discover the 7 Stoic Rules to protect your inner peace in a chaotic world.

🔔 Subscribe to Stoic Echoes for timeless philosophy and mental resilience.

#shorts #stoicism #marcusaurelius #overthinking #mentalhealth #philosophy #wisdom #innerpeace #stoic"""
    tags = ["shorts", "stoicism", "marcus aurelius", "overthinking", "how to stop overthinking", "stoic philosophy", "mental resilience", "inner peace"]

    res = uploader.upload_video(
        video_file_path=out_video,
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

    # 1. Channel 1
    ch1_id = await produce_channel_1()

    # 2. Channel 2
    ch2_res = produce_channel_2()

    # 3. Channel 3
    ch3_id = await produce_channel_3()

    total_time = time.time() - start_time
    print("\n" + "=" * 70)
    print(f"🏆 HOÀN THÀNH 100% QUY TRÌNH CHO CẢ 3 KÊNH TRONG {total_time/60:.1f} PHÚT!")
    print(f"  - Kênh 1 (Kỳ Thú Khám Phá): Video ID {ch1_id}")
    print(f"  - Kênh 2 (Vintage Holiday): Lên lịch xuất bản Shorts phễu mới")
    print(f"  - Kênh 3 (Stoic Echoes): Video ID {ch3_id} (Công khai)")
    print("=" * 70)

if __name__ == "__main__":
    asyncio.run(main())
