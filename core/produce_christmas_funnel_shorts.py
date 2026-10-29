import os
import sys
import subprocess
import json

sys.stdout.reconfigure(encoding='utf-8')

OUTPUT_DIR = "d:/KENH GEHIHI/outputs/christmas_shorts"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def sec_to_ass_time(seconds: float) -> str:
    """Chuyển số giây thành định dạng thời gian ASS: H:MM:SS.cc"""
    centisec = int((seconds - int(seconds)) * 100)
    minutes, seconds = divmod(int(seconds), 60)
    hours, minutes = divmod(minutes, 60)
    return f"{hours}:{minutes:02d}:{seconds:02d}.{centisec:02d}"

def generate_ass_subtitles(
    ass_path: str,
    title_badge: str,
    words_data: list,
    cta_text: str,
    cta_start_sec: float,
    total_duration_sec: float,
    font_name: str = "Georgia"
):
    """
    Tạo file phụ đề ASS chuẩn quốc tế cho YouTube Shorts Giáng Sinh:
    - Badge tiêu đề sang trọng phía trên
    - Lời bài hát karaoke vàng kim rực rỡ, viền đen sắc nét
    - Banner CTA kêu gọi nhấp vào video dài ở phía dưới
    """
    header = f"""[Script Info]
Title: Christmas Short Subtitles
ScriptType: v4.00+
WrapStyle: 0
ScaledBorderAndShadow: yes
PlayResX: 1080
PlayResY: 1920

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: TitleBadge,{font_name},52,&H00FFFFFF,&H0000FFFF,&H00000000,&H80000000,-1,0,0,0,100,100,1,0,1,5,3,8,30,30,220,1
Style: SubtitleNormal,{font_name},62,&H00EBF7FF,&H0000FFFF,&H00000000,&HA0000000,-1,0,0,0,100,100,1,0,1,6,4,2,40,40,620,1
Style: FunnelCTA,Montserrat Black,50,&H0000FFFF,&H0000FFFF,&H00000000,&H90000000,-1,0,0,0,100,100,1,0,1,6,4,2,30,30,320,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    events = []

    # 1. Title Badge (Hiển thị suốt video hoặc trong 12s đầu)
    t_end = sec_to_ass_time(total_duration_sec)
    events.append(f"Dialogue: 0,0:00:00.00,{t_end},TitleBadge,,0,0,0,,{{\\fad(400,400)}}{title_badge}\n")

    # 2. Lyrics karaoke word-by-word
    # Gom words_data thành các câu (mỗi câu 3-5 từ)
    for group in words_data:
        # group là danh sách [{"word": "Have", "start": 1.5, "end": 2.2}, ...]
        g_start = group[0]["start"]
        g_end = group[-1]["end"]

        for active_item in group:
            w_s = sec_to_ass_time(active_item["start"])
            w_e = sec_to_ass_time(active_item["end"])

            line_str = []
            for item in group:
                word_text = item["word"]
                if item == active_item:
                    # Highlight màu vàng kim rực rỡ (&H0032E3FF&), viền đậm
                    line_str.append(f"{{\\c&H0027E2FE&\\3c&H000E6E9C&}}{word_text}{{\\c&H00EBF7FF&\\3c&H00000000&}}")
                else:
                    line_str.append(word_text)

            rendered_line = " ".join(line_str)
            events.append(f"Dialogue: 1,{w_s},{w_e},SubtitleNormal,,0,0,0,,{rendered_line}\n")

    # 3. Funnel CTA Banner (kêu gọi bấm xem full video ở dưới)
    cta_s = sec_to_ass_time(cta_start_sec)
    events.append(f"Dialogue: 2,{cta_s},{t_end},FunnelCTA,,0,0,0,,{{\\fad(500,300)}}\\N{cta_text}\n")

    with open(ass_path, "w", encoding="utf-8") as f:
        f.write(header)
        for ev in events:
            f.write(ev)
    print(f"[+] Đã tạo file phụ đề ASS: {ass_path}")

print("Module loaded successfully.")
