import os
import subprocess
import math

def format_ass_timestamp(seconds: float) -> str:
    """Format seconds into ASS timestamp H:MM:SS.cc"""
    centisec = int((seconds - int(seconds)) * 100)
    minutes, seconds = divmod(int(seconds), 60)
    hours, minutes = divmod(minutes, 60)
    return f"{hours}:{minutes:02d}:{seconds:02d}.{centisec:02d}"

def build_perfect_subtitles(scenes: list, sentence_durations: list, output_ass_path: str, is_shorts: bool = True):
    """
    Tạo file phụ đề ASS chuẩn từng chữ 100% không qua mô hình nhận diện giọng nói (không bị lỗi chính tả).
    scenes: danh sách dict [{"sentence": "...", ...}]
    sentence_durations: danh sách thời lượng (giây) của từng câu.
    """
    os.makedirs(os.path.dirname(os.path.abspath(output_ass_path)), exist_ok=True)
    
    font_name = "Montserrat Black"
    font_size = 64 if is_shorts else 34
    margin_v = 520 if is_shorts else 80
    alignment = 2  # Bottom-center

    header = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {"1080" if is_shorts else "1920"}
PlayResY: {"1920" if is_shorts else "1080"}
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,{font_name},{font_size},&H00FFFFFF,&H0000FFFF,&H00000000,&H90000000,-1,0,0,0,100,100,1,0,1,6,3,{alignment},40,40,{margin_v},1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""

    current_time = 0.0
    all_events = []

    for idx, (scene, dur) in enumerate(zip(scenes, sentence_durations)):
        raw_sentence = scene["sentence"].strip()
        words = raw_sentence.split()
        if not words:
            current_time += dur
            continue

        num_words = len(words)
        # Thời lượng ước tính cho từng từ tỷ lệ thuận với độ dài ký tự
        total_chars = sum(len(w) for w in words)
        word_durations = [(len(w) / total_chars) * dur for w in words]

        word_timings = []
        w_t = current_time
        for w, w_dur in zip(words, word_durations):
            word_timings.append({
                "word": w,
                "start": w_t,
                "end": w_t + w_dur
            })
            w_t += w_dur

        # Gom từ thành cụm ngắn (2 - 3 từ) hiển thị trên màn hình
        chunk_size = 3
        for i in range(0, len(word_timings), chunk_size):
            chunk = word_timings[i:i + chunk_size]
            chunk_start = chunk[0]["start"]
            chunk_end = chunk[-1]["end"]

            for active_w in chunk:
                w_start = format_ass_timestamp(active_w["start"])
                w_end = format_ass_timestamp(active_w["end"])

                line_parts = []
                for item in chunk:
                    text_u = item["word"].upper()
                    if item == active_w:
                        # Highlight từ đang nói màu vàng neon, viền đen dày
                        line_parts.append(f"{{\\c&H002EFFFF&}}{text_u}{{\\c&H00FFFFFF&}}")
                    else:
                        line_parts.append(text_u)

                dialogue_text = " ".join(line_parts)
                all_events.append(f"Dialogue: 0,{w_start},{w_end},Default,,0,0,0,,{dialogue_text}\n")

        current_time += dur

    with open(output_ass_path, "w", encoding="utf-8") as f:
        f.write(header)
        for ev in all_events:
            f.write(ev)

    print(f"[+] Đã tạo file phụ đề hoàn hảo không lỗi chính tả: {output_ass_path}")
