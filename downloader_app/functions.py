from pytubefix import YouTube, Buffer
from pytubefix.cli import on_progress
from pytubefix.exceptions import RegexMatchError
from django.templatetags.static import static
from django.conf import settings
from moviepy import AudioFileClip
from django.contrib import messages
import os

RESERVED_CHARACTERS = '<>:"/\\|?*'


def create_yt_object(request, url):
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
            stream.type = "audio only"
            stream.resolution = ""
        else:
            if stream.is_progressive:
                stream.type = "video with audio"
            else:
                stream.type = "video only"

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

    if itag == "v":
        stream = yt.streams.get_highest_resolution()
    elif itag == "a" or itag == "m":
        stream = yt.streams.get_audio_only()
    else:
        stream = yt.streams.get_by_itag(itag)

    filename = stream.default_filename

    # remove all reserved characters from filename
    for char in filename:
        if char in RESERVED_CHARACTERS:
            filename = filename.replace(char, "")

    stream.download(filename=filename)

    if itag == "m":
        filename = convert_to_mp3(filename)  # return new .mp3 filename

    return filename


def convert_to_mp3(filename):
    try:
        audio_file = AudioFileClip(f"{filename}")  # open m4a file
    except OSError:
        audio_file = None
        print("Sorry, file does not exist, please try again.")

    if audio_file:
        audio_file.write_audiofile(f"{filename[:-3]}mp3")  # write mp3 file
        audio_file.close()
        os.remove(filename)  # delete m4a file from server (mp3 remains)
    else:
        print("Sorry, no audio in this file, try another stream with audio.")

    return f"{filename[:-3]}mp3"  # return .mp3 filename


def download_subtitles():
    pass

