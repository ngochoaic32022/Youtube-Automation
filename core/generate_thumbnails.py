import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

out_dir = "d:/KENH GEHIHI/outputs/thumbnails"
os.makedirs(out_dir, exist_ok=True)

def create_vintage_thumbnail_1(bg_path, output_path):
    """
    Thumbnail for Video 1: 1950s Vintage Christmas Songs (100 Mins)
    Target size: 1280x720
    """
    im = Image.open(bg_path).convert("RGB")
    # Resize & crop to 1280x720
    target_w, target_h = 1280, 720
    im = im.resize((target_w, target_h), Image.Resampling.LANCZOS)
    
    # Warm color grading & contrast boost for punchy display
    enhancer = ImageEnhance.Color(im)
    im = enhancer.enhance(1.25)
    enhancer = ImageEnhance.Contrast(im)
    im = enhancer.enhance(1.15)

    # Dark gradient overlay on the left side to make text pop
    overlay = Image.new("RGBA", (target_w, target_h), (0, 0, 0, 0))
    odraw = ImageDraw.Draw(overlay)
    
    # Left vignette gradient
    for x in range(750):
        alpha = int(220 * (1 - x / 750) ** 1.3)
        odraw.line([(x, 0), (x, target_h)], fill=(12, 10, 18, alpha))
        
    # Bottom vignette gradient
    for y in range(450, target_h):
        alpha = int(180 * ((y - 450) / 270) ** 1.2)
        odraw.line([(0, y), (target_w, y)], fill=(10, 8, 15, alpha))

    im.paste(overlay, (0, 0), overlay)
    draw = ImageDraw.Draw(im)

    # Fonts
    font_main = ImageFont.truetype("C:/Windows/Fonts/georgiab.ttf", 64)
    font_sub = ImageFont.truetype("d:/KENH GEHIHI/assets/fonts/Montserrat-Black.ttf", 36)
    font_badge = ImageFont.truetype("d:/KENH GEHIHI/assets/fonts/Montserrat-Black.ttf", 24)

    # Badge: "1950s NOSTALGIA"
    badge_x, badge_y = 60, 110
    odraw = ImageDraw.Draw(im)
    draw.rounded_rectangle([(badge_x, badge_y), (badge_x + 290, badge_y + 46)], radius=8, fill=(190, 30, 45), outline=(255, 200, 100), width=2)
    draw.text((badge_x + 145, badge_y + 23), "★ 1950s VINTAGE ★", fill=(255, 255, 255), font=font_badge, anchor="mm")

    # Main Title: "VINTAGE\nCHRISTMAS"
    title_text = "VINTAGE\nCHRISTMAS"
    # Shadow
    draw.text((63, 183), title_text, fill=(0, 0, 0), font=font_main, spacing=10)
    draw.text((60, 180), title_text, fill=(255, 225, 150), font=font_main, spacing=10)

    # Subtitle: "COZY HOLIDAY RADIO"
    draw.text((62, 362), "COZY HOLIDAY PLAYLIST", fill=(0, 0, 0), font=font_sub)
    draw.text((60, 360), "COZY HOLIDAY PLAYLIST", fill=(255, 255, 255), font=font_sub)

    # Highlight Pill: "100 MINS • FIREPLACE SOUNDS"
    draw.rounded_rectangle([(60, 440), (450, 495)], radius=10, fill=(20, 60, 35, 220), outline=(100, 220, 140), width=2)
    draw.text((255, 467), "100 MINS • FIREPLACE", fill=(255, 255, 255), font=font_badge, anchor="mm")

    im.save(output_path, "JPEG", quality=95)
    print(f"Generated {output_path}")

def create_vintage_thumbnail_2(bg_path, output_path):
    """
    Thumbnail for Video 2: Traditional Christmas Carols (Silent Night, Joy to the World)
    Target size: 1280x720
    """
    im = Image.open(bg_path).convert("RGB")
    target_w, target_h = 1280, 720
    im = im.resize((target_w, target_h), Image.Resampling.LANCZOS)
    
    enhancer = ImageEnhance.Color(im)
    im = enhancer.enhance(1.3)
    enhancer = ImageEnhance.Contrast(im)
    im = enhancer.enhance(1.18)

    overlay = Image.new("RGBA", (target_w, target_h), (0, 0, 0, 0))
    odraw = ImageDraw.Draw(overlay)
    
    # Left vignette
    for x in range(750):
        alpha = int(230 * (1 - x / 750) ** 1.3)
        odraw.line([(x, 0), (x, target_h)], fill=(12, 10, 18, alpha))
        
    for y in range(450, target_h):
        alpha = int(180 * ((y - 450) / 270) ** 1.2)
        odraw.line([(0, y), (target_w, y)], fill=(10, 8, 15, alpha))

    im.paste(overlay, (0, 0), overlay)
    draw = ImageDraw.Draw(im)

    font_main = ImageFont.truetype("C:/Windows/Fonts/georgiab.ttf", 62)
    font_sub = ImageFont.truetype("d:/KENH GEHIHI/assets/fonts/Montserrat-Black.ttf", 36)
    font_badge = ImageFont.truetype("d:/KENH GEHIHI/assets/fonts/Montserrat-Black.ttf", 24)

    # Badge: "TIMELESS CAROLS"
    badge_x, badge_y = 60, 110
    draw.rounded_rectangle([(badge_x, badge_y), (badge_x + 310, badge_y + 46)], radius=8, fill=(180, 25, 40), outline=(255, 215, 110), width=2)
    draw.text((badge_x + 155, badge_y + 23), "🔔 GOLDEN ERA CAROLS", fill=(255, 255, 255), font=font_badge, anchor="mm")

    # Main Title: "TRADITIONAL\nCHRISTMAS"
    title_text = "TRADITIONAL\nCHRISTMAS"
    draw.text((63, 183), title_text, fill=(0, 0, 0), font=font_main, spacing=10)
    draw.text((60, 180), title_text, fill=(255, 230, 150), font=font_main, spacing=10)

    # Subtitle: "PEACEFUL & WARM"
    draw.text((62, 362), "SILENT NIGHT • JOY TO WORLD", fill=(0, 0, 0), font=font_sub)
    draw.text((60, 360), "SILENT NIGHT • JOY TO WORLD", fill=(255, 255, 255), font=font_sub)

    # Highlight Pill: "RELAXING ACOUSTIC"
    draw.rounded_rectangle([(60, 440), (450, 495)], radius=10, fill=(20, 50, 75, 220), outline=(120, 200, 255), width=2)
    draw.text((255, 467), "PEACEFUL ACOUSTIC CAROLS", fill=(255, 255, 255), font=font_badge, anchor="mm")

    im.save(output_path, "JPEG", quality=95)
    print(f"Generated {output_path}")

if __name__ == "__main__":
    t1 = "d:/KENH GEHIHI/outputs/thumbnails/thumb_video_1.jpg"
    t2 = "d:/KENH GEHIHI/outputs/thumbnails/thumb_video_2.jpg"
    create_vintage_thumbnail_1("d:/KENH GEHIHI/outputs/thumbnails/thumb_raw_1.jpg", t1)
    create_vintage_thumbnail_2("d:/KENH GEHIHI/outputs/thumbnails/thumb_raw_2.jpg", t2)
