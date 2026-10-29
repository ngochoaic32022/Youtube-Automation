import os
import sys
sys.path.insert(0, "d:/KENH GEHIHI")
import json
import time
import subprocess
from datetime import datetime, timedelta, timezone
from core.proxy_manager import get_proxy_youtube_client
from googleapiclient.http import MediaFileUpload
from faster_whisper import WhisperModel

sys.stdout.reconfigure(encoding='utf-8')

TOKEN_PATH = "d:/KENH GEHIHI/config/tokens/token_channel_2.json"
OUTPUT_DIR = "outputs/channel_2"
SHORTS_OUT_DIR = "outputs/channel_2/shorts"
LOG_PATH = "outputs/channel_2/schedule_log.json"

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(SHORTS_OUT_DIR, exist_ok=True)

# 2 Long-form Videos & Playlist targets
V1_URL = "https://www.youtube.com/watch?v=1-6gOvgoQHw"
V1_TITLE = "Vintage Christmas Songs Playlist 🎄 (100 Mins)"

V2_URL = "https://www.youtube.com/watch?v=FVjOfcIBzp0"
V2_TITLE = "Traditional Christmas Carols 🔔 Silent Night, Joy to the World & More"

PLAYLIST_URL = "https://www.youtube.com/playlist?list=PLU5jJLH_2dYY"

# Curated Christmas Songs & Visual Matrix
CATALOG = [
    {
        "id": "most_wonderful_time",
        "song_name": "It's the Most Wonderful Time of the Year",
        "audio_path": "D:/MUSIC/YOUTUBE/LIST BAI/CLASSIC ORIGIN/It_s the Most Wonderful Time of the Year .mp3",
        "audio_start": 0.0,
        "audio_duration": 31.0,
        "clip_1": "D:/MUSIC/YOUTUBE/VID NỀN/moi/Christmas_30s_06_ChristmasMarket.mp4",
        "clip_2": "D:/MUSIC/YOUTUBE/VID NỀN/moi/Christmas_30s_07_ShopWindow.mp4",
        "badge_title": "❄️ 1950s HOLIDAY NOSTALGIA ❄️",
        "badge_sub": "When Christmas felt truly magical",
        "target_url": V1_URL,
        "target_title": "Vintage Christmas Songs Playlist",
        "seo_title": "Nothing Feels More Like Christmas Than This 🎄✨ #shorts #vintagechristmas",
        "description": f"""Step into the nostalgic warmth of 1950s holiday magic with "It's the Most Wonderful Time of the Year".

🎄 LISTEN TO THE FULL 100-MINUTE PLAYLIST HERE:
👉 {V1_URL}
(Or tap the Related Video link above the title!)

Featuring timeless holiday classics, crackling fireplace ambiance, and vintage jazz carols.
✨ Playlist: {PLAYLIST_URL}
🔔 Subscribe to Vintage Holiday Classics for daily holiday nostalgia!

#shorts #vintagechristmas #christmasmusic #1950schristmas #holidaynostalgia #christmassongs #christmascarols #winterwonderland #christmasvibes""",
        "tags": ["shorts", "vintage christmas", "1950s christmas", "most wonderful time of the year", "classic christmas songs", "christmas music", "holiday nostalgia", "vintage holiday classics"]
    },
    {
        "id": "let_it_snow",
        "song_name": "Let It Snow! Let It Snow! Let It Snow!",
        "audio_path": "D:/MUSIC/YOUTUBE/LIST BAI/CLASSIC ORIGIN/Let It Snow!.mp3",
        "audio_start": 9.5,
        "audio_duration": 29.0,
        "clip_1": "D:/MUSIC/YOUTUBE/VID NỀN/moi/Christmas_30s_08_FrostWindow.mp4",
        "clip_2": "D:/MUSIC/YOUTUBE/VID NỀN/moi/Christmas_30s_02_HotCocoa.mp4",
        "badge_title": "☕ COZY WINTER EVENING ☕",
        "badge_sub": "Warm fire & falling snow",
        "target_url": V1_URL,
        "target_title": "Vintage Christmas Songs Playlist",
        "seo_title": "When The Weather Outside Is Frightful ❄️☕ #shorts #cozychristmas",
        "description": f""""The weather outside is frightful, but the fire is so delightful..." Cozy up with this timeless Christmas classic!

🎄 LISTEN TO THE FULL 100-MINUTE VINTAGE PLAYLIST HERE:
👉 {V1_URL}
(Or tap the Related Video link above the title!)

✨ Full Playlist Collection: {PLAYLIST_URL}
🔔 Subscribe to Vintage Holiday Classics for daily peaceful holiday music!

#shorts #letitsnow #cozychristmas #vintagechristmas #christmasmusic #1950schristmas #holidaynostalgia #christmassongs #snowynight""",
        "tags": ["shorts", "let it snow", "cozy christmas", "vintage christmas", "christmas music", "1950s christmas", "holiday classics", "vintage holiday classics"]
    },
    {
        "id": "hark_herald_angels",
        "song_name": "Hark! The Herald Angels Sing",
        "audio_path": "D:/MUSIC/YOUTUBE/LIST BAI/CLASSIC ORIGIN/Hark the Herald Angels Sing.mp3",
        "audio_start": 0.0,
        "audio_duration": 33.0,
        "clip_1": "D:/MUSIC/YOUTUBE/VID NỀN/moi/Christmas_30s_14_BronzeBells.mp4",
        "clip_2": "D:/MUSIC/YOUTUBE/VID NỀN/moi/Christmas_30s_13_HymnChoir.mp4",
        "badge_title": "🔔 TRADITIONAL CHRISTMAS CAROL 🔔",
        "badge_sub": "Peace on earth and mercy mild",
        "target_url": V2_URL,
        "target_title": "Traditional Christmas Carols",
        "seo_title": "The Grandest Christmas Carol in History 🔔 Hark! #shorts #christmascarols",
        "description": f""""Hark! The herald angels sing, Glory to the newborn King!" Experience the uplifting beauty of traditional Christmas carols.

🔔 LISTEN TO THE FULL TRADITIONAL CAROLS COLLECTION HERE:
👉 {V2_URL}
(Or tap the Related Video link above the title!)

✨ Timeless Christmas Playlist: {PLAYLIST_URL}
🙏 Wishing you a peaceful, joyful Christmas filled with blessings.

#shorts #harktheheraldangelssing #christmascarols #traditionalchristmas #churchcarols #peacefulchristmas #christmassongs #holyholiday""",
        "tags": ["shorts", "hark the herald angels sing", "christmas carols", "traditional carols", "church christmas carols", "peaceful christmas", "vintage holiday classics"]
    },
    {
        "id": "silver_bells",
        "song_name": "Silver Bells",
        "audio_path": "D:/MUSIC/YOUTUBE/LIST BAI/CLASSIC ORIGIN/Silver Bells .mp3",
        "audio_start": 0.0,
        "audio_duration": 32.0,
        "clip_1": "D:/MUSIC/YOUTUBE/VID NỀN/moi/Christmas_30s_06_ChristmasMarket.mp4",
        "clip_2": "D:/MUSIC/YOUTUBE/VID NỀN/moi/Christmas_30s_27_LanternBridge.mp4",
        "badge_title": "✨ 1950s CHRISTMAS IN THE CITY ✨",
        "badge_sub": "Ring-a-ling, hear them ring",
        "target_url": V1_URL,
        "target_title": "Vintage Christmas Songs Playlist",
        "seo_title": "City Sidewalks, Busy Sidewalks... 🔔 Silver Bells #shorts #vintagechristmas",
        "description": f""""Silver bells, silver bells, it's Christmas time in the city!" Relive the golden era of holiday shopping, glowing streetlights, and snowfall.

🎄 LISTEN TO THE FULL 100-MINUTE VINTAGE PLAYLIST HERE:
👉 {V1_URL}

✨ Collection Playlist: {PLAYLIST_URL}
🔔 Subscribe to Vintage Holiday Classics for daily classic Christmas music!

#shorts #silverbells #vintagechristmas #1950schristmas #christmasmusic #holidaynostalgia #christmassongs #christmasinthecity""",
        "tags": ["shorts", "silver bells", "vintage christmas", "1950s christmas", "classic christmas songs", "holiday music", "vintage holiday classics"]
    },
    {
        "id": "o_holy_night",
        "song_name": "O Holy Night",
        "audio_path": "D:/MUSIC/YOUTUBE/LIST BAI/CLASSIC ORIGIN/O Holy Night.mp3",
        "audio_start": 0.0,
        "audio_duration": 34.0,
        "clip_1": "D:/MUSIC/YOUTUBE/VID NỀN/moi/Christmas_30s_11_CathedralCandle.mp4",
        "clip_2": "D:/MUSIC/YOUTUBE/VID NỀN/moi/Christmas_30s_28_NorthStar.mp4",
        "badge_title": "🕯️ SACRED CHRISTMAS EVE 🕯️",
        "badge_sub": "The stars are brightly shining",
        "target_url": V2_URL,
        "target_title": "Traditional Christmas Carols",
        "seo_title": "The Most Powerful Carol Ever Composed 🕯️ O Holy Night #shorts #christmas",
        "description": f""""O Holy Night, the stars are brightly shining, it is the night of our dear Savior's birth..." A moment of profound peace and reverence.

🔔 LISTEN TO THE FULL TRADITIONAL CAROLS COLLECTION HERE:
👉 {V2_URL}

✨ Peace & Carols Playlist: {PLAYLIST_URL}
🙏 Wishing you a blessed, serene Christmas season.

#shorts #oholynight #traditionalcarols #christmascarols #peacefulchristmas #churchhymns #silentnight #christmaseve #sacredchristmas""",
        "tags": ["shorts", "o holy night", "christmas carols", "traditional christmas", "peaceful christmas", "church music", "vintage holiday classics"]
    },
    {
        "id": "holly_jolly",
        "song_name": "A Holly Jolly Christmas",
        "audio_path": "D:/MUSIC/YOUTUBE/LIST BAI/CLASSIC ORIGIN/Holly Jolly Christmas .mp3",
        "audio_start": 0.0,
        "audio_duration": 30.0,
        "clip_1": "D:/MUSIC/YOUTUBE/VID NỀN/moi/Christmas_30s_23_Turntable.mp4",
        "clip_2": "D:/MUSIC/YOUTUBE/VID NỀN/moi/Christmas_30s_03_Ornaments.mp4",
        "badge_title": "🎄 1950s HOLIDAY CHEER 🎄",
        "badge_sub": "Have a cup of cheer",
        "target_url": V1_URL,
        "target_title": "Vintage Christmas Songs Playlist",
        "seo_title": "The Most Cheerful Christmas Song Ever Recorded ☕🎄 #shorts #christmas",
        "description": f""""Have a holly jolly Christmas, it's the best time of the year!" Put a smile on your face with this irresistible vintage favorite.

🎄 LISTEN TO THE FULL 100-MINUTE PLAYLIST HERE:
👉 {V1_URL}

✨ Full Christmas Classics Playlist: {PLAYLIST_URL}
🔔 Subscribe to Vintage Holiday Classics!

#shorts #hollyjollychristmas #vintagechristmas #christmasmusic #1950schristmas #holidaycheer #christmassongs #cozychristmas""",
        "tags": ["shorts", "holly jolly christmas", "vintage christmas", "christmas music", "1950s christmas", "holiday classics", "vintage holiday classics"]
    }
]

def load_schedule_log() -> dict:
    if os.path.exists(LOG_PATH):
        try:
            with open(LOG_PATH, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {"published": []}
    return {"published": []}

def save_schedule_log(log_data: dict):
    with open(LOG_PATH, 'w', encoding='utf-8') as f:
        json.dump(log_data, f, ensure_ascii=False, indent=2)

def sec_to_ass(seconds: float) -> str:
    centisec = int((seconds - int(seconds)) * 100)
    minutes, seconds = divmod(int(seconds), 60)
    hours, minutes = divmod(minutes, 60)
    return f"{hours}:{minutes:02d}:{seconds:02d}.{centisec:02d}"

def transcribe_and_build_ass(entry: dict, temp_audio_slice: str, ass_path: str):
    """Sử dụng faster-whisper tiny để nhận diện chính xác từng từ và tạo file phụ đề ASS karaoke"""
    print("[*] Transcribing audio with faster-whisper tiny...")
    model = WhisperModel("tiny", device="cpu", compute_type="int8")
    segments, info = model.transcribe(temp_audio_slice, beam_size=5, word_timestamps=True)

    header = f"""[Script Info]
Title: {entry['song_name']} Short
ScriptType: v4.00+
WrapStyle: 0
ScaledBorderAndShadow: yes
PlayResX: 1080
PlayResY: 1920

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: TitleBadge,Georgia,44,&H00FFFFFF,&H0000FFFF,&H00000000,&H90000000,-1,0,0,0,100,100,2,0,1,5,3,8,30,30,200,1
Style: SubtitleNormal,Arial,58,&H00F5FAFF,&H0000FFFF,&H00000000,&HA0000000,-1,0,0,0,100,100,1,0,1,6,4,2,40,40,820,1
Style: FunnelCTA,Arial Black,42,&H0015E8FF,&H0000FFFF,&H00000000,&HA0000000,-1,0,0,0,100,100,1,0,1,5,3,2,30,30,260,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    events = []
    tot_dur = entry["audio_duration"]
    tot_end = sec_to_ass(tot_dur)

    # Top Badge (Clean ASCII / Unicode without emoji box errors)
    b_title = entry["badge_title"].replace("❄️", "✦").replace("☕", "✦").replace("🔔", "✦").replace("🎄", "✦")
    b_sub = entry["badge_sub"]
    events.append(f"Dialogue: 0,0:00:00.00,{tot_end},TitleBadge,,0,0,0,,{{\\fad(400,400)}}{b_title}\\N{{\\fs32\\c&H00D0EBFF&}}{b_sub}\n")

    # Word-by-word karaoke
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
                    clean_word = w.word.strip()
                    if w == active_w:
                        line_words.append(f"{{\\c&H0027E2FE&\\3c&H000E6E9C&}}{clean_word}{{\\c&H00F5FAFF&\\3c&H00000000&}}")
                    else:
                        line_words.append(clean_word)
                rendered = " ".join(line_words)
                events.append(f"Dialogue: 1,{w_s},{w_e},SubtitleNormal,,0,0,0,,{rendered}\n")

    # Bottom Funnel CTA (Clean glyphs)
    cta_start = sec_to_ass(tot_dur * 0.40)
    t_title = entry["target_title"]
    events.append(f"Dialogue: 2,{cta_start},{tot_end},FunnelCTA,,0,0,0,,{{\\fad(400,0)}}✦ FULL PLAYLIST LINKED BELOW ✦\\N{{\\fs32\\c&H00FFFFFF&}}Tap \"{t_title}\" below\\N{{\\fs26\\c&H00B0E0E6&}}Vintage Holiday Classics\n")

    with open(ass_path, "w", encoding="utf-8") as f:
        f.write(header + "".join(events))
    print(f"[+] Created ASS subtitles: {ass_path}")

def render_short_video(entry: dict) -> str:
    short_id = entry["id"]
    out_mp4 = f"{SHORTS_OUT_DIR}/{short_id}.mp4"
    if os.path.exists(out_mp4) and os.path.getsize(out_mp4) > 1000000:
        print(f"[*] Short video already rendered: {out_mp4}")
        return out_mp4
    ass_path = f"{SHORTS_OUT_DIR}/{short_id}.ass"
    temp_audio = f"{SHORTS_OUT_DIR}/temp_{short_id}.mp3"

    dur = entry["audio_duration"]
    start = entry["audio_start"]
    half_dur = dur / 2.0

    print(f"\n[*] Rendering Short Video for: {entry['song_name']} ({dur:.1f}s)...")

    # 1. Slice audio
    cmd_audio = [
        "ffmpeg", "-y",
        "-ss", str(start), "-t", str(dur),
        "-i", entry["audio_path"],
        temp_audio
    ]
    subprocess.run(cmd_audio, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # 2. Build ASS Subtitles with faster-whisper
    transcribe_and_build_ass(entry, temp_audio, ass_path)

    # 3. Render 1080x1920 video with FFmpeg
    # Dual background clips
    clip1 = entry["clip_1"]
    clip2 = entry["clip_2"]

    cmd_video = [
        "ffmpeg", "-y",
        "-i", temp_audio,
        "-ss", "0.0", "-t", f"{half_dur:.2f}", "-i", clip1,
        "-ss", "0.0", "-t", f"{half_dur:.2f}", "-i", clip2,
        "-filter_complex",
        "[1:v][2:v]concat=n=2:v=1:a=0[v_raw];"
        "[v_raw]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,eq=brightness=0.02:contrast=1.08:saturation=1.18[v_comp];"
        f"[v_comp]ass={ass_path}[v];"
        f"[0:a]afade=t=in:ss=0:d=1.0,afade=t=out:st={dur-1.5:.2f}:d=1.5[a]",
        "-map", "[v]", "-map", "[a]",
        "-c:v", "libx264", "-preset", "medium", "-crf", "23",
        "-c:a", "aac", "-b:a", "320k",
        "-shortest",
        out_mp4
    ]

    t0 = time.time()
    res = subprocess.run(cmd_video, capture_output=True, text=True)
    if res.returncode != 0:
        print("[!] FFmpeg Error:\n", res.stderr[-600:])
        raise RuntimeError("Video rendering failed")

    print(f"[+] Render finished in {time.time() - t0:.1f}s -> {out_mp4} ({os.path.getsize(out_mp4)/1024/1024:.2f} MB)")
    if os.path.exists(temp_audio):
        os.remove(temp_audio)
    return out_mp4

def upload_short_to_youtube(entry: dict, video_path: str, publish_at_iso: str = None) -> dict:
    yt = get_proxy_youtube_client("channel_2")

    is_scheduled = publish_at_iso is not None

    status_body = {
        'privacyStatus': 'private' if is_scheduled else 'public',
        'selfDeclaredMadeForKids': False
    }
    if is_scheduled:
        status_body['publishAt'] = publish_at_iso

    body = {
        'snippet': {
            'title': entry['seo_title'],
            'description': entry['description'],
            'tags': entry['tags'],
            'categoryId': '10' # Music
        },
        'status': status_body
    }

    print(f"[*] Uploading {entry['id']} to Channel 2 (Mode: {'SCHEDULED at ' + publish_at_iso if is_scheduled else 'PUBLIC'})...")
    media = MediaFileUpload(video_path, mimetype='video/mp4', resumable=True)
    req = yt.videos().insert(part='snippet,status', body=body, media_body=media)

    resp = None
    while resp is None:
        status, resp = req.next_chunk()
        if status:
            print(f"    Upload progress: {int(status.progress() * 100)}%")

    vid = resp['id']
    short_url = f"https://youtube.com/shorts/{vid}"
    print(f"[+] Uploaded successfully! Video ID: {vid} -> {short_url}")

    # Pinned comment
    time.sleep(2)
    comment_text = f"🎄 Listen to our complete {entry['target_title']} here: {entry['target_url']} ☕❄️ (Or tap the Related Video link above the title!)"
    try:
        c_body = {
            'snippet': {
                'videoId': vid,
                'topLevelComment': {
                    'snippet': {
                        'textOriginal': comment_text
                    }
                }
            }
        }
        yt.commentThreads().insert(part='snippet', body=c_body).execute()
        print(f"[+] Pinned comment posted on {vid}")
    except Exception as e:
        print(f"[!] Could not post comment (will post when public): {e}")

    # Record log
    log = load_schedule_log()
    log["published"].append({
        "id": entry["id"],
        "video_id": vid,
        "url": short_url,
        "title": entry["seo_title"],
        "song_name": entry["song_name"],
        "publish_at": publish_at_iso if is_scheduled else "INSTANT_PUBLIC",
        "timestamp": datetime.now(timezone.utc).isoformat()
    })
    save_schedule_log(log)

    return {
        "video_id": vid,
        "url": short_url,
        "title": entry["seo_title"]
    }

def produce_next_shorts(count: int = 1, schedule_mode: bool = True):
    """Sản xuất và lên lịch tự động cho các video Shorts tiếp theo"""
    log = load_schedule_log()
    published_ids = {item["id"] for item in log.get("published", [])}

    available = [item for item in CATALOG if item["id"] not in published_ids]
    if not available:
        print("[*] All catalog items published! Cycling back to refreshed versions.")
        available = CATALOG

    to_produce = available[:count]
    print(f"[*] Queue to produce ({len(to_produce)} videos): {[x['id'] for x in to_produce]}")

    results = []
    # Optimal posting hours in GMT+7: 07:00 and 19:00 (matching US peak commute & evening hours)
    base_time = datetime.now(timezone.utc) + timedelta(hours=2)

    for idx, entry in enumerate(to_produce):
        video_file = render_short_video(entry)

        publish_iso = None
        if schedule_mode:
            # First one scheduled 3 hours ahead, second one 10 hours ahead
            sched_time = base_time + timedelta(hours=idx * 8)
            # Round to minute
            sched_time = sched_time.replace(second=0, microsecond=0)
            publish_iso = sched_time.isoformat()

        res = upload_short_to_youtube(entry, video_file, publish_iso)
        results.append(res)

    print("\n================ PRODUCTION COMPLETE ================")
    for r in results:
        print(f"Short: {r['title']} -> {r['url']}")
    return results

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '--list':
        log = load_schedule_log()
        published_ids = {item["id"] for item in log.get("published", [])}
        print("=== CHRISTMAS SHORTS CATALOG ===")
        for item in CATALOG:
            status = "[DONE]" if item["id"] in published_ids else "[READY]"
            print(f"{status} {item['id']:<22} | {item['song_name']}")
    else:
        produce_next_shorts(count=1, schedule_mode=False)
