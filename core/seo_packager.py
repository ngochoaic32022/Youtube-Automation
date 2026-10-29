import json
import os

class SEOPackager:
    @staticmethod
    def package(topic: str, script_summary: str, niche: str, language: str = "vi", is_shorts: bool = False):
        """
        Creates an end-to-end SEO metadata package optimized for YouTube algorithm & CTR.
        """
        if is_shorts:
            titles = [
                f"Sự Thật Kinh Ngạc Về {topic} Mà 99% Người Chưa Biết! 😱 #shorts",
                f"Đừng Để Bị Lừa: Bí Mật Đằng Sau {topic}! 🔥 #shorts",
                f"Tại Sao {topic} Lại Khiến Cả Thế Giới Phải Bàng Hoàng? ⚡ #shorts"
            ] if language == "vi" else [
                f"The Dark Secret Behind {topic} Nobody Told You! 😱 #shorts",
                f"Why {topic} Shocked The Entire World! 🔥 #shorts",
                f"Stop Believing The Myth About {topic}! ⚡ #shorts"
            ]
        else:
            titles = [
                f"Sự Thật Đằng Sau {topic}: Kế Hoạch Thay Đổi Cả Thế Giới",
                f"Hồ Sơ Bí Ẩn: Làm Thế Nào {topic} Thao Túng Toàn Cầu?",
                f"Toàn Cảnh Về {topic}: Bài Học Đắt Giá Chưa Từng Được Kể"
            ] if language == "vi" else [
                f"The Terrifying Reality of {topic}: How It Changes Everything",
                f"Inside {topic}: The Untold Masterplan That Shook The World",
                f"The Rise and Fall of {topic}: A Chilling Documentary"
            ]

        hashtags = ["#shorts", "#kienthuc", "#khampha", "#bian", "#suthat"] if language == "vi" else ["#shorts", "#facts", "#mystery", "#documentary", "#technology"]

        tags = [
            topic,
            f"bí mật {topic}",
            f"sự thật {topic}",
            "khám phá",
            "khoa học vũ trụ",
            "kiến thức thú vị",
            "top sự thật",
            "hồ sơ bí ẩn",
            "câu chuyện có thật"
        ] if language == "vi" else [
            topic,
            f"secrets of {topic}",
            f"truth about {topic}",
            "documentary",
            "explained",
            "deep dive",
            "dark secrets",
            "mind blowing facts"
        ]

        description = f"""🔥 {titles[0]}

📌 Tóm tắt nội dung:
{script_summary}

⏱️ TIMESTAMPS / NỘI DUNG CHÍNH:
00:00 - Cú sốc đầu tiên
00:15 - Bí mật được hé lộ
00:35 - Sự thật chấn động
00:50 - Kết luận & Lời cảnh tỉnh

🔔 Đừng quên bấm ĐĂNG KÝ KÊNH và nhấn CHUÔNG để không bỏ lỡ những câu chuyện và sự thật kỳ thú tiếp theo!
👍 Like và để lại bình luận góc nhìn của bạn bên dưới!

{' '.join(hashtags)}
#youtube #trending #video
"""

        thumbnail_prompt = (
            f"Cinematic YouTube thumbnail, subject: dramatic intense close-up related to {topic}, "
            f"extreme emotional expression, volumetric lighting, dark moody background with high contrast neon cyan and yellow rim lights, "
            f"hyper-realistic 8k, photorealistic octane render, shallow depth of field --ar 16:9 --v 6.0"
            if not is_shorts else
            f"Vertical 9:16 mobile YouTube Shorts thumbnail, bold central focal point about {topic}, "
            f"shocking visual metaphor, bright punchy vibrant colors, high dynamic range HDR, 8k --ar 9:16 --v 6.0"
        )

        package_data = {
            "topic": topic,
            "titles": titles,
            "selected_title": titles[0],
            "description": description,
            "tags": tags,
            "hashtags": hashtags,
            "thumbnail_prompt": thumbnail_prompt
        }

        return package_data

    @staticmethod
    def save_package(package_data: dict, output_json_path: str):
        os.makedirs(os.path.dirname(os.path.abspath(output_json_path)), exist_ok=True)
        with open(output_json_path, "w", encoding="utf-8") as f:
            json.dump(package_data, f, ensure_ascii=False, indent=2)
        return output_json_path
