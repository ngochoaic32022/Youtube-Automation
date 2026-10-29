import os
from PIL import Image, ImageDraw, ImageFont, ImageEnhance

out_dir = "d:/KENH GEHIHI/outputs/thumbnails"

def finish_thumbnail_1():
    src = f"{out_dir}/raw_ai_thumb_1.jpg"
    dst = f"{out_dir}/thumb_video_1.jpg"
    im = Image.open(src).convert("RGB")
    im = im.resize((1280, 720), Image.Resampling.LANCZOS)

    # Slight warmth and contrast punch
    im = ImageEnhance.Contrast(im).enhance(1.08)
    im = ImageEnhance.Color(im).enhance(1.12)

    # Subtle cinematic vignette in the upper left corner for text legibility
    overlay = Image.new("RGBA", (1280, 720), (0, 0, 0, 0))
    odraw = ImageDraw.Draw(overlay)
    
    # Left gradient
    for x in range(650):
        alpha = int(190 * (1 - x / 650) ** 1.4)
        odraw.line([(x, 0), (x, 720)], fill=(8, 6, 12, alpha))
        
    # Bottom gradient
    for y in range(500, 720):
        alpha = int(160 * ((y - 500) / 220) ** 1.3)
        odraw.line([(0, y), (1280, y)], fill=(8, 6, 12, alpha))

    im.paste(overlay, (0, 0), overlay)
    draw = ImageDraw.Draw(im)

    font_badge = ImageFont.truetype("d:/KENH GEHIHI/assets/fonts/Montserrat-Black.ttf", 22)
    font_title = ImageFont.truetype("C:/Windows/Fonts/georgiab.ttf", 60)
    font_sub = ImageFont.truetype("d:/KENH GEHIHI/assets/fonts/Montserrat-Black.ttf", 32)

    # 1. Festive Golden Badge
    bx, by = 60, 90
    draw.rounded_rectangle([(bx, by), (bx + 280, by + 44)], radius=8, fill=(180, 25, 35), outline=(255, 215, 120), width=2)
    draw.text((bx + 140, by + 22), "★ 1950s VINTAGE RADIO ★", fill=(255, 255, 255), font=font_badge, anchor="mm")

    # 2. Main Title with multi-layered deep drop shadow for legibility
    t_text = "VINTAGE\nCHRISTMAS"
    draw.text((64, 154), t_text, fill=(0, 0, 0), font=font_title, spacing=8)
    draw.text((62, 152), t_text, fill=(20, 10, 0), font=font_title, spacing=8)
    draw.text((60, 150), t_text, fill=(255, 230, 150), font=font_title, spacing=8)

    # 3. Subtitle
    draw.text((63, 313), "COZY FIREPLACE & CAROLS", fill=(0, 0, 0), font=font_sub)
    draw.text((60, 310), "COZY FIREPLACE & CAROLS", fill=(255, 255, 255), font=font_sub)

    # 4. Feature Pill
    draw.rounded_rectangle([(60, 385), (410, 435)], radius=10, fill=(15, 55, 30, 230), outline=(100, 220, 140), width=2)
    draw.text((235, 410), "100 MINS • PURE NOSTALGIA", fill=(255, 255, 255), font=font_badge, anchor="mm")

    im.save(dst, "JPEG", quality=95)
    print(f"Finished {dst}")

def finish_thumbnail_2():
    src = f"{out_dir}/raw_ai_thumb_2.jpg"
    dst = f"{out_dir}/thumb_video_2.jpg"
    im = Image.open(src).convert("RGB")
    im = im.resize((1280, 720), Image.Resampling.LANCZOS)

    im = ImageEnhance.Contrast(im).enhance(1.08)
    im = ImageEnhance.Color(im).enhance(1.15)

    overlay = Image.new("RGBA", (1280, 720), (0, 0, 0, 0))
    odraw = ImageDraw.Draw(overlay)
    
    # Left gradient
    for x in range(650):
        alpha = int(200 * (1 - x / 650) ** 1.4)
        odraw.line([(x, 0), (x, 720)], fill=(8, 6, 12, alpha))
        
    for y in range(500, 720):
        alpha = int(160 * ((y - 500) / 220) ** 1.3)
        odraw.line([(0, y), (1280, y)], fill=(8, 6, 12, alpha))

    im.paste(overlay, (0, 0), overlay)
    draw = ImageDraw.Draw(im)

    font_badge = ImageFont.truetype("d:/KENH GEHIHI/assets/fonts/Montserrat-Black.ttf", 22)
    font_title = ImageFont.truetype("C:/Windows/Fonts/georgiab.ttf", 58)
    font_sub = ImageFont.truetype("d:/KENH GEHIHI/assets/fonts/Montserrat-Black.ttf", 30)

    # 1. Festive Golden Badge
    bx, by = 60, 90
    draw.rounded_rectangle([(bx, by), (bx + 310, by + 44)], radius=8, fill=(180, 25, 35), outline=(255, 215, 120), width=2)
    draw.text((bx + 155, by + 22), "🔔 GOLDEN ERA CLASSICS", fill=(255, 255, 255), font=font_badge, anchor="mm")

    # 2. Main Title
    t_text = "TRADITIONAL\nCAROLS"
    draw.text((64, 154), t_text, fill=(0, 0, 0), font=font_title, spacing=8)
    draw.text((62, 152), t_text, fill=(20, 10, 0), font=font_title, spacing=8)
    draw.text((60, 150), t_text, fill=(255, 230, 150), font=font_title, spacing=8)

    # 3. Subtitle
    draw.text((63, 313), "SILENT NIGHT • JOY TO THE WORLD", fill=(0, 0, 0), font=font_sub)
    draw.text((60, 310), "SILENT NIGHT • JOY TO THE WORLD", fill=(255, 255, 255), font=font_sub)

    # 4. Feature Pill
    draw.rounded_rectangle([(60, 385), (420, 435)], radius=10, fill=(18, 45, 75, 230), outline=(120, 200, 255), width=2)
    draw.text((240, 410), "PEACEFUL ACOUSTIC & CHORAL", fill=(255, 255, 255), font=font_badge, anchor="mm")

    im.save(dst, "JPEG", quality=95)
    print(f"Finished {dst}")

if __name__ == "__main__":
    finish_thumbnail_1()
    finish_thumbnail_2()
