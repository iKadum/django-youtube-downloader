from django.shortcuts import render
from .functions import download


def home(request):
    video_url = ""

    if request.method == "POST":
        video_url = request.POST.get("video_url")
        download(video_url)

    context = {"video_url": video_url}
    return render(request, "main.html", context)

