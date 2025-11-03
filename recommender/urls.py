from django.urls import path
from .views import music_agent_view

urlpatterns = [
    path("music-agent/", music_agent_view, name="music_agent"),
]
