import os
import sys
sys.path.append('d:/KENH GEHIHI')
import json
import time
from core.proxy_manager import get_proxy_youtube_client
from googleapiclient.http import MediaFileUpload

sys.stdout.reconfigure(encoding='utf-8')

WORKDIR = "d:/KENH GEHIHI"
BASE_DIR = "outputs/channel_3/video_1"
VIDEO_PATH = os.path.join(WORKDIR, BASE_DIR, "master_video.mp4")
THUMB_PATH = os.path.join(WORKDIR, BASE_DIR, "thumbnail.jpg")
SEO_PATH = os.path.join(WORKDIR, BASE_DIR, "seo_package.json")

def upload_video_1(privacy_status="public", publish_at_iso=None):
    with open(SEO_PATH, 'r', encoding='utf-8') as f:
        seo = json.load(f)

    yt = get_proxy_youtube_client("channel_3")

    status_body = {
        'privacyStatus': privacy_status,
        'selfDeclaredMadeForKids': False
    }
    if publish_at_iso:
        status_body['privacyStatus'] = 'private'
        status_body['publishAt'] = publish_at_iso

    body = {
        'snippet': {
            'title': seo['title'],
            'description': seo['description'],
            'tags': seo['tags'],
            'categoryId': seo.get('category_id', '27')
        },
        'status': status_body
    }

    print(f"[*] Uploading Video 1 to Channel 3 (Mode: {status_body['privacyStatus']})...")
    media = MediaFileUpload(VIDEO_PATH, mimetype='video/mp4', resumable=True)
    req = yt.videos().insert(part='snippet,status', body=body, media_body=media)

    resp = None
    while resp is None:
        status, resp = req.next_chunk()
        if status:
            print(f"  [>] Upload Progress: {int(status.progress() * 100)}%")

    video_id = resp['id']
    video_url = f"https://www.youtube.com/watch?v={video_id}"
    print(f"\n[SUCCESS] VIDEO 1 UPLOADED! ID: {video_id}")
    print(f"👉 URL: {video_url}")

    # Set custom thumbnail
    if os.path.exists(THUMB_PATH):
        try:
            print(f"[*] Setting custom thumbnail from: {THUMB_PATH}...")
            thumb_media = MediaFileUpload(THUMB_PATH, mimetype='image/jpeg')
            yt.thumbnails().set(videoId=video_id, media_body=thumb_media).execute()
            print("[+] Custom thumbnail set successfully!")
        except Exception as e:
            print(f"[!] Thumbnail upload warning: {e}")

    # Save to catalog / log
    log_file = "d:/KENH GEHIHI/outputs/channel_3/publish_log.json"
    log_data = {"videos": []}
    if os.path.exists(log_file):
        try:
            with open(log_file, 'r', encoding='utf-8') as f:
                log_data = json.load(f)
        except:
            pass

    log_data["videos"].append({
        "video_id": video_id,
        "url": video_url,
        "title": seo['title'],
        "published_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "mode": privacy_status
    })
    with open(log_file, 'w', encoding='utf-8') as f:
        json.dump(log_data, f, indent=2, ensure_ascii=False)

    return resp

if __name__ == "__main__":
    upload_video_1()
