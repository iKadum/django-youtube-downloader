from django.shortcuts import render
from django.http import HttpResponse
from wsgiref.util import FileWrapper

from .functions import *


def home(request):
    yt = None
    all_captions = None

    streams_list = []
    video_url = ""

    if request.method == "POST":
        video_url = request.POST.get("video_url")
        yt = create_yt_object(request, video_url)

        if yt:
            streams_list = create_streams(yt)  # create streams from yt object and return streams list
            all_captions = yt.captions

    context = {
        "yt": yt,
        "streams_list": streams_list,
        "video_url": video_url,
        "all_captions": all_captions,
        "v": "v",  # download parameter for video
        "a": "a",  # download parameter for audio
        "m": "m",  # download parameter for audio mp3
        "en": "en",  # download parameter for english subtitles

    }
    return render(request, "main.html", context)


def download(request, video_id, itag):
    filename = download_yt(request, video_id, itag)  # download stream to server and return filename
    file = FileWrapper(open(filename, "rb"))
    response = HttpResponse(file, content_type='application')
    response["Content-Disposition"] = f"attachment; filename = {filename}"
    os.remove(filename)  # delete file from server
    return response


def download_sub(request, video_id, lang):
    filename = download_subtitles(video_id, lang)  # download stream to server and return filename
    file = FileWrapper(open(filename, "rb"))
    response = HttpResponse(file, content_type='application')
    response["Content-Disposition"] = f"attachment; filename = {filename}"
    os.remove(filename)  # delete file from server
    return response


