import os
from faster_whisper import WhisperModel

def format_ass_timestamp(seconds: float) -> str:
    """Format seconds into ASS timestamp H:MM:SS.cc"""
    centisec = int((seconds - int(seconds)) * 100)
    minutes, seconds = divmod(int(seconds), 60)
    hours, minutes = divmod(minutes, 60)
    return f"{hours}:{minutes:02d}:{seconds:02d}.{centisec:02d}"

class SubtitleGenerator:
    def __init__(self, model_size="tiny", device="cpu"):
        self.model = WhisperModel(model_size, device=device, compute_type="int8")

    def generate_srt_and_ass(self, audio_path: str, output_srt: str, output_ass: str = None, format_type: str = "shorts"):
        segments, info = self.model.transcribe(audio_path, word_timestamps=True)
        segment_list = list(segments)

        # Collect all words with timestamps
        all_words = []
        for s in segment_list:
            if s.words:
                for w in s.words:
                    word_clean = w.word.strip()
                    if word_clean:
                        all_words.append({
                            "word": word_clean,
                            "start": w.start,
                            "end": w.end
                        })

        if output_ass:
            os.makedirs(os.path.dirname(os.path.abspath(output_ass)), exist_ok=True)
            self._write_dynamic_ass(all_words, output_ass, format_type)

        return segment_list

    def _write_dynamic_ass(self, words, ass_path: str, format_type: str):
        is_shorts = (format_type == "shorts")
        font_name = "Montserrat Black"
        font_size = 62 if is_shorts else 32
        margin_v = 520 if is_shorts else 80
        alignment = 2  # Bottom-center

        # ASS header with custom font and high-contrast outline
        header = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {"1080" if is_shorts else "1920"}
PlayResY: {"1920" if is_shorts else "1080"}
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,{font_name},{font_size},&H00FFFFFF,&H0000FFFF,&H00000000,&H90000000,-1,0,0,0,100,100,1,0,1,5,3,{alignment},40,40,{margin_v},1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
        with open(ass_path, "w", encoding="utf-8") as f:
            f.write(header)

            if not words:
                return

            # Group into short punchy chunks of 2 to 4 words
            chunk_size = 3 if is_shorts else 6
            for i in range(0, len(words), chunk_size):
                chunk = words[i:i + chunk_size]
                chunk_start = chunk[0]["start"]
                chunk_end = chunk[-1]["end"]

                # Each word in chunk gets highlighted as spoken
                for active_idx, active_word in enumerate(chunk):
                    w_start = format_ass_timestamp(active_word["start"])
                    w_end = format_ass_timestamp(active_word["end"])
                    
                    # Highlight active word in neon yellow &H0000FFFF&, other words in crisp white
                    line_parts = []
                    for w in chunk:
                        text_u = w["word"].upper() if is_shorts else w["word"]
                        if w == active_word:
                            line_parts.append(f"{{\\c&H002EFFFF&}}{text_u}{{\\c&H00FFFFFF&}}")
                        else:
                            line_parts.append(text_u)

                    display_text = " ".join(line_parts)
                    f.write(f"Dialogue: 0,{w_start},{w_end},Default,,0,0,0,,{display_text}\n")
