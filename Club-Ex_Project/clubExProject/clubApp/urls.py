from django.urls import path
from .views import IndexView, LoginView, SignUpView, ViewVideoListView, SearchResultsView,VideoView, AccountView, StatsView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('login/', LoginView.as_view(), name='login'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('club/videos', ViewVideoListView.as_view(), name='videolist'),
    path('club/searchresults', SearchResultsView.as_view(), name='results'),
    path('club/video/<int:pk>', VideoView.as_view(), name='video'),
    path('club/account/<int:pk>', AccountView.as_view(), name='account'),
    path('club/stats/', StatsView.as_view(), name='stats'),
]