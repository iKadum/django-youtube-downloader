from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.home, name="homepage"),
    path("download/<str:itag>/", views.download, name="download"),
]

