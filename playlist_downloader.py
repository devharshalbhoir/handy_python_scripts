import os
import re
import tempfile

from pytube import Playlist, YouTube


def download_playlist(url, resolution):
    playlist = Playlist(url)
    playlist_name = re.sub(r'\W+', '-', playlist.title)

    if not os.path.exists(playlist_name):
        os.mkdir(playlist_name)

    for index, v in enumerate(playlist.videos, start=1):
        video = YouTube(v.watch_url, use_oauth=True)
        video_resolution = video.streams.filter(res=resolution).first()
        video_filename = "video.mp4"
        if video_resolution:
            video_filename = f"{video_resolution.default_filename}"
        video_path = os.path.join(playlist_name, video_filename)
        if os.path.exists(video_path):
            print(f"{video_filename} already exists")
            continue

        # if not video_streams:
        highest_resolution_stream = video.streams.get_highest_resolution()
        video_name = highest_resolution_stream.default_filename
        print(
            f"Downloading {video_name} in {highest_resolution_stream.resolution}")

        # Create a temporary file for merging video and audio
        with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as temp_file:
            temp_file_path = temp_file.name

        video_path2 = os.path.join(playlist_name, video_name)
        os.rename(temp_file_path, video_path2)
        highest_resolution_stream.download(filename=video_path2)
        print("---------------- Completed ------------------")


if __name__ == "__main__":
    playlist_url = input("Enter the playlist url: ")
    resolutions = ["240p", "360p", "480p", "720p", "1080p", "1440p", "2160p"]
    resolution = input(f"Please select a resolution {resolutions}: ")
    download_playlist(playlist_url, resolution)

# playlist_url = "https://youtube.com/playlist?list=PL2W7_Se58Bo1bIb8UDmTQUdN19IN0kB71"
# resolution = "1080p"
