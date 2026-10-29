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
OLD_VIDEO_ID = "N5vVubDATXY"
SHORT_ID = "JvzxsvNbuqc"

def run_replacement():
    yt = get_proxy_youtube_client("channel_3")

    # 1. Set old video to private
    print(f"[*] Setting old video {OLD_VIDEO_ID} to PRIVATE...")
    try:
        yt.videos().update(
            part='status',
            body={
                'id': OLD_VIDEO_ID,
                'status': {'privacyStatus': 'private'}
            }
        ).execute()
        print(f"[+] Old video {OLD_VIDEO_ID} set to PRIVATE successfully!")
    except Exception as e:
        print(f"[!] Warning setting old video private: {e}")

    # 2. Upload new perfected video
    with open(SEO_PATH, 'r', encoding='utf-8') as f:
        seo = json.load(f)

    body = {
        'snippet': {
            'title': seo['title'],
            'description': seo['description'],
            'tags': seo['tags'],
            'categoryId': seo.get('category_id', '27')
        },
        'status': {
            'privacyStatus': 'public',
            'selfDeclaredMadeForKids': False
        }
    }

    print("[*] Uploading perfected Master Video with burned subtitles...")
    media = MediaFileUpload(VIDEO_PATH, mimetype='video/mp4', resumable=True)
    req = yt.videos().insert(part='snippet,status', body=body, media_body=media)

    resp = None
    while resp is None:
        status, resp = req.next_chunk()
        if status:
            print(f"  [>] Upload Progress: {int(status.progress() * 100)}%")

    new_video_id = resp['id']
    new_video_url = f"https://www.youtube.com/watch?v={new_video_id}"
    print(f"\n[SUCCESS] PERFECTED VIDEO UPLOADED! ID: {new_video_id}")
    print(f"👉 URL: {new_video_url}")

    # 3. Set thumbnail
    if os.path.exists(THUMB_PATH):
        try:
            print(f"[*] Setting custom thumbnail from: {THUMB_PATH}...")
            thumb_media = MediaFileUpload(THUMB_PATH, mimetype='image/jpeg')
            yt.thumbnails().set(videoId=new_video_id, media_body=thumb_media).execute()
            print("[+] Custom thumbnail set successfully!")
        except Exception as e:
            print(f"[!] Thumbnail error: {e}")

    # 4. Update Shorts description with new link
    try:
        print(f"[*] Updating Short {SHORT_ID} description to point to {new_video_url}...")
        short_res = yt.videos().list(part='snippet', id=SHORT_ID).execute()
        if short_res.get('items'):
            short_item = short_res['items'][0]
            desc = short_item['snippet']['description']
            updated_desc = desc.replace(f"https://www.youtube.com/watch?v={OLD_VIDEO_ID}", new_video_url)
            short_item['snippet']['description'] = updated_desc
            yt.videos().update(part='snippet', body={'id': SHORT_ID, 'snippet': short_item['snippet']}).execute()
            print("[+] Shorts description updated with new link!")
    except Exception as e:
        print(f"[!] Warning updating shorts: {e}")

    # 5. Save log
    log_file = "d:/KENH GEHIHI/outputs/channel_3/publish_log.json"
    with open(log_file, 'w', encoding='utf-8') as f:
        json.dump({
            "master_video_id": new_video_id,
            "master_video_url": new_video_url,
            "short_id": SHORT_ID,
            "old_video_id_private": OLD_VIDEO_ID,
            "published_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        }, f, indent=2)

    return new_video_id

if __name__ == "__main__":
    run_replacement()
