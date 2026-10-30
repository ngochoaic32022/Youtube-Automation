import os
import sys
import json
import time
import asyncio
import subprocess

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT_DIR)

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

import edge_tts
from core.clean_subtitle_builder import build_perfect_subtitles
from core.video_renderer import VideoRenderer
from core.youtube_uploader import YouTubeUploader
from core.veo_video_generator import VeoVideoGenerator

OUT_DIR = os.path.join(ROOT_DIR, "outputs", "video_7_saomoc")
os.makedirs(OUT_DIR, exist_ok=True)

SCENES = [
    {
        "sentence": "Bạn có biết, ngay lúc này, hàng ngàn thiên thạch khổng lồ đang lao vun vút trong không gian với vận tốc hơn 40.000 km một giờ?",
        "keyword": "asteroid flying in space",
        "fallback": "galaxy space universe"
    },
    {
        "sentence": "Nếu chỉ một tiểu hành tinh cỡ vài km đâm vào Trái Đất, năng lượng giải phóng sẽ tương đương với hàng triệu quả bom nguyên tử nổ cùng lúc!",
        "keyword": "huge explosion earth destruction",
        "fallback": "fire fiery magma explosion"
    },
    {
        "sentence": "Thế nhưng, chính lực hấp dẫn khổng lồ của Sao Mộc đã như một máy hút bụi vũ trụ, hút lệch hoặc nuốt chửng những quái vật không gian này.",
        "keyword": "planet jupiter space",
        "fallback": "planets solar system"
    },
    {
        "sentence": "Năm 1994, nhân loại từng chứng kiến sao chổi Shoemaker đâm thẳng vào Sao Mộc, để lại những vết sẹo to bằng cả Trái Đất.",
        "keyword": "comet space explosion",
        "fallback": "meteor impact universe"
    },
    {
        "sentence": "Chúng ta vẫn đang an toàn sống sót mỗi ngày nhờ sự che chở kỳ diệu của vũ trụ. Bấm đăng ký Kỳ Thú Khám Phá để khám phá thêm nhé!",
        "keyword": "earth rotating from space",
        "fallback": "beautiful planet earth"
    }
]

async def produce_and_upload():
    print("\n" + "=" * 75)
    print("🚀 SẢN XUẤT CẤP TỐC VIDEO CA TRƯA KÊNH 1 (KỲ THÚ KHÁM PHÁ)")
    print("   Chủ đề: Bí Ẩn Sao Mộc & Lá Chắn Hộ Mệnh Của Trái Đất")
    print("=" * 75)

    # 1. Sinh voice Nam Minh
    voice_file = os.path.join(OUT_DIR, "voice_saomoc.mp3")
    full_script = " ".join([s["sentence"] for s in SCENES])
    print(f"\n[1/5] 🎙️ Đang tạo giọng đọc AI Nam Minh (vi-VN-NamMinhNeural)...")
    comm = edge_tts.Communicate(full_script, "vi-VN-NamMinhNeural", rate="+4%")
    await comm.save(voice_file)

    renderer = VideoRenderer(width=1080, height=1920, fps=30)
    dur = renderer._get_audio_duration(voice_file)
    print(f"      Thời lượng giọng đọc: {dur:.2f}s")

    # 2. Thu thập clips chuyển động (Hybrid Dual-Engine: 1 Veo Hook + Free Pexels Stock HD)
    print(f"\n[2/5] 🎬 Đang thu thập các video chuyển động 9:16 (Hybrid Dual-Engine)...")
    veo_gen = VeoVideoGenerator()
    clips = veo_gen.fetch_hybrid_clips_for_shorts(
        scenes=SCENES,
        channel_id="channel_1",
        output_dir=OUT_DIR,
        veo_quota_per_video=1
    )

    if not clips:
        print("[!] Không có clips, kiểm tra lại nguồn cấp.")
        return

    # 3. Tạo phụ đề Karaoke động
    print(f"\n[3/5] ✍️ Tạo phụ đề Montserrat Black động nhấp nháy...")
    ass_file = os.path.join(OUT_DIR, "subtitles.ass")
    sentence_durs = [dur / len(SCENES)] * len(SCENES)
    build_perfect_subtitles(SCENES, sentence_durs, ass_file, is_shorts=True)

    # 4. Render video hoàn chỉnh
    print(f"\n[4/5] 🎞️ Đang render video hoàn chỉnh 1080x1920 Full HD...")
    final_video = os.path.join(OUT_DIR, "short_saomoc_master.mp4")
    bg_music = os.path.join(ROOT_DIR, "assets", "music", "deep_ocean_drone.mp3")
    if not os.path.exists(bg_music):
        bg_music = None

    renderer.render_from_video_clips(
        video_clip_paths=clips,
        voice_audio_path=voice_file,
        output_video_path=final_video,
        subtitle_path=ass_file,
        bg_music_path=bg_music,
        music_volume=0.12
    )

    print(f"      ✅ Render thành công: {final_video}")

    # 5. Đăng tải PUBLIC lên YouTube Kênh 1
    print(f"\n[5/5] 📡 Đang tải lên YouTube Kênh 1 (Kỳ Thú Khám Phá)...")
    uploader = YouTubeUploader("channel_1")
    title = "Nếu Không Có Sao Mộc, Trái Đất Đã Bị Hủy Diệt Từ Lâu? 😱 #shorts"
    desc = """Bí ẩn vũ trụ: Thứ gì đang âm thầm hoạt động như chiếc 'máy hút bụi vũ trụ', che chở cho sự sống trên Trái Đất suốt hàng tỷ năm qua?

⏱️ TIMESTAMPS:
00:00 - Quái vật không gian 40.000 km/h
00:08 - Sức công phá hàng triệu bom nguyên tử
00:16 - Lá chắn vô hình của Sao Mộc
00:24 - Vụ va chạm lịch sử Shoemaker-Levy 9
00:32 - Sự che chở kỳ diệu của vũ trụ

🔔 Đăng ký kênh Kỳ Thú Khám Phá đón xem 2 video mỗi ngày vào lúc 11:30 và 18:45!

#shorts #khoahoc #khampha #vutru #bian #saomoc #thienthach #traidat #kythukhampha
"""
    tags = [
        "shorts", "sao mộc", "thiên thạch", "vũ trụ", "bí ẩn vũ trụ", 
        "khoa học", "khám phá", "trái đất", "tiểu hành tinh", "kỳ thú khám phá", 
        "khoa học vũ trụ", "hố đen", "sao chổi"
    ]

    video_id = uploader.upload_video(
        video_file_path=final_video,
        title=title,
        description=desc,
        tags=tags,
        category_id="28",
        privacy_status="public"
    )

    print("\n" + "=" * 75)
    print(f"🎉 XUẤT BẢN THÀNH CÔNG CA TRƯA KÊNH 1!")
    print(f"📌 Video ID: {video_id}")
    print(f"🔗 Link xem: https://youtu.be/{video_id}")
    print("=" * 75)
    return video_id

if __name__ == "__main__":
    asyncio.run(produce_and_upload())
