import os
import json
import random
import requests
import sys

# Ensure UTF-8 output
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def get_pexels_api_key():
    # 1. Check environment variable (e.g. from GitHub Actions Secret)
    env_key = os.environ.get("PEXELS_API_KEY")
    if env_key:
        return env_key.strip()
    
    # 2. Check config/api_keys.json
    api_key_path = os.path.join(ROOT_DIR, "config", "api_keys.json")
    if os.path.exists(api_key_path):
        try:
            with open(api_key_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get("PEXELS_API_KEY", "").strip()
        except Exception:
            pass
    return None

def search_stock_videos(query, orientation="portrait", per_page=10):
    """
    Search Pexels for stock videos.
    orientation: 'portrait' (9:16 Shorts) or 'landscape' (16:9 Long-form)
    """
    api_key = get_pexels_api_key()
    if not api_key:
        print("[StockVideo] Error: No PEXELS_API_KEY found.")
        return []

    headers = {"Authorization": api_key}
    url = f"https://api.pexels.com/videos/search?query={requests.utils.quote(query)}&orientation={orientation}&per_page={per_page}"

    try:
        res = requests.get(url, headers=headers, timeout=12)
        if res.status_code == 200:
            data = res.json()
            return data.get("videos", [])
        else:
            print(f"[StockVideo] API Error {res.status_code}: {res.text}")
            return []
    except Exception as e:
        print(f"[StockVideo] Request failed: {e}")
        return []

def select_best_video_file(video_item, target_orientation="portrait"):
    """
    Select the optimal video file from a Pexels video object.
    Prefers Full HD (1080x1920 for portrait, 1920x1080 for landscape).
    """
    files = video_item.get("video_files", [])
    if not files:
        return None

    # Filter by mp4
    mp4_files = [f for f in files if f.get("file_type") == "video/mp4"]
    if not mp4_files:
        mp4_files = files

    if target_orientation == "portrait":
        # Look for width=1080, height=1920, or height >= 1080
        candidates = [f for f in mp4_files if f.get("height", 0) >= 1080 and f.get("width", 0) <= f.get("height", 0)]
        if candidates:
            return sorted(candidates, key=lambda x: x.get("height", 0))[0]
    else:
        # Landscape: look for width >= 1920
        candidates = [f for f in mp4_files if f.get("width", 0) >= 1920 and f.get("width", 0) >= f.get("height", 0)]
        if candidates:
            return sorted(candidates, key=lambda x: x.get("width", 0))[0]

    # Fallback to the highest resolution available
    return max(mp4_files, key=lambda x: x.get("width", 0) * x.get("height", 0))

def download_file(download_url, output_path):
    """Downloads a video stream directly to output_path."""
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    try:
        with requests.get(download_url, stream=True, timeout=30) as r:
            r.raise_for_status()
            with open(output_path, "wb") as f:
                for chunk in r.iter_content(chunk_size=1024 * 512):
                    if chunk:
                        f.write(chunk)
        return True
    except Exception as e:
        print(f"[StockVideo] Download failed: {e}")
        return False

def fetch_stock_video_clip(keyword, output_path, orientation="portrait", fallback_keywords=None):
    """
    High-level function: Searches and downloads a stock clip for a given keyword.
    If nothing found, tries fallback keywords.
    """
    print(f"[StockVideo] Searching '{keyword}' (orientation: {orientation})...")
    videos = search_stock_videos(keyword, orientation=orientation, per_page=8)

    if not videos and fallback_keywords:
        for fb in fallback_keywords:
            print(f"[StockVideo] Trying fallback keyword '{fb}'...")
            videos = search_stock_videos(fb, orientation=orientation, per_page=8)
            if videos:
                break

    if not videos:
        print(f"[StockVideo] No video found for '{keyword}'.")
        return False

    chosen = random.choice(videos[:4])
    best_file = select_best_video_file(chosen, target_orientation=orientation)
    if not best_file or "link" not in best_file:
        print("[StockVideo] Could not find suitable video file in response.")
        return False

    print(f"[StockVideo] Selected video ID {chosen.get('id')} ({best_file.get('width')}x{best_file.get('height')}). Downloading...")
    success = download_file(best_file["link"], output_path)
    if success:
        print(f"[StockVideo] Saved: {output_path} ({os.path.getsize(output_path) / (1024*1024):.1f} MB)")
    return success

if __name__ == "__main__":
    test_out = os.path.join(ROOT_DIR, "outputs", "test_stock_short.mp4")
    fetch_stock_video_clip("deep sea mysterious ocean", test_out, orientation="portrait")
