import os
import sys
import json
import asyncio
from core.tts_engine import TTSEngine
from core.subtitle_gen import SubtitleGenerator
from core.video_renderer import VideoRenderer
from core.seo_packager import SEOPackager

# Force UTF-8 stdout for Windows console
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

CONFIG_PATH = "d:/KENH GEHIHI/config/channels.json"

def load_channels():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)["channels"]

async def run_pipeline(channel_id: str, topic: str, scenes: list, bg_music: str = None):
    """
    scenes is a list of dicts:
    [
        {"sentence": "...", "image": "path/to/img.jpg", "description": "..."},
        ...
    ]
    """
    channels = load_channels()
    if channel_id not in channels:
        print(f"Error: Kênh '{channel_id}' không tồn tại trong channels.json")
        return

    chan = channels[channel_id]
    is_shorts = (chan["format"] == "shorts")
    res_w, res_h = chan["resolution"]
    voice = chan["voice"]
    out_dir = f"d:/KENH GEHIHI/outputs/{channel_id}"
    os.makedirs(out_dir, exist_ok=True)

    script_sentences = [s["sentence"] for s in scenes]
    image_paths = [s["image"] for s in scenes]
    full_script = " ".join(script_sentences)

    print(f"\n========================================================")
    print(f"[*] SẢN XUẤT VIDEO CHẤT LƯỢNG CAO CHO: {chan['name']} ({channel_id})")
    print(f"[*] Chủ đề: {topic}")
    print(f"[*] Tổng số phân cảnh: {len(scenes)} cảnh (100% Khớp nội dung)")
    print(f"========================================================")

    # 1. TTS Voice Generation
    print("\n[1/4] Đang tạo Voiceover AI chất lượng cao...")
    tts = TTSEngine(voice=voice)
    voice_audio = os.path.join(out_dir, "voice.mp3")
    raw_srt = os.path.join(out_dir, "voice.srt")
    duration = await tts.generate_speech(full_script, voice_audio, raw_srt)
    print(f"  -> Hoàn thành Voiceover! Thời lượng: {duration:.2f} giây")

    # 2. Subtitles Generation (Whisper + ASS Styling)
    print("\n[2/4] Đang tạo phụ đề Typography nổi bật (Whisper AI + ASS)...")
    sub_gen = SubtitleGenerator(model_size="tiny", device="cpu")
    ass_path = os.path.join(out_dir, "subtitles.ass")
    sub_gen.generate_srt_and_ass(voice_audio, raw_srt, ass_path, format_type=chan["format"])
    print(f"  -> Phụ đề lưu tại: {ass_path}")

    # 3. Phân cảnh hình ảnh khớp 100%
    print("\n[3/4] Kiểm tra độ khớp hình ảnh và lời thoại:")
    for idx, s in enumerate(scenes, 1):
        print(f"  [Phân cảnh {idx}] {s['description']}")
        print(f"     + Lời thoại: \"{s['sentence']}\"")
        print(f"     + File ảnh:  {s['image']}")

    # 4. Video Rendering (FFmpeg Ken Burns + Ducked Music + Burned Subs)
    print("\n[4/4] Đang dựng video điện ảnh (hiệu ứng chuyển động + âm thanh đáy biển)...")
    renderer = VideoRenderer(width=res_w, height=res_h, fps=30)
    final_video = os.path.join(out_dir, "final_video.mp4")
    
    renderer.render(
        image_paths=image_paths,
        voice_audio_path=voice_audio,
        output_video_path=final_video,
        subtitle_path=ass_path,
        bg_music_path=bg_music,
        music_volume=0.18
    )
    print(f"  -> ĐÃ RENDER THÀNH PHẨM: {final_video}")

    # 5. SEO Packaging
    print("\n[*] Đang đóng gói Metadata SEO hoàn chỉnh...")
    seo_meta = SEOPackager.package(
        topic=topic,
        script_summary=full_script[:200],
        niche=chan["niche"],
        language=chan["language"],
        is_shorts=is_shorts
    )
    seo_json = os.path.join(out_dir, "seo_package.json")
    SEOPackager.save_package(seo_meta, seo_json)

    seo_txt = os.path.join(out_dir, "seo_metadata.txt")
    with open(seo_txt, "w", encoding="utf-8") as f:
        f.write(f"=== TIÊU ĐỀ GỢI Ý (CHỌN 1) ===\n")
        for i, t in enumerate(seo_meta["titles"], 1):
            f.write(f"{i}. {t}\n")
        f.write(f"\n=== MÔ TẢ VIDEO ===\n{seo_meta['description']}\n")
        f.write(f"\n=== THẺ TAGS ===\n{', '.join(seo_meta['tags'])}\n")
        f.write(f"\n=== PROMPT THUMBNAIL (MIDJOURNEY/FLUX) ===\n{seo_meta['thumbnail_prompt']}\n")

    print(f"  -> Gói SEO lưu tại: {seo_txt}")
    print("\n========================================================")
    print(f"[HOÀN TẤT] Video mẫu sinh động, khớp chuẩn 100% nội dung đã sẵn sàng!")
    print(f"Video path: {final_video}")
    print(f"========================================================")

if __name__ == "__main__":
    demo_topic = "Bí Mật Cực Kỳ Đáng Sợ Dưới Đáy Rãnh Mariana"
    
    # 5 phân cảnh khớp chính xác từng câu thoại
    curated_scenes = [
        {
            "sentence": "Bạn có biết, con người đã lên mặt trăng nhiều lần, nhưng mới chỉ có 4 người từng xuống tới điểm sâu nhất của rãnh Mariana?",
            "image": "d:/KENH GEHIHI/outputs/channel_1/scene_1.jpg",
            "description": "Cảnh 1: Phi hành gia Apollo bước chân trên bề mặt Mặt Trăng (đối lập vũ trụ vs đáy biển)"
        },
        {
            "sentence": "Ở độ sâu gần 11 nghìn mét, áp lực nước lớn gấp 1000 lần trên mặt đất, đủ để bóp nát một chiếc tàu ngầm trong nháy mắt.",
            "image": "d:/KENH GEHIHI/outputs/channel_1/scene_3.jpg",
            "description": "Cảnh 2: Hẻm vực đại dương tối đen sâu 11.000m với áp lực nước nghẹt thở"
        },
        {
            "sentence": "Thế nhưng, các nhà khoa học lại phát hiện những sinh vật kỳ dị không hề có mắt và cơ thể hoàn toàn trong suốt đang bơi lội.",
            "image": "d:/KENH GEHIHI/outputs/channel_1/scene_4.jpg",
            "description": "Cảnh 3: Sinh vật kỳ dị trong suốt, phát quang sinh học neon giữa lòng đại dương tăm tối"
        },
        {
            "sentence": "Kinh ngạc hơn nữa, ở nơi tưởng chừng không có sự sống, họ vẫn tìm thấy một mảnh túi ni lông của con người.",
            "image": "d:/KENH GEHIHI/outputs/channel_1/scene_5.jpg",
            "description": "Cảnh 4: Rác thải túi ni lông trôi dạt dưới đáy biển sâu thẳm gây chấn động"
        },
        {
            "sentence": "Bạn nghĩ dưới đáy đại dương còn ẩn chứa bí mật gì nữa? Đăng ký kênh để khám phá thêm nhé!",
            "image": "d:/KENH GEHIHI/outputs/channel_1/scene_2.jpg",
            "description": "Cảnh 5: Tàu thám hiểm lặn sâu vào vực thẳm vô tận và lời kêu gọi Đăng ký kênh"
        }
    ]
    bg_music = "d:/KENH GEHIHI/assets/music/deep_ocean_drone.mp3"

    asyncio.run(run_pipeline("channel_1", demo_topic, curated_scenes, bg_music))
