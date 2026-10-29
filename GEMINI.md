# HỆ THỐNG YOUTUBE AUTOMATION ENGINE (MASTER INSTRUCTIONS & SCHEDULE)

> ⚠️ **BẢN GHI NHỚ TỰ ĐỘNG BẮT BUỘC DÀNH CHO AGENT KHI MỞ WORKSPACE D:\KENH GEHIHI**
> Agent phải đọc và tuân thủ nghiêm ngặt lịch trình, không được quên, không để người dùng phải nhắc lại!

---

## 📌 QUY ĐỊNH LỊCH TRÌNH 3 KÊNH (BẮT BUỘC HÀNG NGÀY)

### 1. 🟢 KÊNH 1: [Kỳ Thú Khám Phá - Khoa Học & Bí Ẩn] (ID: channel_1)
* **Định dạng:** YouTube Shorts (9:16, 1080x1920)
* **Tần suất bắt buộc:** **CHÍNH XÁC 2 VIDEO MỖI NGÀY**
  * ⏰ **Ca 1 (Trưa): 11:30 GMT+7**
  * ⏰ **Ca 2 (Tối): 18:45 GMT+7**
* **Tiêu chuẩn sản xuất:**
  * Giọng đọc AI: `vi-VN-NamMinhNeural` (Edge-TTS)
  * Phụ đề: Font `Montserrat Black`, chữ to màu trắng/vàng, hiệu ứng karaoke nhảy từ nhấp nháy bắt mắt
  * Hình ảnh: Khớp 100% nội dung từng câu thoại (Visual-Narrative Sync)
  * Render: FFmpeg Ken Burns chuyển động, nhạc nền dìm âm (`deep_ocean_drone.mp3`)
  * Đóng gói SEO: Tiêu đề giật gân CTR cao, mô tả có timestamp, tags và hashtag

---

### 2. 🎄 KÊNH 2: [Vintage Holiday Classics] (ID: channel_2)
* **Định dạng:** Long-form (16:9, nhạc Giáng sinh 1-2 tiếng) + Phễu Shorts dẫn luồng
* **Tần suất bắt buộc:**
  * **Video dài:** 1 video/tuần (thứ 7 hoặc chủ nhật)
  * **Shorts phễu:** **1-2 Shorts/ngày** trích đoạn nhạc hay, gắn link Related Video dẫn về video dài để cày 4.000 giờ xem.

---

### 3. 🏛️ KÊNH 3: [Stoic Echoes] (ID: channel_3)
* **Định dạng:** Hybrid Flywheel (Long-form 16:9 + Shorts 9:16)
* **Niche & Khán giả:** Triết học Khắc Kỷ (Stoicism), Marcus Aurelius, Seneca. Thị trường Mỹ & Tier-1 (RPM $15 - $28).
* **Tần suất bắt buộc:**
  * 🎬 **Video dài (Long-form 16:9): 2 VIDEO / TUẦN vào THỨ 5 VÀ CHỦ NHẬT** (Thời lượng 8 - 12 phút).
  * 📱 **Video ngắn (Shorts 9:16): 1 VIDEO / NGÀY** làm vệ tinh dẫn link về video dài.
* **Tiêu chuẩn sản xuất:**
  * Giọng đọc: `en-US-ChristopherNeural` (Edge-TTS), tốc độ `-3%`, pitch `-2Hz` trầm ấm, uy quyền.
  * Nhạc nền: Ambient mưa rơi + drone thiền định.
  * Hình ảnh: Tượng đá cẩm thạch La Mã, kiến trúc cổ đại Hy Lạp/La Mã.

---

## 🛡️ AN TOÀN HỆ THỐNG & PROXY HARD-LOCK
* Kênh 1: Proxy IP `171.241.66.158` (Token: `config/tokens/token_channel_1.json`)
* Kênh 2: Proxy IP `14.250.193.244` (Token: `config/tokens/token_channel_2.json`)
* Kênh 3: Proxy IP `171.245.160.235` (Token: `config/tokens/token_channel_3.json`)
* **Tuyệt đối không gọi API trực tiếp nếu chưa verify Proxy khớp 100%!**

---

## ⚡ NGUYÊN TẮC HÀNH XỬ CỦA AGENT KHI BẮT ĐẦU PHIÊN:
1. Khi người dùng mở phiên làm việc hoặc hỏi tình hình:
   - Ngay lập tức kiểm tra giờ hiện tại và đối chiếu với lịch xuất bản trong ngày của cả 3 kênh.
   - Báo cáo số liệu thực tế (views, subs, video mới) bằng API.
   - Nếu đến lịch (ví dụ Kênh 1 đến ca 11:30 / 18:45, hoặc Kênh 3 vào Thứ 5 / Chủ Nhật), **tự động đề xuất kịch bản và chuẩn bị sẵn sàng video**, không đợi người dùng giục.
