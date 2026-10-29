import os
from PIL import Image, ImageDraw, ImageFont, ImageEnhance

out_dir = "d:/KENH GEHIHI/outputs/thumbnails"

def render_refined_1():
    src = f"{out_dir}/raw_ai_thumb_1.jpg"
    dst = f"{out_dir}/thumb_v1_refined.jpg"
    im = Image.open(src).convert("RGB")
    im = im.resize((1280, 720), Image.Resampling.LANCZOS)

    # Rich warm saturation and deep contrast
    im = ImageEnhance.Contrast(im).enhance(1.10)
    im = ImageEnhance.Color(im).enhance(1.15)

    # Subtle soft dark gradient in top-left to make serif text crystal clear
    overlay = Image.new("RGBA", (1280, 720), (0, 0, 0, 0))
    odraw = ImageDraw.Draw(overlay)
    for y in range(260):
        for x in range(600):
            dist = (x/600)**2 + (y/260)**2
            if dist < 1.0:
                alpha = int(140 * (1 - dist))
                overlay.putpixel((x, y), (5, 3, 10, alpha))
                
    im.paste(overlay, (0, 0), overlay)
    draw = ImageDraw.Draw(im)

    font_title = ImageFont.truetype("C:/Windows/Fonts/georgiab.ttf", 52)
    font_sub = ImageFont.truetype("d:/KENH GEHIHI/assets/fonts/Montserrat-Black.ttf", 24)

    # Luxury gold gradient simulation with drop shadow
    # Title: 1950s VINTAGE CHRISTMAS
    t_text = "1950s VINTAGE CHRISTMAS"
    draw.text((52, 62), t_text, fill=(0, 0, 0), font=font_title)
    draw.text((50, 60), t_text, fill=(255, 230, 160), font=font_title)

    # Sub: COZY FIREPLACE & NOSTALGIC RADIO • 100 MINS
    s_text = "COZY FIREPLACE & NOSTALGIC RADIO • 100 MINS"
    draw.text((52, 126), s_text, fill=(0, 0, 0), font=font_sub)
    draw.text((50, 124), s_text, fill=(255, 255, 255), font=font_sub)

    im.save(dst, "JPEG", quality=95)
    print(f"Refined 1: {dst}")

def render_refined_2():
    src = f"{out_dir}/raw_ai_thumb_2.jpg"
    dst = f"{out_dir}/thumb_v2_refined.jpg"
    im = Image.open(src).convert("RGB")
    im = im.resize((1280, 720), Image.Resampling.LANCZOS)

    im = ImageEnhance.Contrast(im).enhance(1.10)
    im = ImageEnhance.Color(im).enhance(1.15)

    overlay = Image.new("RGBA", (1280, 720), (0, 0, 0, 0))
    odraw = ImageDraw.Draw(overlay)
    for y in range(260):
        for x in range(650):
            dist = (x/650)**2 + (y/260)**2
            if dist < 1.0:
                alpha = int(140 * (1 - dist))
                overlay.putpixel((x, y), (5, 3, 10, alpha))
                
    im.paste(overlay, (0, 0), overlay)
    draw = ImageDraw.Draw(im)

    font_title = ImageFont.truetype("C:/Windows/Fonts/georgiab.ttf", 52)
    font_sub = ImageFont.truetype("d:/KENH GEHIHI/assets/fonts/Montserrat-Black.ttf", 24)

    # Title: TRADITIONAL CHRISTMAS CAROLS
    t_text = "TRADITIONAL CHRISTMAS CAROLS"
    draw.text((52, 62), t_text, fill=(0, 0, 0), font=font_title)
    draw.text((50, 60), t_text, fill=(255, 230, 160), font=font_title)

    # Sub: SILENT NIGHT, JOY TO THE WORLD & CLASSIC HYMNS
    s_text = "SILENT NIGHT, JOY TO THE WORLD & CLASSIC HYMNS"
    draw.text((52, 126), s_text, fill=(0, 0, 0), font=font_sub)
    draw.text((50, 124), s_text, fill=(255, 255, 255), font=font_sub)

    im.save(dst, "JPEG", quality=95)
    print(f"Refined 2: {dst}")

if __name__ == "__main__":
    render_refined_1()
    render_refined_2()
