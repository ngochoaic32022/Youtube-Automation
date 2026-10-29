import sys
import json
import os
import time
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

sys.stdout.reconfigure(encoding='utf-8')

with open('config/tokens/token_channel_2.json', 'r', encoding='utf-8') as f:
    info = json.load(f)
creds = Credentials.from_authorized_user_info(info)
yt = build('youtube', 'v3', credentials=creds)

def upload_short(video_path, title, description, tags, pinned_comment):
    print(f"[*] Uploading {video_path}...")
    body = {
        'snippet': {
            'title': title,
            'description': description,
            'tags': tags,
            'categoryId': '10' # Music
        },
        'status': {
            'privacyStatus': 'public',
            'selfDeclaredMadeForKids': False
        }
    }
    media = MediaFileUpload(video_path, mimetype='video/mp4', resumable=True)
    req = yt.videos().insert(part='snippet,status', body=body, media_body=media)
    
    resp = None
    while resp is None:
        status, resp = req.next_chunk()
        if status:
            print(f"    Progress: {int(status.progress() * 100)}%")
            
    vid = resp['id']
    short_url = f"https://youtube.com/shorts/{vid}"
    print(f"[+] Video uploaded successfully: {vid} -> {short_url}")
    
    # Post comment
    time.sleep(2)
    try:
        c_body = {
            'snippet': {
                'videoId': vid,
                'topLevelComment': {
                    'snippet': {
                        'textOriginal': pinned_comment
                    }
                }
            }
        }
        c_resp = yt.commentThreads().insert(part='snippet', body=c_body).execute()
        print(f"[+] Comment posted successfully on {vid}")
    except Exception as e:
        print(f"[!] Could not post comment: {e}")
        
    return vid, short_url

if __name__ == '__main__':
    # 1. Upload Short 1
    v1_tags = [
        'shorts', 'vintage christmas', '1950s christmas', 'classic christmas songs',
        'have yourself a merry little christmas', 'old christmas music',
        'cozy christmas fireplace', 'nostalgic christmas', 'holiday jazz', 'vintage holiday classics'
    ]
    v1_desc = """Step back in time to the warm, glowing holiday evenings of the 1950s with Frank Sinatra singing "Have Yourself A Merry Little Christmas". 

🎄 LISTEN TO THE FULL 100-MINUTE PLAYLIST HERE:
👉 https://www.youtube.com/watch?v=1-6gOvgoQHw
(Or tap the Related Video link above the title!)

Featuring timeless holiday classics, vintage jazz carols, and crackling fireplace ambiance to warm your winter soul.

✨ Track: Have Yourself A Merry Little Christmas
🔔 Subscribe to Vintage Holiday Classics for daily nostalgic holiday music!

#shorts #vintagechristmas #christmasmusic #1950schristmas #holidaynostalgia #franksinatra #cozychristmas #christmassongs #christmascarols"""

    v1_comment = '🎄 Listen to our full 100-Minute Vintage Christmas Playlist here: https://www.youtube.com/watch?v=1-6gOvgoQHw ☕❄️ (Or tap the Related Video link right below this Short!)'

    id1, url1 = upload_short(
        'outputs/christmas_shorts/short_1_vintage_christmas.mp4',
        'Nothing Beats 1950s Christmas on a Snowy Evening ☕🎄 #shorts #vintagechristmas',
        v1_desc,
        v1_tags,
        v1_comment
    )

    # 2. Upload Short 2
    v2_tags = [
        'shorts', 'silent night', 'christmas carols', 'traditional christmas carols',
        'peaceful christmas music', 'holy night', 'church christmas carols',
        'holiday music', 'vintage holiday classics'
    ]
    v2_desc = """"Silent Night, Holy Night... All is calm, all is bright." Experience the serene peace of the world's most beloved traditional Christmas carol.

🔔 LISTEN TO THE FULL TRADITIONAL CAROLS COLLECTION HERE:
👉 https://www.youtube.com/watch?v=FVjOfcIBzp0
(Or tap the Related Video link above the title!)

Wishing you and your family a peaceful, blessed, and joyous Christmas season.

✨ Track: Silent Night (Traditional Acoustic & Choral)
🔔 Subscribe to Vintage Holiday Classics for timeless Christmas music!

#shorts #silentnight #traditionalchristmas #christmascarols #peacefulchristmas #christmassongs #holidaymusic #churchcarols #christmaseve"""

    v2_comment = '🔔 Listen to the complete Traditional Christmas Carols Collection here: https://www.youtube.com/watch?v=FVjOfcIBzp0 🕊️✨ (Or tap the Related Video link right below this Short!)'

    id2, url2 = upload_short(
        'outputs/christmas_shorts/short_2_silent_night.mp4',
        'The Most Peaceful Christmas Carol Ever Written 🔔 Silent Night #shorts #christmas',
        v2_desc,
        v2_tags,
        v2_comment
    )

    print("\n================ SUMMARY ================")
    print(f"Short 1: {url1}")
    print(f"Short 2: {url2}")
