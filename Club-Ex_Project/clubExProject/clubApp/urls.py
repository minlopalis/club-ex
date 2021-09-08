from django.urls import path
from . import views
from .views import IndexView, SearchResultsView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('club/videos/', views.viewVideoList, name='videolist'),
    path('club/searchresults/', views.SearchResultsView.as_view(), name='results'),
    path('club/video/<int:pk>', views.videoView, name='video'),
    path('club/stats/<int:pk>', views.StatisticsView.as_view(), name='stats'), 
    path('sandbox/', views.view_sandbox, name='sandbox'),
]