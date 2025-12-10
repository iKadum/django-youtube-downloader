from django.shortcuts import render, redirect
from django.http import HttpResponse
from wsgiref.util import FileWrapper
import os
from .functions import *


def home(request):
    yt = None
    streams_list = []
    video_url = ""

    if request.method == "POST":
        video_url = request.POST.get("video_url")
        yt = create_yt_object(video_url, request)

        if yt:
            streams_list = create_streams(yt)  # create streams from yt object and return streams list

    context = {
        "yt": yt,
        "streams_list": streams_list,
        "video_url": video_url,
    }
    return render(request, "main.html", context)


def download(request, video_id, itag):
    print(video_id)
    yt = YouTube(f"https://youtube.com/watch?v={video_id}")
    video = yt.streams.get_by_itag(itag)
    video.download()
    filename = video.default_filename

    file = FileWrapper(open(filename, "rb"))
    response = HttpResponse(file, content_type='application/vnd.mp4')
    response["Content-Disposition"] = f"attachment; filename = {filename}"
    os.remove(filename)
    return response
