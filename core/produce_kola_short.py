import os
import sys
import json
import time
import asyncio
import subprocess
import urllib.request
from datetime import datetime

sys.path.insert(0, "d:/KENH GEHIHI")

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

OUT_DIR = "d:/KENH GEHIHI/outputs/video_6_kola"
os.makedirs(OUT_DIR, exist_ok=True)

SCENES = [
    {
        "sentence": "Năm 1970, Liên Xô đã cố gắng đào một cái hố sâu nhất hành tinh để xuyên thủng vỏ Trái Đất, đó chính là Siêu hố khoan Kola.",
        "url": "https://images.unsplash.com/photo-1578328819058-b69f3a3b0f6b?w=1080&q=80",
        "desc": "Tháp khoan công nghiệp khổng lồ giữa vùng băng giá"
    },
    {
        "sentence": "Họ mất gần 20 năm để khoan sâu tới 12.262 mét, tương đương chiều cao của 30 tòa nhà chọc trời cộng lại.",
        "url": "https://images.unsplash.com/photo-1509198397868-475647b2a1e5?w=1080&q=80",
        "desc": "Hố sâu hun hút đâm thẳng vào lòng đất"
    },
    {
        "sentence": "Nhưng ở độ sâu nghẹt thở này, nhiệt độ tăng vọt lên tới 180 độ C, khiến mũi khoan hợp kim cứng nhất cũng bị biến dạng và tan chảy như sáp.",
        "url": "https://images.unsplash.com/photo-1508873696983-2df57036476b?w=1080&q=80",
        "desc": "Nham thạch rực đỏ và kim loại nóng chảy trong lòng đất"
    },
    {
        "sentence": "Kỳ bí hơn, các micro địa chấn thả xuống đáy hố đã thu lại những âm thanh gầm rú ma quái, khiến toàn bộ dự án bị đóng cửa và hàn kín vĩnh viễn.",
        "url": "https://images.unsplash.com/photo-1518709268805-4e9042af9f23?w=1080&q=80",
        "desc": "Sóng âm địa chấn và bóng tối rùng mình"
    },
    {
        "sentence": "Bạn có tin Trái Đất còn ẩn giấu những bí mật không tưởng? Bấm đăng ký kênh Kỳ Thú Khám Phá để cùng giải mã nhé!",
        "url": "https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=1080&q=80",
        "desc": "Lõi Trái Đất rực sáng giữa vũ trụ"
    }
]

async def main():
    print("=" * 70)
    print("🚨 SẢN XUẤT CẤP TỐC VIDEO KHUNG TRƯA (11:30) CHO KÊNH 1 - PUBLIC NGAY")
    print("=" * 70)

    # 1. Download visuals
    image_paths = []
    for idx, sc in enumerate(SCENES, 1):
        img_path = f"{OUT_DIR}/scene_{idx}.jpg"
        if not os.path.exists(img_path):
            print(f"  [+] Tải ảnh cảnh {idx}: {sc['desc'][:40]}...")
            req = urllib.request.Request(sc["url"], headers={"User-Agent": "Mozilla/5.0"})
            try:
                with urllib.request.urlopen(req, timeout=12) as resp:
                    with open(img_path, "wb") as f:
                        f.write(resp.read())
            except Exception as e:
                print(f"      Lỗi {e}, dùng ảnh fallback...")
                import shutil
                fallback = f"d:/KENH GEHIHI/outputs/video_3/scene_{min(idx, 5)}.jpg"
                shutil.copy2(fallback, img_path)
        image_paths.append(img_path)

    # 2. TTS Voiceover
    print("  [+] Tạo giọng đọc Nam Minh AI...")
    full_script = " ".join([s["sentence"] for s in SCENES])
    tts = TTSEngine(voice="vi-VN-NamMinhNeural")
    voice_audio = f"{OUT_DIR}/voice.mp3"
    raw_srt = f"{OUT_DIR}/voice.srt"
    dur = await tts.generate_speech(full_script, voice_audio, raw_srt)
    print(f"      Thời lượng: {dur:.2f}s")

    # 3. Clean ASS Subtitle
    print("  [+] Đồng bộ phụ đề typography Montserrat Black...")
    ass_path = f"{OUT_DIR}/subtitles.ass"
    sentence_durs = [dur / len(SCENES)] * len(SCENES)
    build_perfect_subtitles(SCENES, sentence_durs, ass_path, is_shorts=True)

    # 4. Render Video
    print("  [+] Render video Ken Burns 1080x1920...")
    final_video = f"{OUT_DIR}/final_video.mp4"
    renderer = VideoRenderer(width=1080, height=1920, fps=30)
    renderer.render(
        image_paths=image_paths,
        voice_audio_path=voice_audio,
        output_video_path=final_video,
        subtitle_path=ass_path,
        bg_music_path="d:/KENH GEHIHI/assets/music/deep_ocean_drone.mp3",
        music_volume=0.16
    )
    print(f"  -> Video sẵn sàng: {final_video}")

    # 5. Upload PUBLIC Ngay Lập Tức
    print("  [+] Đang đăng tải PUBLIC ngay lập tức lên YouTube Kênh 1...")
    uploader = YouTubeUploader("channel_1")
    title = "Hố Khoan Kola: Tại Sao Nhân Loại Không Thể Đào Xuyên Trái Đất? 😱 #shorts"
    desc = """Năm 1970, Liên Xô đã đào cái hố sâu nhất hành tinh: Siêu hố khoan Kola sâu 12.262m. Tại sao dự án buộc phải hàn kín vĩnh viễn?

⏱️ TIMESTAMPS:
00:00 - Siêu hố khoan sâu nhất Trái Đất
00:07 - Chiều sâu nghẹt thở 12.262 mét
00:15 - Nhiệt độ nung chảy mũi khoan
00:23 - Âm thanh ma quái dưới lòng đất
00:30 - Bí mật bị niêm phong vĩnh cửu

🔔 Đăng ký kênh Kỳ Thú Khám Phá đón xem 2 video mỗi ngày vào lúc 11:30 và 18:45!

#shorts #hokhoankola #kola #khoahoc #khampha #bian #traidat #diachat #rungkinh
"""
    tags = ["hố khoan kola", "kola superdeep borehole", "đào xuyên trái đất", "khoa học bí ẩn", "âm thanh địa ngục kola", "kỳ thú khám phá", "shorts"]

    vid = uploader.upload_video(
        video_file_path=final_video,
        title=title,
        description=desc,
        tags=tags,
        category_id="27",
        privacy_status="public"
    )
    print(f"\n🎉 [THÀNH CÔNG] Video ca trưa đã PUBLIC: https://youtu.be/{vid}")
    return vid

if __name__ == "__main__":
    asyncio.run(main())
