import os
import json
import datetime
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

from core.proxy_manager import get_proxy_youtube_client

SCOPES = [
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/youtube.readonly"
]

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

class YouTubeUploader:
    def __init__(self, channel_id: str, client_secrets_file: str = None):
        self.channel_id = channel_id
        self.client_secrets_file = client_secrets_file or os.path.join(ROOT_DIR, "config", "client_secrets.json")
        self.token_file = os.path.join(ROOT_DIR, "config", "tokens", f"token_{channel_id}.json")
        os.makedirs(os.path.dirname(self.token_file), exist_ok=True)

    def get_authenticated_service(self):
        return get_proxy_youtube_client(self.channel_id)

    def upload_video(self, 
                     video_file_path: str, 
                     title: str, 
                     description: str, 
                     tags: list = None, 
                     category_id: str = "27", 
                     privacy_status: str = "private",
                     publish_at_iso: str = None):
        """
        Uploads video to YouTube.
        privacy_status: 'private', 'unlisted', or 'public'.
        publish_at_iso: ISO 8601 string (e.g. '2026-10-28T12:00:00.000Z') to schedule video.
        """
        youtube = self.get_authenticated_service()

        status_body = {"privacyStatus": privacy_status}
        if publish_at_iso:
            status_body["publishAt"] = publish_at_iso
            status_body["privacyStatus"] = "private"  # Scheduled videos must have privacyStatus=private

        body = {
            "snippet": {
                "title": title[:100],
                "description": description[:5000],
                "tags": tags or [],
                "categoryId": category_id
            },
            "status": status_body
        }

        file_sz = os.path.getsize(video_file_path) if os.path.exists(video_file_path) else 0
        use_resumable = file_sz > 10 * 1024 * 1024

        media = MediaFileUpload(video_file_path, mimetype="video/mp4", resumable=use_resumable)
        request = youtube.videos().insert(
            part=",".join(body.keys()),
            body=body,
            media_body=media
        )

        if use_resumable:
            response = None
            while response is None:
                status, response = request.next_chunk()
                if status:
                    print(f"  [>] Upload Progress: {int(status.progress() * 100)}%")
        else:
            response = request.execute()

        video_id = response.get("id")
        print(f"[+] Upload hoàn tất! Video URL: https://youtu.be/{video_id}")
        return video_id
