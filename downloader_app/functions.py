from pytubefix import YouTube, Buffer
from pytubefix.cli import on_progress
from pytubefix.exceptions import RegexMatchError
from django.templatetags.static import static
from django.conf import settings
from django.contrib import messages

RESERVED_CHARACTERS = '<>:"/\\|?*'


def create_yt_object(url, request):
    try:
        yt = YouTube(url)  # check if the url is a valid YouTube url
    except RegexMatchError:
        messages.error(request, "You entered an invalid url. Check the url and try again!")
        print("You entered an invalid url. Check the url and try again!")
        return None

    return yt


def create_streams(yt):
    streams_list = []
    streams = yt.streams
    for stream in streams:
        #  change video/mp4, video/webm, audio/mp4 and audio/webm to mp4 or webm
        if "mp4" in stream.mime_type:
            stream.mime_type = "mp4"
        else:
            stream.mime_type = "webm"

        if stream.type == "audio":
            stream.fps = ""
            stream.type = "audio only "
            stream.resolution = ""
        else:
            if stream.is_progressive:
                stream.type = "video with audio"
            else:
                stream.type = "video only "

        streams_list.append({
            "itag": f"{stream.itag}",
            "type": f"{stream.type}",
            "mime_type": f"{stream.mime_type}",
            "fps": f"{stream.fps}",
            "resolution": f"{stream.resolution}",
            "filesize": f"{stream.filesize / 1048576:.1f}",
        })
    return streams_list


def download_yt(video_id, itag):
    yt = YouTube(f"https://youtube.com/watch?v={video_id}")
    video = yt.streams.get_by_itag(itag)
    filename = video.default_filename

    # remove all reserved characters from filename
    for char in filename:
        if char in RESERVED_CHARACTERS:
            filename = filename.replace(char, "")

    video.download(filename=filename)

    return filename

