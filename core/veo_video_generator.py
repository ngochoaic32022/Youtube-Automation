"""
GOOGLE VEO VIDEO GENERATION ENGINE FOR YOUTUBE SHORTS
=============================================================================
Tích hợp mô hình tạo video AI Veo (Google DeepMind) vào quy trình sản xuất
YouTube Shorts tự động, thay thế hoàn toàn ảnh tĩnh bằng video chuyển động
điện ảnh 9:16 chất lượng cao.
=============================================================================
"""

import os
import sys
import json
import time
import subprocess
from typing import List, Dict, Optional

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(ROOT_DIR, "outputs", "veo_clips")
os.makedirs(OUTPUT_DIR, exist_ok=True)

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

class VeoPromptOptimizer:
    """
    Tối ưu hóa kịch bản câu thoại thành Prompt điện ảnh tiêu chuẩn cho Veo:
    - Bổ sung camera movement (slow pan, cinematic dolly, aerial tilt)
    - Ánh sáng điện ảnh (volumetric lighting, chiaroscuro, torchlight, cosmic glow)
    - Tỉ lệ khung hình dọc 9:16 (Vertical Shorts)
    - Phong cách chi tiết chân thực (photorealistic, 8k, cinematic color grade)
    """

    CHANNEL_STYLES = {
        "channel_1": "Hyper-realistic science documentary style, IMAX 70mm, volumetric space lighting, photorealistic VFX, deep space cosmic colors, cinematic camera push-in, 9:16 vertical aspect ratio, ultra-detailed 8K.",
        "channel_2": "Nostalgic 1950s Kodachrome vintage holiday aesthetic, warm golden glow, soft snowfall, cozy fireplace bokeh, analog film grain, smooth gentle pan, 9:16 vertical aspect ratio.",
        "channel_3": "Cinematic dark academia stoic philosophy, ancient Rome, dramatic chiaroscuro side lighting, marble statue details, moody rain, slow motion dust particles, 9:16 vertical aspect ratio, epic cinematic."
    }

    @classmethod
    def optimize_prompt(cls, raw_concept: str, channel_id: str = "channel_1") -> str:
        base_style = cls.CHANNEL_STYLES.get(channel_id, cls.CHANNEL_STYLES["channel_1"])
        optimized = f"{raw_concept.strip()}, {base_style}"
        return optimized


class VeoVideoGenerator:
    """
    Quản lý việc sinh video qua Google Veo API hoặc Google Gen AI SDK.
    Hỗ trợ chế độ Hybrid Dual-Engine tiết kiệm credit tối đa.
    """

    def __init__(self, api_key: Optional[str] = None, project_id: Optional[str] = None):
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY")
        self.project_id = project_id or os.environ.get("GOOGLE_CLOUD_PROJECT")

        if not self.api_key:
            key_file = os.path.join(ROOT_DIR, "config", "api_keys.json")
            if os.path.exists(key_file):
                try:
                    with open(key_file, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        self.api_key = data.get("GEMINI_API_KEY")
                except Exception:
                    pass

    def generate_clip_via_sdk(
        self,
        prompt: str,
        output_path: str,
        duration_seconds: int = 5,
        aspect_ratio: str = "9:16",
        model: str = "veo-3.1-generate-preview"
    ) -> bool:
        """
        Sinh video thông qua Google Gen AI SDK (`google-genai`).
        """
        try:
            from google import genai
            from google.genai import types

            if self.api_key:
                client = genai.Client(api_key=self.api_key)
            elif self.project_id:
                client = genai.Client()
            else:
                print("[!] Chưa có GEMINI_API_KEY hoặc GOOGLE_CLOUD_PROJECT.")
                return False

            print(f"[*] Đang gửi yêu cầu tạo video Veo ({model})...")
            print(f"    Prompt: {prompt[:80]}...")

            operation = client.models.generate_videos(
                model=model,
                prompt=prompt,
                config=types.GenerateVideosConfig(
                    aspect_ratio=aspect_ratio,
                    number_of_videos=1,
                    duration_seconds=duration_seconds,
                    resolution="1080p"
                )
            )

            print("[*] Đang chờ Veo render video điện ảnh...")
            while not operation.done:
                time.sleep(10)
                operation = client.operations.get(operation)

            if operation.response and operation.response.generated_videos:
                video_obj = operation.response.generated_videos[0]
                client.files.download(file=video_obj.video, destination=output_path)
                print(f"[+] Veo Render thành công: {output_path}")
                return True
            else:
                print(f"[!] Veo không trả về video: {operation}")
                return False

        except ImportError:
            print("[!] Thư viện 'google-genai' chưa được cài đặt. Có thể cài bằng: pip install google-genai")
            return False
        except Exception as e:
            print(f"[!] Lỗi khi gọi Veo SDK: {e}")
            return False

    def fetch_hybrid_clips_for_shorts(
        self,
        scenes: List[Dict[str, str]],
        channel_id: str,
        output_dir: str,
        veo_quota_per_video: int = 1
    ) -> List[str]:
        """
        CHIẾN LƯỢC TIẾT KIỆM CREDIT TỐI ĐA (HYBRID DUAL-ENGINE):
        - Scene 1 (Hook - 3 đến 5s đầu): Dùng VEO để tạo hiệu ứng điện ảnh đỉnh cao, giữ chân người xem.
        - Các Scene tiếp theo: Dùng Stock Video HD từ Pexels (100% MIỄN PHÍ, 0 Credit).
        - Nếu Veo hết credit / lỗi kết nối: Tự động Fallback sang Pexels ngay, không bị dừng pipeline.
        """
        os.makedirs(output_dir, exist_ok=True)
        video_paths = []
        from core.stock_video_fetcher import fetch_stock_video_clip

        print(f"\n{'='*75}")
        print(f"⚡ HYBRID DUAL-ENGINE: VẬN HÀNH TIẾT KIỆM CREDIT CHO {channel_id.upper()}")
        print(f"   Quota Veo cho video này: {veo_quota_per_video} cảnh (Cảnh Hook) | Các cảnh còn lại: Pexels HD (0 credit)")
        print(f"{'='*75}")

        veo_used = 0
        for idx, sc in enumerate(scenes, 1):
            clip_path = os.path.join(output_dir, f"hybrid_clip_{idx}.mp4")

            # Quyết định dùng Veo hay Pexels
            should_use_veo = (idx <= veo_quota_per_video) and bool(self.api_key or self.project_id)
            clip_ok = False

            if should_use_veo:
                print(f"\n>>> 🌟 [CẢNH {idx} - HOOK]: KÍCH HOẠT GOOGLE VEO (Tối đa hóa CTR & Retention)...")
                concept = sc.get("visual_prompt") or sc.get("keyword") or sc.get("sentence")
                optimized_prompt = VeoPromptOptimizer.optimize_prompt(concept, channel_id)
                print(f"    Veo Prompt: {optimized_prompt[:85]}...")

                clip_ok = self.generate_clip_via_sdk(
                    prompt=optimized_prompt,
                    output_path=clip_path,
                    duration_seconds=5,
                    aspect_ratio="9:16"
                )
                if clip_ok:
                    veo_used += 1
                    print(f"    ✅ Veo đã sinh clip Hook thành công! (Đã dùng: {veo_used}/{veo_quota_per_video} credit)")
                else:
                    print("    ⚠️ Veo chưa trả về video, tự động kích hoạt SMART FALLBACK sang Stock Video HD...")

            if not clip_ok:
                # Dùng Pexels Stock Video HD (0 Credit)
                mode_desc = "SMART FALLBACK" if should_use_veo else "TIẾT KIỆM CREDIT (PEXELS HD 0 XU)"
                print(f"\n>>> 🎬 [CẢNH {idx}]: {mode_desc}...")
                kw = sc.get("keyword", "cinematic space")
                fb = sc.get("fallback", "universe")
                clip_ok = fetch_stock_video_clip(kw, clip_path, orientation="portrait", fallback_keywords=[fb, "space background"])
                if not clip_ok:
                    # Dùng clip dự phòng trong outputs nếu có
                    fallback_local = os.path.join(ROOT_DIR, "outputs", "test_stock_short.mp4")
                    if os.path.exists(fallback_local):
                        clip_path = fallback_local
                        clip_ok = True

            if clip_ok and os.path.exists(clip_path):
                video_paths.append(clip_path)

        print(f"\n{'='*75}")
        print(f"🏁 ĐÃ HOÀN TẤT THU THẬP {len(video_paths)}/{len(scenes)} CLIPS:")
        print(f"   • Số clip Veo điện ảnh: {veo_used}")
        print(f"   • Số clip Stock HD miễn phí: {len(video_paths) - veo_used} (Tiết kiệm credit thành công!)")
        print(f"{'='*75}\n")

        return video_paths


if __name__ == "__main__":
    print("=" * 70)
    print("GOOGLE VEO VIDEO ENGINE TEST")
    print("=" * 70)
    generator = VeoVideoGenerator()
    test_prompt = VeoPromptOptimizer.optimize_prompt(
        "A giant fiery asteroid hurtles through deep space towards Earth, glowing magma cracks, orbital velocity",
        "channel_1"
    )
    print("Mẫu Prompt Veo được tối ưu:")
    print(f"-> {test_prompt}\n")
