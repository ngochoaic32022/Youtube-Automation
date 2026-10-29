import os
import asyncio
import edge_tts
import subprocess
import json

class TTSEngine:
    def __init__(self, voice="vi-VN-NamMinhNeural", rate="+0%", volume="+0%"):
        self.voice = voice
        self.rate = rate
        self.volume = volume

    async def generate_speech(self, text: str, output_audio_path: str, output_srt_path: str = None) -> float:
        """
        Generates audio file from text using edge-tts.
        Optionally generates SRT subtitle file.
        Returns the duration of the audio in seconds.
        """
        os.makedirs(os.path.dirname(os.path.abspath(output_audio_path)), exist_ok=True)
        communicate = edge_tts.Communicate(text, self.voice, rate=self.rate, volume=self.volume)
        
        if output_srt_path:
            os.makedirs(os.path.dirname(os.path.abspath(output_srt_path)), exist_ok=True)
            submaker = edge_tts.SubMaker()
            with open(output_audio_path, "wb") as audio_file:
                async for chunk in communicate.stream():
                    if chunk["type"] == "audio":
                        audio_file.write(chunk["data"])
                    elif chunk["type"] == "WordBoundary":
                        submaker.feed(chunk)
            
            with open(output_srt_path, "w", encoding="utf-8") as srt_file:
                srt_file.write(submaker.get_srt())
        else:
            await communicate.save(output_audio_path)

        duration = self.get_audio_duration(output_audio_path)
        return duration

    @staticmethod
    def get_audio_duration(audio_path: str) -> float:
        cmd = [
            "ffprobe", "-v", "error",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            audio_path
        ]
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        try:
            return float(result.stdout.strip())
        except Exception:
            return 0.0

if __name__ == "__main__":
    # Quick self-test
    async def test():
        engine = TTSEngine(voice="vi-VN-NamMinhNeural")
        test_text = "Chào bạn! Đây là giọng đọc mẫu thử nghiệm cho kênh YouTube tự động hoá."
        out_audio = "d:/KENH GEHIHI/outputs/test_voice.mp3"
        out_srt = "d:/KENH GEHIHI/outputs/test_voice.srt"
        dur = await engine.generate_speech(test_text, out_audio, out_srt)
        print(f"Generated test voice: {out_audio} ({dur:.2f}s)")

    asyncio.run(test())
