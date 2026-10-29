import os
import sys
import json
import subprocess
import time
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

sys.stdout.reconfigure(encoding='utf-8')

OUTPUT_DIR = "d:/KENH GEHIHI/outputs/christmas_shorts"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def sec_to_ass(seconds: float) -> str:
    centisec = int((seconds - int(seconds)) * 100)
    minutes, seconds = divmod(int(seconds), 60)
    hours, minutes = divmod(minutes, 60)
    return f"{hours}:{minutes:02d}:{seconds:02d}.{centisec:02d}"

def write_ass_short_1(ass_path: str):
    header = """[Script Info]
Title: Christmas Short 1
ScriptType: v4.00+
WrapStyle: 0
ScaledBorderAndShadow: yes
PlayResX: 1080
PlayResY: 1920

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: TitleBadge,Georgia,46,&H00FFFFFF,&H0000FFFF,&H00000000,&H90000000,-1,0,0,0,100,100,1,0,1,5,3,8,30,30,220,1
Style: SubtitleNormal,Georgia,54,&H00F5FAFF,&H0000FFFF,&H00000000,&HA0000000,-1,0,0,0,100,100,1,0,1,6,4,2,40,40,680,1
Style: FunnelCTA,Montserrat Black,40,&H0015E8FF,&H0000FFFF,&H00000000,&HA0000000,-1,0,0,0,100,100,1,0,1,5,3,2,30,30,320,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    events = []
    # Badge (Top)
    events.append("Dialogue: 0,0:00:00.00,0:00:34.00,TitleBadge,,0,0,0,,{\\fad(400,400)}❄️ 1950s VINTAGE CHRISTMAS ❄️\\N{\\fs34\\c&H00D0EBFF&}When holidays felt truly magical\n")

    # Line 1: Have yourself a merry little Christmas (1.48s -> 9.50s)
    l1 = [
        ("Have", 1.48, 2.88),
        ("yourself", 2.88, 3.92),
        ("a", 3.92, 4.96),
        ("merry", 4.96, 5.80),
        ("little", 5.80, 7.00),
        ("Christmas,", 7.00, 9.50)
    ]
    for cur in l1:
        s_str = sec_to_ass(cur[1])
        e_str = sec_to_ass(cur[2])
        words_fmt = []
        for w in l1:
            if w == cur:
                words_fmt.append(f"{{\\c&H0027E2FE&\\3c&H000E6E9C&}}{w[0]}{{\\c&H00F5FAFF&\\3c&H00000000&}}")
            else:
                words_fmt.append(w[0])
        events.append(f"Dialogue: 1,{s_str},{e_str},SubtitleNormal,,0,0,0,,{' '.join(words_fmt)}\n")

    # Line 2: Let your heart be light (10.30s -> 14.50s)
    l2 = [
        ("Let", 10.30, 10.88),
        ("your", 10.88, 11.50),
        ("heart", 11.50, 12.30),
        ("be", 12.30, 12.80),
        ("light,", 12.80, 14.50)
    ]
    for cur in l2:
        s_str = sec_to_ass(cur[1])
        e_str = sec_to_ass(cur[2])
        words_fmt = []
        for w in l2:
            if w == cur:
                words_fmt.append(f"{{\\c&H0027E2FE&\\3c&H000E6E9C&}}{w[0]}{{\\c&H00F5FAFF&\\3c&H00000000&}}")
            else:
                words_fmt.append(w[0])
        events.append(f"Dialogue: 1,{s_str},{e_str},SubtitleNormal,,0,0,0,,{' '.join(words_fmt)}\n")

    # Line 3: From now on our troubles will be out of sight (14.88s -> 24.50s)
    l3 = [
        ("From", 14.88, 15.32),
        ("now", 15.32, 16.04),
        ("on", 16.04, 16.58),
        ("our", 16.58, 17.20),
        ("troubles", 17.20, 18.14),
        ("will", 18.14, 18.98),
        ("be", 18.98, 19.56),
        ("out", 19.56, 20.38),
        ("of", 20.38, 21.34),
        ("sight,", 21.34, 24.50)
    ]
    for cur in l3:
        s_str = sec_to_ass(cur[1])
        e_str = sec_to_ass(cur[2])
        words_fmt = []
        for w in l3:
            if w == cur:
                words_fmt.append(f"{{\\c&H0027E2FE&\\3c&H000E6E9C&}}{w[0]}{{\\c&H00F5FAFF&\\3c&H00000000&}}")
            else:
                words_fmt.append(w[0])
        line_rendered = " ".join(words_fmt[:5]) + "\\N" + " ".join(words_fmt[5:])
        events.append(f"Dialogue: 1,{s_str},{e_str},SubtitleNormal,,0,0,0,,{line_rendered}\n")

    # Line 4: Have yourself a merry little Christmas... (25.50s -> 34.00s)
    l4 = [
        ("Have", 25.50, 27.50),
        ("yourself", 27.50, 29.50),
        ("a", 29.50, 30.50),
        ("merry", 30.50, 31.50),
        ("little", 31.50, 32.20),
        ("Christmas...", 32.20, 34.00)
    ]
    for cur in l4:
        s_str = sec_to_ass(cur[1])
        e_str = sec_to_ass(cur[2])
        words_fmt = []
        for w in l4:
            if w == cur:
                words_fmt.append(f"{{\\c&H0027E2FE&\\3c&H000E6E9C&}}{w[0]}{{\\c&H00F5FAFF&\\3c&H00000000&}}")
            else:
                words_fmt.append(w[0])
        events.append(f"Dialogue: 1,{s_str},{e_str},SubtitleNormal,,0,0,0,,{' '.join(words_fmt)}\n")

    # Bottom Funnel CTA (16.0s -> 34.0s)
    events.append("Dialogue: 2,0:00:16.00,0:00:34.00,FunnelCTA,,0,0,0,,{\\fad(400,0)}🎄 FULL 100-MIN PLAYLIST LINKED BELOW ⬇\\N{\\fs32\\c&H00FFFFFF&}Tap Related Video link right under this short ⤵\n")

    with open(ass_path, "w", encoding="utf-8") as f:
        f.write(header + "".join(events))
    print(f"[+] Subtitle file created: {ass_path}")

def write_ass_short_2(ass_path: str):
    header = """[Script Info]
Title: Christmas Short 2
ScriptType: v4.00+
WrapStyle: 0
ScaledBorderAndShadow: yes
PlayResX: 1080
PlayResY: 1920

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: TitleBadge,Georgia,46,&H00FFFFFF,&H0000FFFF,&H00000000,&H90000000,-1,0,0,0,100,100,1,0,1,5,3,8,30,30,220,1
Style: SubtitleNormal,Georgia,54,&H00F5FAFF,&H0000FFFF,&H00000000,&HA0000000,-1,0,0,0,100,100,1,0,1,6,4,2,40,40,680,1
Style: FunnelCTA,Montserrat Black,40,&H0015E8FF,&H0000FFFF,&H00000000,&HA0000000,-1,0,0,0,100,100,1,0,1,5,3,2,30,30,320,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    events = []
    # Badge (Top)
    events.append("Dialogue: 0,0:00:00.00,0:00:42.00,TitleBadge,,0,0,0,,{\\fad(400,400)}🔔 TRADITIONAL CHRISTMAS CAROL 🔔\\N{\\fs34\\c&H00D0EBFF&}The most peaceful carol ever written\n")

    # Line 1: Silent night, holy night (0.68s -> 9.50s)
    l1 = [
        ("Silent", 0.68, 2.08),
        ("night,", 2.08, 4.72),
        ("holy", 6.06, 6.88),
        ("night,", 6.88, 9.50)
    ]
    for cur in l1:
        s_str = sec_to_ass(cur[1])
        e_str = sec_to_ass(cur[2])
        words_fmt = []
        for w in l1:
            if w == cur:
                words_fmt.append(f"{{\\c&H0027E2FE&\\3c&H000E6E9C&}}{w[0]}{{\\c&H00F5FAFF&\\3c&H00000000&}}")
            else:
                words_fmt.append(w[0])
        events.append(f"Dialogue: 1,{s_str},{e_str},SubtitleNormal,,0,0,0,,{' '.join(words_fmt)}\n")

    # Line 2: All is calm, all is bright (10.20s -> 17.00s)
    l2 = [
        ("All", 10.20, 10.62),
        ("is", 10.62, 11.46),
        ("calm,", 11.46, 13.36),
        ("all", 14.76, 14.78),
        ("is", 14.78, 15.48),
        ("bright.", 15.48, 17.00)
    ]
    for cur in l2:
        s_str = sec_to_ass(cur[1])
        e_str = sec_to_ass(cur[2])
        words_fmt = []
        for w in l2:
            if w == cur:
                words_fmt.append(f"{{\\c&H0027E2FE&\\3c&H000E6E9C&}}{w[0]}{{\\c&H00F5FAFF&\\3c&H00000000&}}")
            else:
                words_fmt.append(w[0])
        events.append(f"Dialogue: 1,{s_str},{e_str},SubtitleNormal,,0,0,0,,{' '.join(words_fmt)}\n")

    # Line 3: Round yon Virgin, Mother and Child (17.50s -> 26.50s)
    l3 = [
        ("Round", 17.50, 18.78),
        ("yon", 18.78, 19.88),
        ("Virgin,", 19.88, 21.34),
        ("Mother", 21.34, 22.74),
        ("and", 22.74, 23.90),
        ("Child,", 23.90, 26.50)
    ]
    for cur in l3:
        s_str = sec_to_ass(cur[1])
        e_str = sec_to_ass(cur[2])
        words_fmt = []
        for w in l3:
            if w == cur:
                words_fmt.append(f"{{\\c&H0027E2FE&\\3c&H000E6E9C&}}{w[0]}{{\\c&H00F5FAFF&\\3c&H00000000&}}")
            else:
                words_fmt.append(w[0])
        events.append(f"Dialogue: 1,{s_str},{e_str},SubtitleNormal,,0,0,0,,{' '.join(words_fmt)}\n")

    # Line 4: Holy Infant so tender and mild (27.00s -> 34.00s)
    l4 = [
        ("Holy", 27.00, 27.10),
        ("Infant", 27.10, 28.76),
        ("so", 28.76, 30.10),
        ("tender", 30.10, 30.94),
        ("and", 30.94, 32.34),
        ("mild,", 32.34, 34.00)
    ]
    for cur in l4:
        s_str = sec_to_ass(cur[1])
        e_str = sec_to_ass(cur[2])
        words_fmt = []
        for w in l4:
            if w == cur:
                words_fmt.append(f"{{\\c&H0027E2FE&\\3c&H000E6E9C&}}{w[0]}{{\\c&H00F5FAFF&\\3c&H00000000&}}")
            else:
                words_fmt.append(w[0])
        events.append(f"Dialogue: 1,{s_str},{e_str},SubtitleNormal,,0,0,0,,{' '.join(words_fmt)}\n")

    # Line 5: Sleep in heavenly peace... (34.00s -> 42.00s)
    l5 = [
        ("Sleep", 34.00, 35.98),
        ("in", 35.98, 36.62),
        ("heavenly", 36.62, 38.12),
        ("peace...", 38.12, 42.00)
    ]
    for cur in l5:
        s_str = sec_to_ass(cur[1])
        e_str = sec_to_ass(cur[2])
        words_fmt = []
        for w in l5:
            if w == cur:
                words_fmt.append(f"{{\\c&H0027E2FE&\\3c&H000E6E9C&}}{w[0]}{{\\c&H00F5FAFF&\\3c&H00000000&}}")
            else:
                words_fmt.append(w[0])
        events.append(f"Dialogue: 1,{s_str},{e_str},SubtitleNormal,,0,0,0,,{' '.join(words_fmt)}\n")

    # Bottom Funnel CTA (18.0s -> 42.0s)
    events.append("Dialogue: 2,0:00:18.00,0:00:42.00,FunnelCTA,,0,0,0,,{\\fad(400,0)}🕊️ FULL PEACEFUL CAROLS LINKED BELOW ⬇\\N{\\fs32\\c&H00FFFFFF&}Tap Related Video link right under this short ⤵\n")

    with open(ass_path, "w", encoding="utf-8") as f:
        f.write(header + "".join(events))
    print(f"[+] Subtitle file created: {ass_path}")

def render_short_1() -> str:
    print("\n================ RENDER SHORT 1 ================")
    ass_path = "outputs/christmas_shorts/short1.ass"
    write_ass_short_1(ass_path)

    audio_src = "D:/MUSIC/YOUTUBE/LIST BAI/CLASSIC ORIGIN/Have Yourself A Merry Little Christmas  .mp3"
    clip1 = "D:/MUSIC/YOUTUBE/VID NỀN/moi/Christmas_30s_23_Turntable.mp4"
    clip2 = "D:/MUSIC/YOUTUBE/VID NỀN/moi/Christmas_30s_01_FireplaceMantle.mp4"
    out_mp4 = "outputs/christmas_shorts/short_1_vintage_christmas.mp4"

    # 34.0 seconds total: clip 1 takes 17.0s, clip 2 takes 17.0s
    cmd = [
        "ffmpeg", "-y",
        "-ss", "12.0", "-t", "34.0", "-i", audio_src,
        "-ss", "0.0", "-t", "17.0", "-i", clip1,
        "-ss", "0.0", "-t", "17.0", "-i", clip2,
        "-filter_complex",
        "[1:v][2:v]concat=n=2:v=1:a=0[v_raw];"
        "[v_raw]split=2[v_bg_in][v_fg_in];"
        "[v_bg_in]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=25:5,eq=brightness=-0.08:contrast=1.05:saturation=1.2[bg];"
        "[v_fg_in]scale=1040:-1,pad=1056:594:8:4:color=0xD4AF37@0.8[fg];"
        "[bg][fg]overlay=(W-w)/2:520[v_comp];"
        f"[v_comp]ass={ass_path}[v];"
        "[0:a]afade=t=in:ss=0:d=1.0,afade=t=out:st=32.5:d=1.5[a]",
        "-map", "[v]", "-map", "[a]",
        "-c:v", "libx264", "-preset", "medium", "-crf", "18",
        "-c:a", "aac", "-b:a", "320k",
        "-shortest",
        out_mp4
    ]
    print("[*] Running FFmpeg rendering for Short 1...")
    t0 = time.time()
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print("FFmpeg Error:\n", res.stderr[-800:])
        raise RuntimeError("Render Short 1 failed")
    print(f"[+] Render Short 1 completed in {time.time() - t0:.1f}s. Size: {os.path.getsize(out_mp4)/1024/1024:.2f} MB")
    return out_mp4

def render_short_2() -> str:
    print("\n================ RENDER SHORT 2 ================")
    ass_path = "outputs/christmas_shorts/short2.ass"
    write_ass_short_2(ass_path)

    audio_src = "D:/MUSIC/YOUTUBE/LIST BAI/CLASSIC ORIGIN/Silent Night - Male Voice.mp3"
    clip1 = "D:/MUSIC/YOUTUBE/VID NỀN/moi/Christmas_30s_11_CathedralCandle.mp4"
    clip2 = "D:/MUSIC/YOUTUBE/VID NỀN/moi/Christmas_30s_24_Carolers.mp4"
    out_mp4 = "outputs/christmas_shorts/short_2_silent_night.mp4"

    # 42.0 seconds total: clip 1 takes 21.0s, clip 2 takes 21.0s
    cmd = [
        "ffmpeg", "-y",
        "-ss", "7.5", "-t", "42.0", "-i", audio_src,
        "-ss", "0.0", "-t", "21.0", "-i", clip1,
        "-ss", "0.0", "-t", "21.0", "-i", clip2,
        "-filter_complex",
        "[1:v][2:v]concat=n=2:v=1:a=0[v_raw];"
        "[v_raw]split=2[v_bg_in][v_fg_in];"
        "[v_bg_in]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=25:5,eq=brightness=-0.08:contrast=1.05:saturation=1.2[bg];"
        "[v_fg_in]scale=1040:-1,pad=1056:594:8:4:color=0xD4AF37@0.8[fg];"
        "[bg][fg]overlay=(W-w)/2:520[v_comp];"
        f"[v_comp]ass={ass_path}[v];"
        "[0:a]afade=t=in:ss=0:d=1.0,afade=t=out:st=40.5:d=1.5[a]",
        "-map", "[v]", "-map", "[a]",
        "-c:v", "libx264", "-preset", "medium", "-crf", "18",
        "-c:a", "aac", "-b:a", "320k",
        "-shortest",
        out_mp4
    ]
    print("[*] Running FFmpeg rendering for Short 2...")
    t0 = time.time()
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print("FFmpeg Error:\n", res.stderr[-800:])
        raise RuntimeError("Render Short 2 failed")
    print(f"[+] Render Short 2 completed in {time.time() - t0:.1f}s. Size: {os.path.getsize(out_mp4)/1024/1024:.2f} MB")
    return out_mp4

def upload_short_and_pin_comment(video_path: str, title: str, description: str, tags: list, pinned_comment: str) -> dict:
    with open('config/tokens/token_channel_2.json', 'r', encoding='utf-8') as f:
        info = json.load(f)
    creds = Credentials.from_authorized_user_info(info)
    yt = build('youtube', 'v3', credentials=creds)

    body = {
        'snippet': {
            'title': title,
            'description': description,
            'tags': tags,
            'categoryId': '10' # Music
        },
        'status': {
            'privacyStatus': 'public',
            'selfDeclaredMadeForKids': False
        }
    }

    print(f"[*] Uploading {os.path.basename(video_path)} to Channel 2...")
    media = MediaFileUpload(video_path, chunksize=-1, resumable=True, mimetype='video/mp4')
    req = yt.videos().insert(part='snippet,status', body=body, media_body=media)
    resp = req.execute()
    video_id = resp['id']
    short_url = f"https://youtube.com/shorts/{video_id}"
    print(f"[+] Uploaded successfully! Video ID: {video_id} -> {short_url}")

    # Post comment
    try:
        comment_body = {
            'snippet': {
                'videoId': video_id,
                'topLevelComment': {
                    'snippet': {
                        'textOriginal': pinned_comment
                    }
                }
            }
        }
        comment_res = yt.commentThreads().insert(part='snippet', body=comment_body).execute()
        comment_id = comment_res['id']
        print(f"[+] Pinned comment created: {comment_id}")
    except Exception as e:
        print(f"[!] Warning: Could not post comment automatically: {e}")

    return {
        'id': video_id,
        'url': short_url,
        'title': title
    }

if __name__ == '__main__':
    v1 = render_short_1()
    v2 = render_short_2()
    print("\nAll videos rendered successfully! Ready for upload.")
