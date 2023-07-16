import re
import math
from datetime import datetime, timedelta

from flask import Blueprint, render_template, request
from googleapiclient.discovery import build

from config import youtube_api_key, youtube_channel_id

bp = Blueprint("youtube", __name__, url_prefix="/youtube")

@bp.route("/")
def main():
    youtube = build("youtube", "v3", developerKey=youtube_api_key)

    videos = []
    nextPageToken = None

    hours_pattern = re.compile(r"(\d+)H")
    minutes_pattern = re.compile(r"(\d+)M")
    seconds_pattern = re.compile(r"(\d+)S")

    while True:
        playlist_request = youtube.playlistItems().list(
            part="contentDetails",
            playlistId="PLQQ1DxVUSynEX6k953Mo-V711SOyndaug",
            maxResults=50,
            pageToken=nextPageToken
        )
        playlist_response = playlist_request.execute()

        video_ids = []

        for item in playlist_response["items"]:
            video_ids.append(item["contentDetails"]["videoId"])

        video_request = youtube.videos().list(
            part="snippet, statistics, contentDetails",
            id=",".join(video_ids)
        )
        video_response = video_request.execute()

        for item in video_response["items"]:
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

        nextPageToken = playlist_response.get("nextPageToken")

        if not nextPageToken:
            break

    videos.sort(key=lambda video: video["published"], reverse=True)

    # Pagination
    page = request.args.get('page', default=1, type=int)
    per_page = 10  # number of items per page
    start = (page - 1) * per_page  # first item to display on this page
    end = start + per_page  # last item to display on this page
    items_on_page = videos[start:end]  # items to display on this page

    total = len(videos)  # total number of items in the list
    last_page = math.ceil(total / per_page)  # last page number
    block_size = 5  # number of pages in the navigation block
    block_num = int((page - 1) / block_size)  # current block number
    block_start = int((block_size * block_num) + 1)  # first page number in the block (1, 6, 11, ...
    block_end = math.ceil(block_start + (block_size - 1))  # last page number in the block

    if block_end > last_page:
        block_end = last_page

    return render_template(
        "page/youtube/main.jinja-html", 
        videos=items_on_page,
        page=page,
        per_page=per_page,
        total=total,
        last_page=last_page,
        block_start=block_start,
        block_end=block_end,
        )
