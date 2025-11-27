from pytubefix import YouTube
from pytubefix.cli import on_progress


def download(url):
    yt = YouTube(url, on_progress_callback=on_progress)
    ys = yt.streams.get_highest_resolution()
    ys.download()
    print(f"Video '{yt.title}' successfully downloaded")
