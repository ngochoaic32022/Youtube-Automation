import os
import sys
sys.path.append('d:/KENH GEHIHI')
import json
import time
import subprocess
import asyncio
import edge_tts
from faster_whisper import WhisperModel
from core.proxy_manager import get_proxy_youtube_client
from googleapiclient.http import MediaFileUpload

sys.stdout.reconfigure(encoding='utf-8')

SHORTS_DIR = "d:/KENH GEHIHI/outputs/channel_3/shorts"
os.makedirs(SHORTS_DIR, exist_ok=True)

TARGET_VIDEO_ID = "N5vVubDATXY"
TARGET_VIDEO_URL = f"https://www.youtube.com/watch?v={TARGET_VIDEO_ID}"
TARGET_VIDEO_TITLE = "7 Stoic Rules to Protect Your Peace of Mind"

SCRIPT_TEXT = """When someone insults you, disrespects you, or betrays your expectations... notice what happens inside you.
A surge of anger.
Marcus Aurelius wrote two thousand years ago:
"Choose not to be harmed—and you won't feel harmed. Don't feel harmed—and you haven't been."
An insult has zero power over you until you attach your own judgment to it.
When you react with rage, you are volunteering to be their puppet.
Next time someone provokes you: Pause. Look at them in complete silence.
Silence is not weakness. Silence is the ultimate display of supreme self-control.
Watch the full 7 Stoic Rules in the related video below."""

SEO_TITLE = "The Stoic Art of Not Giving a F*** 🏛️ #shorts #stoicism #marcusaurelius"
SEO_DESCRIPTION = f"""An insult has zero power over you until you attach your own judgment to it. 

🏛️ WATCH THE FULL 10-MINUTE LESSON HERE:
👉 {TARGET_VIDEO_URL}
(Or tap the Related Video link above the title!)

Discover the 7 Stoic Rules of Marcus Aurelius, Seneca, and Epictetus to protect your inner peace in a chaotic world.

🔔 Subscribe to Stoic Echoes for daily timeless wisdom and mental resilience.

#shorts #stoicism #marcusaurelius #seneca #philosophy #wisdom #mentalstrength #discipline #stoic"""

SEO_TAGS = ["shorts", "stoicism", "marcus aurelius", "stoic quotes", "mental strength", "how to stop caring", "stoic echoes", "philosophy", "inner peace"]

def sec_to_ass(seconds: float) -> str:
    centisec = int((seconds - int(seconds)) * 100)
    minutes, seconds = divmod(int(seconds), 60)
    hours, minutes = divmod(minutes, 60)
    return f"{hours}:{minutes:02d}:{seconds:02d}.{centisec:02d}"

async def generate_speech(audio_out: str):
    print("[*] Generating voiceover for Short 1...")
    comm = edge_tts.Communicate(SCRIPT_TEXT, 'en-US-ChristopherNeural', rate='-3%', pitch='-2Hz')
    await comm.save(audio_out)
    print(f"[+] Audio saved to: {audio_out}")

def build_ass(audio_path: str, ass_path: str, total_duration: float):
    print("[*] Transcribing with faster-whisper for karaoke ASS...")
    model = WhisperModel("tiny", device="cpu", compute_type="int8")
    segments, info = model.transcribe(audio_path, beam_size=5, word_timestamps=True)

    header = f"""[Script Info]
Title: Stoic Short 1 Subtitles
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
    tot_end = sec_to_ass(total_duration)

    # Top Badge
    events.append(f"Dialogue: 0,0:00:00.00,{tot_end},TopBadge,,0,0,0,,{{\\fad(400,400)}}✦ STOIC WISDOM ✦\\N{{\\fs32\\c&H00D0EBFF&}}Rule 2: Silence is Power\n")

    # Word by word karaoke
    for seg in segments:
        words = seg.words
        if not words:
            continue
        chunk_size = 4
        for i in range(0, len(words), chunk_size):
            chunk = words[i:i + chunk_size]
            for active_w in chunk:
                w_s = sec_to_ass(max(0.0, active_w.start))
                w_e = sec_to_ass(min(total_duration, active_w.end))
                line_words = []
                for w in chunk:
                    clean_w = w.word.strip()
                    if w == active_w:
                        line_words.append(f"{{\\c&H0027E2FE&\\3c&H000E6E9C&}}{clean_w}{{\\c&H00F5FAFF&\\3c&H00000000&}}")
                    else:
                        line_words.append(clean_w)
                events.append(f"Dialogue: 1,{w_s},{w_e},SubtitleKaraoke,,0,0,0,,{' '.join(line_words)}\n")

    # Bottom CTA
    cta_start = sec_to_ass(total_duration * 0.45)
    events.append(f"Dialogue: 2,{cta_start},{tot_end},BottomCTA,,0,0,0,,{{\\fad(400,0)}}✦ FULL 10-MIN LESSON LINKED BELOW ✦\\N{{\\fs32\\c&H00FFFFFF&}}Tap \"{TARGET_VIDEO_TITLE}\" below\\N{{\\fs26\\c&H00B0E0E6&}}Stoic Echoes\n")

    with open(ass_path, "w", encoding="utf-8") as f:
        f.write(header + "".join(events))
    print(f"[+] ASS subtitles written to: {ass_path}")

def render_short_video(bg_img: str, voice_audio: str, ass_path: str, out_video: str, duration: float):
    print(f"[*] Rendering vertical 9:16 Short ({duration:.1f}s)...")
    
    # Generate subtle rain audio bed
    rain_audio = f"{SHORTS_DIR}/rain_tmp.mp3"
    subprocess.run([
        "ffmpeg", "-y",
        "-f", "lavfi", "-t", str(duration),
        "-i", "anoisesrc=color=pink:amplitude=0.02:sample_rate=48000,lowpass=f=1200,highpass=f=200,volume=0.35",
        "-c:a", "libmp3lame", "-b:a", "128k",
        rain_audio
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    cmd = [
        "ffmpeg", "-y",
        "-loop", "1", "-t", str(duration), "-i", bg_img,
        "-i", voice_audio,
        "-i", rain_audio,
        "-filter_complex",
        f"[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,eq=brightness=0.02:contrast=1.08:saturation=1.15,ass={ass_path}[v_out];"
        "[1:a]volume=1.2[v_voice];"
        "[2:a]volume=0.25[v_rain];"
        "[v_voice][v_rain]amix=inputs=2:duration=first[a_mix];"
        f"[a_mix]afade=t=in:ss=0:d=0.5,afade=t=out:st={duration-1.0:.2f}:d=1.0[a_out]",
        "-map", "[v_out]",
        "-map", "[a_out]",
        "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "320k",
        "-shortest",
        out_video
    ]
    t0 = time.time()
    subprocess.run(cmd, check=True)
    if os.path.exists(rain_audio):
        os.remove(rain_audio)
    print(f"[SUCCESS] Short rendered in {time.time() - t0:.1f}s -> {out_video} ({os.path.getsize(out_video)/1024/1024:.2f} MB)")

def upload_short(video_path: str):
    yt = get_proxy_youtube_client("channel_3")
    body = {
        'snippet': {
            'title': SEO_TITLE,
            'description': SEO_DESCRIPTION,
            'tags': SEO_TAGS,
            'categoryId': '27'
        },
        'status': {
            'privacyStatus': 'public',
            'selfDeclaredMadeForKids': False
        }
    }
    print("[*] Uploading Short 1 to Channel 3 via Proxy...")
    media = MediaFileUpload(video_path, mimetype='video/mp4', resumable=True)
    req = yt.videos().insert(part='snippet,status', body=body, media_body=media)

    resp = None
    while resp is None:
        status, resp = req.next_chunk()
        if status:
            print(f"  [>] Upload Progress: {int(status.progress() * 100)}%")

    short_id = resp['id']
    short_url = f"https://youtube.com/shorts/{short_id}"
    print(f"\n[SUCCESS] SHORT 1 PUBLISHED LIVE! ID: {short_id}")
    print(f"👉 URL: {short_url}")
    return resp

def produce_and_upload():
    audio_path = f"{SHORTS_DIR}/short1_audio.mp3"
    ass_path = "outputs/channel_3/shorts/short1.ass"
    video_out = f"{SHORTS_DIR}/short1_master.mp4"
    bg_img = "d:/KENH GEHIHI/outputs/channel_3/video_1/visuals/scene_1.jpg"

    if not os.path.exists(audio_path):
        asyncio.run(generate_speech(audio_path))
    
    cmd_probe = ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", audio_path]
    dur = float(subprocess.check_output(cmd_probe).strip())
    print(f"[*] Audio Duration: {dur:.2f}s")

    build_ass(audio_path, ass_path, dur)
    render_short_video(bg_img, audio_path, ass_path, video_out, dur)
    upload_short(video_out)

if __name__ == "__main__":
    produce_and_upload()
