import sys
import os
sys.path.insert(0, os.path.abspath("."))
sys.stdout.reconfigure(encoding='utf-8')

from core.channel2_daily_shorts_engine import CATALOG, render_short_video, upload_short_to_youtube

entry = CATALOG[0] # most_wonderful_time
print(f"[*] Producing and scheduling: {entry['song_name']}...")

video_file = render_short_video(entry)

publish_iso = "2026-10-28T00:00:00Z"
res = upload_short_to_youtube(entry, video_file, publish_iso)
print(f"\n[✓] Successfully produced and scheduled: {res['title']} -> {res['url']}")
