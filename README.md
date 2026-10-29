# HỆ THỐNG YOUTUBE AUTOMATION ENGINE (3 KÊNH)

Hệ thống tự động hoá sản xuất nội dung, dựng video, tạo phụ đề typography, đóng gói SEO và đăng tải tự động lên 3 kênh YouTube.

---

## 1. Cấu Trúc Thư Mục
- `config/channels.json`: Định nghĩa cấu hình 3 kênh (Niche, tỷ lệ khung hình, ngôn ngữ, giọng đọc AI).
- `config/client_secrets.json`: File xác thực Google Cloud YouTube Data API v3 (tải từ console.cloud.google.com).
- `core/`:
  - `tts_engine.py`: Động cơ lồng tiếng AI chất lượng cao (Edge-TTS hỗ trợ giọng Việt & Anh).
  - `subtitle_gen.py`: Trích xuất âm thanh và đồng bộ phụ đề chữ to chuẩn nhịp (faster-whisper + ASS format).
  - `video_renderer.py`: Bộ ghép video điện ảnh (FFmpeg, hiệu ứng Ken Burns chuyển động, nhạc nền, sub burned).
  - `seo_packager.py`: Đóng gói Title CTR cao, Description có timestamp, Tags và Midjourney prompt cho Thumbnail.
  - `youtube_uploader.py`: Module upload video tự động (hẹn giờ schedule).
- `outputs/`: Thư mục lưu video thành phẩm, audio, phụ đề và metadata của từng kênh.

---

## 2. Cách Chạy Thử Hoặc Sản Xuất Video

### Chạy demo tạo 1 video hoàn chỉnh:
```powershell
python "d:\KENH GEHIHI\main.py"
```

### Video thành phẩm mẫu:
- File video: `d:\KENH GEHIHI\outputs\channel_1\final_video.mp4` (Shorts 1080x1920)
- Metadata SEO: `d:\KENH GEHIHI\outputs\channel_1\seo_metadata.txt`
