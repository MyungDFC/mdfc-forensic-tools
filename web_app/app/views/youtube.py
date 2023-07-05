import re
from datetime import datetime, timedelta

from flask import Blueprint, render_template
from googleapiclient.discovery import build

from config import youtube_api_key, youtube_channel_id

bp = Blueprint("youtube", __name__, url_prefix="/youtube")

@bp.route("/")
def main():
    youtube = build("youtube", "v3", developerKey=youtube_api_key)

    channel_request = youtube.channels().list(
        part="statistics",
        id=youtube_channel_id
    )
    channel_response = channel_request.execute()

    videos = []
    nextPageToken = None

    hours_pattern = re.compile(r"(\d+)H")
    minutes_pattern = re.compile(r"(\d+)M")
    seconds_pattern = re.compile(r"(\d+)S")

    while True:
        pl_request = youtube.playlistItems().list(
            part="contentDetails",
            playlistId="PLQQ1DxVUSynEX6k953Mo-V711SOyndaug",
            maxResults=50,
            pageToken=nextPageToken
        )
        pl_response = pl_request.execute()

        video_ids = []

        for item in pl_response["items"]:
            video_ids.append(item["contentDetails"]["videoId"])

        vid_request = youtube.videos().list(
            part="snippet, statistics, contentDetails",
            id=",".join(video_ids)
        )
        vid_response = vid_request.execute()

        for item in vid_response["items"]:
            # items
            vid_title = item["snippet"]["title"]
            vid_views = item["statistics"]["viewCount"]
            vid_duration = item["contentDetails"]["duration"]
            vid_published = item["snippet"]["publishedAt"]

            # vid_url
            vid_id = item["id"]
            vid_url = f"https://www.youtube.com/embed/{vid_id}"

            # vid_duration
            hours = hours_pattern.search(vid_duration)
            minutes = minutes_pattern.search(vid_duration)
            seconds = seconds_pattern.search(vid_duration)

            hours = int(hours.group(1)) if hours else 0
            minutes = int(minutes.group(1)) if minutes else 0
            seconds = int(seconds.group(1)) if seconds else 0

            vid_seconds = timedelta(
                hours=hours,
                minutes=minutes,
                seconds=seconds
            ).total_seconds()

            minutes, seconds = divmod(vid_seconds, 60)
            hours, minutes = divmod(minutes, 60)
            minutes = int(minutes)
            seconds = int(seconds)
            vid_duration = f"{minutes}분 {seconds}초"

            # TODO: published
            # format = "%Y-%m-%dT%H:%M:%SZ"
            # vid_published = datetime.strptime(vid_published, format)

            videos.append(
                {
                    "title": vid_title,
                    "published": vid_published,
                    "url": vid_url,
                    "views": format(int(vid_views), ",d"),
                    "duration": vid_duration,
                }
            )

        nextPageToken = pl_response.get("nextPageToken")

        if not nextPageToken:
            break

    videos.sort(key=lambda video: video["published"], reverse=True)

    return render_template(
        "page/youtube/main.jinja-html", videos=videos)
