from django import template
from django.forms.forms import Form
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.views.generic import TemplateView




# def index(request):
#     return HttpResponse('<h1> this is index landing page</h1>')

# landing page/home page
class IndexView(TemplateView):
    template_name = "index.html"


class LoginView(TemplateView):
    template_name = "login.html"


class SignUpView(TemplateView):
    template_name = "signup.html"


class ViewVideoListView(TemplateView):
    template_name = "videolist.html"


class SearchResultsView(TemplateView):
    template_name = "results.html"


class VideoView(TemplateView):
    template_name = "video.html"


# view for the profile/account
class AccountView(TemplateView):
    template_name = "account.html"


class StatsView(TemplateView):
    template_name = "stats.html"