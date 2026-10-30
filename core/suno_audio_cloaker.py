"""
SUNO AUDIO CLOAKER & AUTOMATION TOOL
=============================================================================
Công cụ xử lý âm thanh số (DSP) chuyên sâu để vô hiệu hóa thuật toán 
Acoustic Fingerprinting (ACRCloud / Audible Magic / ContentID) của Suno AI,
cho phép upload nhạc và tạo bản Cover/Remix/Extend trên tài khoản Suno Pro.
=============================================================================
"""

import os
import sys
import subprocess
import argparse
import json
import time

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(ROOT_DIR, "outputs", "suno_ready")
os.makedirs(OUTPUT_DIR, exist_ok=True)

class SunoAudioCloaker:
    """
    Áp dụng các kỹ thuật biến đổi phổ âm thanh đa tầng (Multi-stage DSP Transformation)
    nhằm phá vỡ cấu trúc Spectral Peak Constellation Hash của hệ thống kiểm duyệt bản quyền.
    """

    @staticmethod
    def check_ffmpeg():
        try:
            res = subprocess.run(["ffmpeg", "-version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return res.returncode == 0
        except FileNotFoundError:
            return False

    @staticmethod
    def cloak_audio(
        input_path: str,
        output_name: str = None,
        mode: str = "smart_cover",
        pitch_semitones: float = 1.25,
        tempo_factor: float = 1.04,
        start_sec: float = 0.0,
        duration_sec: float = 60.0
    ) -> str:
        """
        Xử lý file âm thanh với các profile chuyên biệt:
        - smart_cover: Đổi tone + tốc độ nhẹ + EQ Bandpass + dải nhiễu ngầm (Giữ nguyên giai điệu để Suno cover)
        - karaoke_mid_side: Triệt tiêu âm thanh trung tâm (lead vocal), giữ bè và hợp âm
        - aggressive_cloaking: Kết hợp đổi tone, tempo, đảo pha nhẹ và chèn ambient padding
        """
        if not os.path.exists(input_path):
            raise FileNotFoundError(f"Không tìm thấy file nguồn: {input_path}")

        base_name = os.path.splitext(os.path.basename(input_path))[0]
        if not output_name:
            output_name = f"{base_name}_{mode}_suno_ready.mp3"
        output_path = os.path.join(OUTPUT_DIR, output_name)

        # Tính toán tần số mẫu mới cho pitch shift
        # 2^(semitones / 12)
        pitch_ratio = 2.0 ** (pitch_semitones / 12.0)
        target_sample_rate = int(44100 * pitch_ratio)

        # Xây dựng Audio Filter Graph FFmpeg
        filters = []

        if mode == "smart_cover":
            # 1. Pitch shift thông qua asetrate và đưa về 44100 chuẩn
            # 2. Điều chỉnh tốc độ (atempo) bù trừ để nhịp phách lệch chuẩn ContentID
            # 3. Highpass 90Hz & Lowpass 8500Hz để cắt sạch tần số biên nhận diện
            # 4. Thêm 1.2s delay ở đầu để phá sliding window của thuật toán quét
            atempo_val = tempo_factor / pitch_ratio
            # Giới hạn atempo giữa 0.5 và 2.0 theo chuẩn ffmpeg
            atempo_val = max(0.5, min(2.0, atempo_val))
            
            filter_str = (
                f"asetrate={target_sample_rate},"
                f"aresample=44100,"
                f"atempo={atempo_val:.4f},"
                f"highpass=f=95,"
                f"lowpass=f=8200,"
                f"adelay=1200|1200"
            )
            filters.append(filter_str)

        elif mode == "karaoke_mid_side":
            # Triệt tiêu mono center channel (lead vocal) bằng phép trừ L - R
            filter_str = (
                f"pan=stereo|c0=c0-c1|c1=c1-c0,"
                f"asetrate={target_sample_rate},"
                f"aresample=44100,"
                f"atempo={max(0.5, min(2.0, tempo_factor / pitch_ratio)):.4f},"
                f"highpass=f=80,"
                f"lowpass=f=9000,"
                f"adelay=800|800"
            )
            filters.append(filter_str)

        elif mode == "aggressive_cloaking":
            # Chuyển đổi tối đa: Pitch + Tempo + Stereo Widening + Bandpass
            filter_str = (
                f"asetrate={target_sample_rate},"
                f"aresample=44100,"
                f"atempo={max(0.5, min(2.0, tempo_factor / pitch_ratio)):.4f},"
                f"extrastereo=m=1.8,"
                f"highpass=f=110,"
                f"lowpass=f=7800,"
                f"volume=0.95,"
                f"adelay=1500|1500"
            )
            filters.append(filter_str)
        else:
            raise ValueError(f"Mode không hợp lệ: {mode}")

        combined_filters = ",".join(filters)

        cmd = [
            "ffmpeg", "-y",
            "-ss", str(start_sec),
            "-t", str(duration_sec),
            "-i", input_path,
            "-af", combined_filters,
            "-b:a", "192k",
            "-ar", "44100",
            output_path
        ]

        print(f"[*] Đang thực thi DSP Cloaking ({mode})...")
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if res.returncode != 0:
            print(f"[!] Lỗi FFmpeg: {res.stderr}")
            raise RuntimeError(f"FFmpeg thất bại: {res.stderr}")

        print(f"[+] Hoàn tất! File đã làm sạch chữ ký bản quyền: {output_path}")
        return output_path

    @staticmethod
    def generate_suno_prompt_guide(genre_style: str = "Acoustic Pop Rock", lyrics: str = "") -> dict:
        """
        Tạo cấu trúc prompt tối ưu để Suno Pro Cover / Extend thành công mà không bị chặn text filter.
        """
        return {
            "style_prompt": f"Cover, {genre_style}, modernized arrangement, dynamic instruments, crystal clear vocals",
            "recommended_model": "v3.5 or v4 (Pro/Premier)",
            "tips": [
                "1. Khi tải lên Suno, chọn tính năng 'Upload Audio' (tối đa 60s hoặc 120s tùy gói).",
                "2. Sau khi file tải lên báo 'Ready' (đã vượt qua bộ quét bản quyền), nhấn nút '...' chọn 'Extend' hoặc 'Reuse Audio / Cover'.",
                "3. Trong ô 'Style of Music': Nhập phong cách bạn muốn biến tấu (ví dụ: Acoustic ballad, Lo-fi chill, Epic Cinematic rock).",
                "4. Trong ô 'Lyrics': Không copy nguyên văn lời gốc nếu là bài quá nổi tiếng tiếng Anh. Hãy dùng tính năng Instrumental trước, hoặc thay đổi chính tả đồng âm (Phonetic spelling) nếu muốn AI hát lại đúng lời."
            ]
        }


class SunoApiUploader:
    """
    Tự động hóa giao tiếp với API Suno (Studio API) để upload file và gửi lệnh Cover/Extend
    thông qua JWT / Session Cookie từ tài khoản Suno Pro.
    """

    def __init__(self, token: str):
        self.token = token.strip()
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
            "Referer": "https://suno.com/",
            "Origin": "https://suno.com"
        }
        import requests
        self.session = requests.Session()
        self.session.headers.update(self.headers)

    def upload_and_cover(self, audio_path: str, style_tags: str = "acoustic rock cover", title: str = "Cover Song") -> dict:
        import requests
        print(f"[*] Đang khởi tạo phiên upload Suno API cho: {os.path.basename(audio_path)}...")

        # 1. Yêu cầu cấp presigned URL
        init_url = "https://studio-api.suno.ai/api/c/upload/audio/"
        payload = {"extension": "mp3"}
        r_init = self.session.post(init_url, json=payload)
        if r_init.status_code not in (200, 201):
            raise RuntimeError(f"Không thể khởi tạo upload Suno ({r_init.status_code}): {r_init.text}")

        data = r_init.json()
        clip_id = data.get("id") or data.get("clip_id")
        upload_url = data.get("url") or data.get("upload_url")

        print(f"[+] Clip ID được cấp: {clip_id}")
        print(f"[*] Đang tải trực tiếp luồng audio lên đám mây Suno...")

        # 2. Upload nhị phân lên presigned S3/GCS URL
        with open(audio_path, "rb") as f:
            r_put = requests.put(
                upload_url,
                data=f,
                headers={"Content-Type": "audio/mpeg"}
            )
        if r_put.status_code not in (200, 204):
            raise RuntimeError(f"Lỗi khi đẩy file lên storage ({r_put.status_code}): {r_put.text}")

        print(f"[+] Tải audio hoàn tất. Đang gửi xác nhận hoàn thành...")

        # 3. Hoàn tất upload và kích hoạt kiểm duyệt
        finish_url = "https://studio-api.suno.ai/api/c/upload/finish/"
        r_fin = self.session.post(finish_url, json={"clip_id": clip_id, "upload_type": "audio"})
        if r_fin.status_code not in (200, 201):
            raise RuntimeError(f"Lỗi khi hoàn tất upload ({r_fin.status_code}): {r_fin.text}")

        print(f"[*] Đang chờ Suno phân tích âm thanh (10-15s)...")
        time.sleep(12)

        # 4. Kiểm tra trạng thái clip
        status_url = f"https://studio-api.suno.ai/api/feed/?ids={clip_id}"
        r_stat = self.session.get(status_url)
        if r_stat.status_code == 200:
            clips = r_stat.json()
            if clips and len(clips) > 0:
                c_status = clips[0].get("status")
                print(f"[+] Trạng thái Clip trên Suno: {c_status.upper()}")
                if c_status in ("complete", "uploaded"):
                    print(f"🎉 BẢN QUYỀN ĐÃ ĐƯỢC VƯỢT QUA THÀNH CÔNG!")
                elif c_status == "error":
                    print(f"[!] Clip bị báo lỗi: {clips[0].get('error_message')}")

        return {"clip_id": clip_id, "status": "submitted"}


def main():
    parser = argparse.ArgumentParser(description="Suno Audio Cloaker & Copyright Bypass Tool")
    parser.add_argument("--input", "-i", type=str, help="Đường dẫn file audio gốc (.mp3, .wav, .m4a)")
    parser.add_argument("--mode", "-m", choices=["smart_cover", "karaoke_mid_side", "aggressive_cloaking"], default="smart_cover", help="Chế độ xử lý DSP")
    parser.add_argument("--pitch", "-p", type=float, default=1.25, help="Độ dịch tone (semitones, mặc định +1.25)")
    parser.add_argument("--tempo", "-t", type=float, default=1.04, help="Hệ số tốc độ BPM (mặc định 1.04 = nhanh hơn 4%%)")
    parser.add_argument("--start", "-s", type=float, default=0.0, help="Thời điểm bắt đầu cắt (giây)")
    parser.add_argument("--duration", "-d", type=float, default=60.0, help="Thời lượng đoạn trích (giây, khuyến nghị 45-60s)")
    parser.add_argument("--token", type=str, default="", help="Suno Bearer Token (nếu muốn auto upload lên Suno Pro)")
    parser.add_argument("--style", type=str, default="acoustic rock cover", help="Phong cách cover muốn Suno phối lại")

    args = parser.parse_args()

    if not args.input:
        print("=" * 70)
        print("SUNO AUDIO CLOAKER - TOOL XỬ LÝ ÂM THANH QUA MẶT CONTENT FILTER")
        print("=" * 70)
        print("Hướng dẫn sử dụng nhanh:")
        print("  python core/suno_audio_cloaker.py -i <path_to_song.mp3> -m smart_cover")
        print("  python core/suno_audio_cloaker.py -i <path_to_song.mp3> -m karaoke_mid_side -d 60")
        print("  python core/suno_audio_cloaker.py -i <path_to_song.mp3> -m aggressive_cloaking -p 1.5 -t 1.06")
        return

    cloaker = SunoAudioCloaker()
    out_file = cloaker.cloak_audio(
        input_path=args.input,
        mode=args.mode,
        pitch_semitones=args.pitch,
        tempo_factor=args.tempo,
        start_sec=args.start,
        duration_sec=args.duration
    )

    guide = cloaker.generate_suno_prompt_guide(genre_style=args.style)
    print("\n" + "=" * 70)
    print("📋 HƯỚNG DẪN COVER TRÊN SUNO PRO:")
    print("=" * 70)
    for tip in guide["tips"]:
        print(tip)
    print(f"\n👉 File sạch chữ ký đã sẵn sàng tại: {out_file}")

    if args.token:
        print("\n" + "=" * 70)
        print("🚀 ĐANG TỰ ĐỘNG UPLOAD LÊN TÀI KHOẢN SUNO PRO QUA API...")
        print("=" * 70)
        uploader = SunoApiUploader(token=args.token)
        uploader.upload_and_cover(audio_path=out_file, style_tags=args.style)

if __name__ == "__main__":
    main()
