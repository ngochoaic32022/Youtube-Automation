import os
import subprocess
from typing import List

class VideoRenderer:
    def __init__(self, width: int = 1080, height: int = 1920, fps: int = 30):
        self.width = width
        self.height = height
        self.fps = fps

    def _get_audio_duration(self, audio_path: str) -> float:
        cmd = [
            "ffprobe", "-v", "error",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            audio_path
        ]
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return float(res.stdout.strip())

    def render_from_video_clips(self,
                                video_clip_paths: List[str],
                                voice_audio_path: str,
                                output_video_path: str,
                                subtitle_path: str = None,
                                bg_music_path: str = None,
                                music_volume: float = 0.15):
        """
        Renders a full dynamic video using real motion video clips (e.g. from Pexels stock footage).
        Scales, centers, crops, mixes voice and background music, and burns in karaoke subtitles.
        """
        os.makedirs(os.path.dirname(os.path.abspath(output_video_path)), exist_ok=True)
        total_duration = self._get_audio_duration(voice_audio_path)
        num_clips = max(1, len(video_clip_paths))
        duration_per_clip = total_duration / num_clips

        temp_dir = os.path.join(os.path.dirname(output_video_path), "temp_clips")
        os.makedirs(temp_dir, exist_ok=True)

        temp_clips = []
        for idx, clip in enumerate(video_clip_paths):
            out_clip = os.path.join(temp_dir, f"prepared_clip_{idx:03d}.mp4")
            
            # Filter: scale to fill target frame and crop to exact dimensions
            vf = (
                f"scale={self.width}:{self.height}:force_original_aspect_ratio=increase,"
                f"crop={self.width}:{self.height},"
                f"fps={self.fps}"
            )

            # Loop the clip if it's shorter than required duration
            cmd = [
                "ffmpeg", "-y",
                "-stream_loop", "-1",
                "-i", clip,
                "-vf", vf,
                "-t", f"{duration_per_clip:.3f}",
                "-an",
                "-pix_fmt", "yuv420p",
                "-c:v", "libx264",
                "-preset", "veryfast",
                out_clip
            ]
            subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
            temp_clips.append(out_clip)

        # Concatenate prepared clips
        concat_txt = os.path.join(temp_dir, "concat_motion.txt")
        with open(concat_txt, "w", encoding="utf-8") as f:
            for c in temp_clips:
                clean_path = os.path.abspath(c).replace("\\", "/")
                f.write(f"file '{clean_path}'\n")

        temp_concat_video = os.path.join(temp_dir, "concat_motion_visual.mp4")
        subprocess.run([
            "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", concat_txt,
            "-c", "copy", temp_concat_video
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

        # Subtitles filter
        sub_filter = ""
        if subtitle_path and os.path.exists(subtitle_path):
            clean_sub = os.path.abspath(subtitle_path).replace("\\", "/").replace(":", "\\:")
            sub_filter = f",subtitles='{clean_sub}'"

        inputs = ["-i", temp_concat_video, "-i", voice_audio_path]
        audio_filter = "[1:a]volume=1.0[a1];"

        if bg_music_path and os.path.exists(bg_music_path):
            inputs.extend(["-i", bg_music_path])
            audio_filter += f"[2:a]aloop=loop=-1:size=2e+09,volume={music_volume}[a2];[a1][a2]amix=inputs=2:duration=first[aout]"
            map_audio = "[aout]"
        else:
            audio_filter += "[a1]anull[aout]"
            map_audio = "[aout]"

        vf_cmd = f"null{sub_filter}"

        final_cmd = [
            "ffmpeg", "-y",
            *inputs,
            "-filter_complex", f"{audio_filter};[0:v]{vf_cmd}[vout]",
            "-map", "[vout]",
            "-map", map_audio,
            "-c:v", "libx264",
            "-preset", "fast",
            "-crf", "20",
            "-c:a", "aac",
            "-b:a", "192k",
            "-t", f"{total_duration:.3f}",
            output_video_path
        ]

        subprocess.run(final_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

        # Cleanup temp files
        try:
            for c in temp_clips:
                if os.path.exists(c):
                    os.remove(c)
            if os.path.exists(concat_txt):
                os.remove(concat_txt)
            if os.path.exists(temp_concat_video):
                os.remove(temp_concat_video)
        except Exception:
            pass

        return output_video_path

    def render(self, 
               image_paths: List[str], 
               voice_audio_path: str, 
               output_video_path: str, 
               subtitle_path: str = None, 
               bg_music_path: str = None, 
               music_volume: float = 0.15):
        """
        Renders a dynamic, cinematic video with alternating Ken Burns camera moves from images.
        """
        os.makedirs(os.path.dirname(os.path.abspath(output_video_path)), exist_ok=True)
        total_duration = self._get_audio_duration(voice_audio_path)

        num_images = max(1, len(image_paths))
        duration_per_img = total_duration / num_images
        frames_per_img = int(duration_per_img * self.fps)

        temp_dir = os.path.join(os.path.dirname(output_video_path), "temp_clips")
        os.makedirs(temp_dir, exist_ok=True)

        temp_clips = []
        for idx, img in enumerate(image_paths):
            clip_path = os.path.join(temp_dir, f"clip_{idx:03d}.mp4")
            
            mode = idx % 4
            if mode == 0:
                zp_filter = f"zoompan=z='min(zoom+0.0015,1.18)':d={frames_per_img}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'"
            elif mode == 1:
                zp_filter = f"zoompan=z='1.12':d={frames_per_img}:x='iw/2-(iw/zoom/2)':y='(ih-ih/zoom)*(on/{frames_per_img})'"
            elif mode == 2:
                zp_filter = f"zoompan=z='min(zoom+0.002,1.20)':d={frames_per_img}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'"
            else:
                zp_filter = f"zoompan=z='if(lte(zoom,1.0),1.18,max(1.001,zoom-0.0015))':d={frames_per_img}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'"

            full_vf = (
                f"scale={self.width*2}:{self.height*2}:force_original_aspect_ratio=increase,"
                f"crop={self.width*2}:{self.height*2},"
                f"{zp_filter}:s={self.width}x{self.height}:fps={self.fps}"
            )

            cmd = [
                "ffmpeg", "-y", "-loop", "1", "-i", img,
                "-vf", full_vf,
                "-t", f"{duration_per_img:.3f}",
                "-pix_fmt", "yuv420p",
                "-c:v", "libx264",
                "-preset", "veryfast",
                clip_path
            ]
            subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
            temp_clips.append(clip_path)

        concat_txt = os.path.join(temp_dir, "concat.txt")
        with open(concat_txt, "w", encoding="utf-8") as f:
            for clip in temp_clips:
                clean_path = os.path.abspath(clip).replace("\\", "/")
                f.write(f"file '{clean_path}'\n")

        temp_concat_video = os.path.join(temp_dir, "concat_visual.mp4")
        subprocess.run([
            "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", concat_txt,
            "-c", "copy", temp_concat_video
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

        sub_filter = ""
        if subtitle_path and os.path.exists(subtitle_path):
            clean_sub = os.path.abspath(subtitle_path).replace("\\", "/").replace(":", "\\:")
            sub_filter = f",subtitles='{clean_sub}'"

        inputs = ["-i", temp_concat_video, "-i", voice_audio_path]
        audio_filter = "[1:a]volume=1.0[a1];"

        if bg_music_path and os.path.exists(bg_music_path):
            inputs.extend(["-i", bg_music_path])
            audio_filter += f"[2:a]aloop=loop=-1:size=2e+09,volume={music_volume}[a2];[a1][a2]amix=inputs=2:duration=first[aout]"
            map_audio = "[aout]"
        else:
            audio_filter += "[a1]anull[aout]"
            map_audio = "[aout]"

        vf_cmd = f"null{sub_filter}"

        final_cmd = [
            "ffmpeg", "-y",
            *inputs,
            "-filter_complex", f"{audio_filter};[0:v]{vf_cmd}[vout]",
            "-map", "[vout]",
            "-map", map_audio,
            "-c:v", "libx264",
            "-preset", "fast",
            "-crf", "20",
            "-c:a", "aac",
            "-b:a", "192k",
            "-t", f"{total_duration:.3f}",
            output_video_path
        ]

        subprocess.run(final_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

        try:
            for c in temp_clips:
                if os.path.exists(c):
                    os.remove(c)
            if os.path.exists(concat_txt):
                os.remove(concat_txt)
            if os.path.exists(temp_concat_video):
                os.remove(temp_concat_video)
        except Exception:
            pass

        return output_video_path
