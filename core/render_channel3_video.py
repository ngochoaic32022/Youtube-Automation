import os
import sys
import subprocess
import time

sys.stdout.reconfigure(encoding='utf-8')

WORKDIR = "d:/KENH GEHIHI"
BASE_DIR = "outputs/channel_3/video_1"
AUDIO_PATH = os.path.join(WORKDIR, BASE_DIR, "master_audio.mp3")
ASS_PATH = f"{BASE_DIR}/subtitles_styled.ass"
OUT_VIDEO = os.path.join(WORKDIR, BASE_DIR, "master_video.mp4")
CONCAT_FILE = os.path.join(WORKDIR, BASE_DIR, "concat.txt")

# Get exact audio duration
cmd_probe = [
    "ffprobe", "-v", "error",
    "-show_entries", "format=duration",
    "-of", "default=noprint_wrappers=1:nokey=1",
    AUDIO_PATH
]
dur = float(subprocess.check_output(cmd_probe).strip())
print(f"[*] Audio Duration: {dur:.2f}s (~{dur/60:.1f} mins)")

# Build 14-shot sequence (scenes 1-7 twice)
shot_count = 14
shot_dur = dur / shot_count
print(f"[*] Each of 14 shots will play for {shot_dur:.2f}s")

with open(CONCAT_FILE, "w", encoding="utf-8") as f:
    for shot in range(shot_count):
        scene_idx = (shot % 7) + 1
        img_path = f"{WORKDIR}/{BASE_DIR}/visuals/scene_{scene_idx}.jpg".replace("\\", "/")
        f.write(f"file '{img_path}'\n")
        f.write(f"duration {shot_dur:.3f}\n")
    # Concat demuxer requirement: repeat last file once
    last_img = f"{WORKDIR}/{BASE_DIR}/visuals/scene_7.jpg".replace("\\", "/")
    f.write(f"file '{last_img}'\n")

print(f"[+] Concat list written to: {CONCAT_FILE}")

# FFmpeg render command
cmd_render = [
    "ffmpeg", "-y",
    "-f", "concat", "-safe", "0", "-i", CONCAT_FILE,
    "-i", AUDIO_PATH,
    "-filter_complex",
    f"[0:v]fps=25,scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,eq=brightness=0.01:contrast=1.06:saturation=1.12,ass={ASS_PATH}[v_out]",
    "-map", "[v_out]",
    "-map", "1:a",
    "-c:v", "libx264", "-preset", "fast", "-crf", "19", "-pix_fmt", "yuv420p",
    "-c:a", "aac", "-b:a", "320k",
    "-shortest",
    OUT_VIDEO
]

print("\n[*] Starting FFmpeg render...")
t0 = time.time()
p = subprocess.run(cmd_render, capture_output=True, text=True)
if p.returncode != 0:
    print("[!] Error:\n", p.stderr[-800:])
    sys.exit(1)

elapsed = time.time() - t0
sz_mb = os.path.getsize(OUT_VIDEO) / (1024 * 1024)
print(f"\n[SUCCESS] Rendered Master Video in {elapsed:.1f}s!")
print(f"[+] Output: {OUT_VIDEO} ({sz_mb:.2f} MB)")
