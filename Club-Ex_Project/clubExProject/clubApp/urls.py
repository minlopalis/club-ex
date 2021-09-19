from django.urls import path
from . import views
from .views import IndexView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('club/videos/', views.viewVideoList, name='videolist'),
    path('club/video/<int:pk>', views.videoView, name='video'),
    path('club/stats/<int:pk>', views.StatisticsView.as_view(), name='stats'), 

    path('ajax/update_video_watch_time/', views.update_video_watch_time, name='updateWatchTime'),
    path('ajax/update_video_views/', views.update_video_views, name='updateViews'),
    path('ajax/update_video_rating/', views.update_video_rating, name='updateRating'),
    path('ajax/get_video_rating/<int:pk>', views.get_video_rating, name='getRating')
]