from django.urls import path, include
from streamapp import views


urlpatterns = [
    path("", views.main, name="main"),
    path("feed", views.index, name="index"),
    path("video_feed", views.video_feed, name="video_feed"),
    path("anal", views.anal, name="anal"),
]
