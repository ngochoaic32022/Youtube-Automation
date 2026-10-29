import os
import sys
import time
import asyncio
import subprocess
import json

sys.path.insert(0, "d:/KENH GEHIHI")

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

import edge_tts
from faster_whisper import WhisperModel
from core.youtube_uploader import YouTubeUploader

WORKDIR = "d:/KENH GEHIHI"
BASE_DIR = "outputs/channel_3/video_2"
VISUALS_DIR = "outputs/channel_3/video_1/visuals"
OUT_DIR = os.path.join(WORKDIR, BASE_DIR)
os.makedirs(OUT_DIR, exist_ok=True)

SCRIPT_PATH = os.path.join(OUT_DIR, "script.txt")
VOICE_PATH = os.path.join(OUT_DIR, "audio_voice.mp3")
MASTER_AUDIO_PATH = os.path.join(OUT_DIR, "master_audio.mp3")
ASS_PATH = os.path.join(OUT_DIR, "subtitles_styled.ass")
OUT_VIDEO = os.path.join(OUT_DIR, "master_video.mp4")
CONCAT_FILE = os.path.join(OUT_DIR, "concat.txt")

SEO_DATA = {
    "title": "How to Become Untouchable: 7 Stoic Lessons on Quiet Strength (Marcus Aurelius & Seneca)",
    "description": """True power is never loud. Loudness is insecurity disguised as confidence. True power is quiet, immovable, and untouchable.

In this deep philosophical exploration, we uncover 7 Stoic lessons from Roman Emperor Marcus Aurelius, Seneca, and Epictetus on how to build an unbreakable mind and master the art of quiet strength in an overwhelming, chaotic world.

🏛️ TIMESTAMPS:
00:00 - The Illusion of Loud Power
01:10 - Lesson 1: Speak Only When Words Beat Silence
02:25 - Lesson 2: Never Seek Approval From Strangers
03:40 - Lesson 3: The Art of Emotional Non-Reaction
05:00 - Lesson 4: Practice Voluntary Discomfort
06:20 - Lesson 5: Stop Explaining Yourself to Fools
07:45 - Lesson 6: Amor Fati - Turn Adversity Into Fuel
09:10 - Lesson 7: Memento Mori - The Ultimate Perspective
10:30 - Conclusion: The Unbreakable Sanctuary

🔔 Subscribe to Stoic Echoes for timeless philosophy, discipline, and mental resilience.

#stoicism #marcusaurelius #seneca #philosophy #wisdom #mentalstrength #discipline #selfcontrol #stoicwisdom #ancientwisdom #mindset #innerpeace
""",
    "tags": [
        "stoicism", "marcus aurelius", "seneca", "epictetus", "quiet strength", 
        "how to be untouchable", "stoic philosophy", "mental resilience", "self discipline", 
        "inner peace", "philosophy", "stoic quotes", "ancient wisdom"
    ]
}

def sec_to_ass(seconds: float) -> str:
    centisec = int((seconds - int(seconds)) * 100)
    minutes, seconds = divmod(int(seconds), 60)
    hours, minutes = divmod(minutes, 60)
    return f"{hours}:{minutes:02d}:{seconds:02d}.{centisec:02d}"

async def step_1_generate_voice():
    if os.path.exists(VOICE_PATH) and os.path.getsize(VOICE_PATH) > 100000:
        print(f"[+] Voiceover file already exists: {VOICE_PATH}")
        return

    print("[1/5] Generating English Voiceover (en-US-ChristopherNeural)...")
    with open(SCRIPT_PATH, "r", encoding="utf-8") as f:
        raw_text = f.read()

    # Filter out section brackets
    clean_lines = []
    for line in raw_text.splitlines():
        line = line.strip()
        if not line or line.startswith("["):
            continue
        clean_lines.append(line)
    narration_text = " ".join(clean_lines)

    comm = edge_tts.Communicate(narration_text, 'en-US-ChristopherNeural', rate='-3%', pitch='-2Hz')
    await comm.save(VOICE_PATH)
    print(f"[+] Voiceover saved to: {VOICE_PATH}")

def step_2_mix_audio():
    if os.path.exists(MASTER_AUDIO_PATH) and os.path.getsize(MASTER_AUDIO_PATH) > 100000:
        print(f"[+] Master audio file already exists: {MASTER_AUDIO_PATH}")
        return

    print("[2/5] Mixing voiceover with ambient meditative rain soundscape...")
    # Check voice duration
    cmd_probe = [
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        VOICE_PATH
    ]
    dur = float(subprocess.check_output(cmd_probe).decode("utf-8").strip())

    # Generate subtle rain audio
    rain_audio = os.path.join(OUT_DIR, "ambient_rain.mp3")
    subprocess.run([
        "ffmpeg", "-y",
        "-f", "lavfi", "-t", str(dur + 2.0),
        "-i", "anoisesrc=color=pink:amplitude=0.015:sample_rate=48000,lowpass=f=1200,highpass=f=200,volume=0.25",
        "-c:a", "libmp3lame", "-b:a", "128k",
        rain_audio
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # Mix voice + rain
    cmd_mix = [
        "ffmpeg", "-y",
        "-i", VOICE_PATH,
        "-i", rain_audio,
        "-filter_complex",
        "[0:a]volume=1.2[v];"
        "[1:a]volume=0.2[a_bg];"
        "[v][a_bg]amix=inputs=2:duration=first[out]",
        "-map", "[out]",
        "-c:a", "libmp3lame", "-b:a", "192k",
        MASTER_AUDIO_PATH
    ]
    subprocess.run(cmd_mix, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if os.path.exists(rain_audio):
        os.remove(rain_audio)
    print(f"[+] Master audio created: {MASTER_AUDIO_PATH} ({dur/60:.1f} mins)")

def step_3_generate_subtitles():
    if os.path.exists(ASS_PATH) and os.path.getsize(ASS_PATH) > 5000:
        print(f"[+] Subtitles ASS file already exists: {ASS_PATH}")
        return

    print("[3/5] Transcribing and styling ASS subtitles (16:9 1920x1080)...")
    model = WhisperModel("tiny", device="cpu", compute_type="int8")
    segments, _ = model.transcribe(VOICE_PATH, beam_size=5)

    header = """[Script Info]
Title: Stoic Echoes Long-form 2
ScriptType: v4.00+
WrapStyle: 0
ScaledBorderAndShadow: yes
PlayResX: 1920
PlayResY: 1080

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Georgia,42,&H00FFFFFF,&H0000FFFF,&H00000000,&H90000000,-1,0,0,0,100,100,1,0,1,4,2,2,80,80,90,1
Style: Accent,Montserrat Black,44,&H0015E8FF,&H0000FFFF,&H00000000,&HA0000000,-1,0,0,0,100,100,1,0,1,5,3,2,80,80,90,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    events = []
    for seg in segments:
        text = seg.text.strip()
        if not text:
            continue
        s_time = sec_to_ass(seg.start)
        e_time = sec_to_ass(seg.end)
        # Highlight important philosophical words
        styled_text = text.replace("Marcus Aurelius", "{\\c&H0027E2FE&}Marcus Aurelius{\\c&H00FFFFFF&}") \
                          .replace("Seneca", "{\\c&H0027E2FE&}Seneca{\\c&H00FFFFFF&}") \
                          .replace("Epictetus", "{\\c&H0027E2FE&}Epictetus{\\c&H00FFFFFF&}") \
                          .replace("Amor Fati", "{\\c&H0027E2FE&}Amor Fati{\\c&H00FFFFFF&}") \
                          .replace("Memento Mori", "{\\c&H0027E2FE&}Memento Mori{\\c&H00FFFFFF&}")
        events.append(f"Dialogue: 0,{s_time},{e_time},Default,,0,0,0,,{styled_text}\n")

    with open(ASS_PATH, "w", encoding="utf-8") as f:
        f.write(header + "".join(events))
    print(f"[+] ASS subtitles written to: {ASS_PATH}")

def step_4_render_video():
    if os.path.exists(OUT_VIDEO) and os.path.getsize(OUT_VIDEO) > 10000000:
        print(f"[+] Master video already rendered: {OUT_VIDEO}")
        return OUT_VIDEO

    print("[4/5] Rendering 1080p 16:9 Master Video with FFmpeg...")
    cmd_probe = [
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        MASTER_AUDIO_PATH
    ]
    dur = float(subprocess.check_output(cmd_probe).decode("utf-8").strip())
    print(f"      Total Video Duration: {dur:.2f}s ({dur/60:.1f} mins)")

    # Build sequence of 14 shots using available 7 marble statues
    shot_count = 14
    shot_dur = dur / shot_count

    with open(CONCAT_FILE, "w", encoding="utf-8") as f:
        for shot in range(shot_count):
            idx = (shot % 7) + 1
            img_path = f"{WORKDIR}/{VISUALS_DIR}/scene_{idx}.jpg".replace("\\", "/")
            f.write(f"file '{img_path}'\n")
            f.write(f"duration {shot_dur:.3f}\n")
        last_img = f"{WORKDIR}/{VISUALS_DIR}/scene_7.jpg".replace("\\", "/")
        f.write(f"file '{last_img}'\n")

    ass_relative = f"{BASE_DIR}/subtitles_styled.ass"
    cmd_render = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0", "-i", CONCAT_FILE,
        "-i", MASTER_AUDIO_PATH,
        "-filter_complex",
        f"[0:v]fps=24,scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,eq=brightness=0.01:contrast=1.06:saturation=1.12,ass='{ass_relative}'[v_out]",
        "-map", "[v_out]",
        "-map", "1:a",
        "-c:v", "libx264", "-preset", "fast", "-crf", "22", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k",
        "-shortest",
        OUT_VIDEO
    ]

    t0 = time.time()
    res = subprocess.run(cmd_render, capture_output=True, text=True)
    if res.returncode != 0:
        print("[!] FFmpeg Error:\n", res.stderr[-800:])
        raise RuntimeError("Video rendering failed")

    print(f"[+] Render complete in {time.time()-t0:.1f}s -> {OUT_VIDEO} ({os.path.getsize(OUT_VIDEO)/1024/1024:.2f} MB)")
    return OUT_VIDEO

def step_5_upload():
    print("[5/5] Uploading Master Video to Channel 3 (Stoic Echoes) via Proxy...")
    uploader = YouTubeUploader("channel_3")
    
    vid = uploader.upload_video(
        video_file_path=OUT_VIDEO,
        title=SEO_DATA["title"],
        description=SEO_DATA["description"],
        tags=SEO_DATA["tags"],
        category_id="27",
        privacy_status="public"
    )

    # Save metadata log
    log_file = os.path.join(OUT_DIR, "publish_log.json")
    with open(log_file, "w", encoding="utf-8") as f:
        json.dump({
            "video_id": vid,
            "url": f"https://www.youtube.com/watch?v={vid}",
            "title": SEO_DATA["title"],
            "published_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        }, f, indent=2, ensure_ascii=False)

    print(f"\n🎉 [HOÀN TẤT THÀNH CÔNG] Video Dài Kênh 3 Đã Lên Sóng!")
    print(f"👉 Link: https://www.youtube.com/watch?v={vid}")
    return vid

async def main():
    print("=" * 75)
    print("🏛️ KHỞI CHẠY QUY TRÌNH SẢN XUẤT VIDEO DÀI (LONG-FORM) SỐ 2 CHO KÊNH 3")
    print("Chủ đề: How to Become Untouchable: 7 Stoic Lessons on Quiet Strength")
    print("=" * 75)
    
    await step_1_generate_voice()
    step_2_mix_audio()
    step_3_generate_subtitles()
    step_4_render_video()
    step_5_upload()

if __name__ == "__main__":
    asyncio.run(main())
