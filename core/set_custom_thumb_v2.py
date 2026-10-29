import os
import sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

sys.path.insert(0, "d:/KENH GEHIHI")

from core.proxy_manager import get_proxy_youtube_client
from googleapiclient.http import MediaFileUpload

OUT_DIR = "d:/KENH GEHIHI/outputs/channel_3/video_2"
os.makedirs(OUT_DIR, exist_ok=True)
THUMB_PATH = os.path.join(OUT_DIR, "thumbnail.jpg")

# 1. Base Image: scene_5 (Dramatic Roman statue in shadow)
bg_path = "d:/KENH GEHIHI/outputs/channel_3/video_1/visuals/scene_5.jpg"
im = Image.open(bg_path).convert("RGB")

target_w, target_h = 1280, 720
im = im.resize((target_w, target_h), Image.Resampling.LANCZOS)

# 2. Cinematic Contrast & Color Grading
enhancer = ImageEnhance.Contrast(im)
im = enhancer.enhance(1.25)
enhancer = ImageEnhance.Brightness(im)
im = enhancer.enhance(0.9)

# 3. Vignette overlay for text legibility
overlay = Image.new("RGBA", (target_w, target_h), (0, 0, 0, 0))
odraw = ImageDraw.Draw(overlay)

# Heavy left gradient (covers 65% of screen width)
for x in range(850):
    alpha = int(240 * (1 - (x / 850) ** 1.2))
    odraw.line([(x, 0), (x, target_h)], fill=(5, 8, 15, alpha))

# Bottom subtle gradient
for y in range(450, target_h):
    alpha = int(180 * ((y - 450) / 270) ** 1.3)
    odraw.line([(0, y), (target_w, y)], fill=(5, 5, 10, alpha))

im.paste(overlay, (0, 0), overlay)
draw = ImageDraw.Draw(im)

# 4. Fonts
font_path_main = "d:/KENH GEHIHI/assets/fonts/Montserrat-Black.ttf"
font_path_serif = "C:/Windows/Fonts/georgiab.ttf"

font_badge = ImageFont.truetype(font_path_main, 24)
font_large = ImageFont.truetype(font_path_main, 76)
font_highlight = ImageFont.truetype(font_path_main, 84)
font_sub = ImageFont.truetype(font_path_serif, 38)

# 5. Badge: "★ STOIC MASTERY ★"
bx, by = 60, 100
bw, bh = 290, 48
draw.rounded_rectangle([(bx, by), (bx + bw, by + bh)], radius=8, fill=(160, 20, 30), outline=(255, 215, 0), width=2)
draw.text((bx + bw // 2, by + bh // 2), "★ STOIC MASTERY ★", fill=(255, 255, 255), font=font_badge, anchor="mm")

# 6. Main Headline with 3D drop shadow
# Line 1: "BECOME"
x1, y1 = 60, 180
# Shadow
for dx, dy in [(4, 4), (5, 5), (6, 6)]:
    draw.text((x1 + dx, y1 + dy), "BECOME", fill=(0, 0, 0), font=font_large)
draw.text((x1, y1), "BECOME", fill=(255, 255, 255), font=font_large)

# Line 2: "UNTOUCHABLE" (Cyan / Gold Glow)
x2, y2 = 60, 265
for dx, dy in [(4, 4), (5, 5), (6, 6), (7, 7)]:
    draw.text((x2 + dx, y2 + dy), "UNTOUCHABLE", fill=(0, 0, 0), font=font_highlight)
draw.text((x2, y2), "UNTOUCHABLE", fill=(21, 232, 255), font=font_highlight)

# Line 3: "7 RULES OF QUIET STRENGTH"
x3, y3 = 60, 390
draw.text((x3 + 3, y3 + 3), "7 Rules of Quiet Strength", fill=(0, 0, 0), font=font_sub)
draw.text((x3, y3), "7 Rules of Quiet Strength", fill=(255, 215, 100), font=font_sub)

# Save
im.save(THUMB_PATH, "JPEG", quality=95)
print(f"[+] Custom Thumbnail saved to: {THUMB_PATH}")

# 7. Upload to Video 2 on YouTube
VIDEO_ID = "8nHOW4XTU6w"
print(f"[*] Uploading unique thumbnail to Video {VIDEO_ID} on Channel 3...")
yt = get_proxy_youtube_client("channel_3")
media = MediaFileUpload(THUMB_PATH, mimetype="image/jpeg")
yt.thumbnails().set(videoId=VIDEO_ID, media_body=media).execute()
print(f"[SUCCESS] Custom Thumbnail set for {VIDEO_ID}!")
