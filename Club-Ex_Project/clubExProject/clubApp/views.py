from django import template
from django.forms.forms import Form
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from .models import Price, Video


# landing page/home page
class IndexView(TemplateView):
    template_name = "index.html"
    model = Price

    # price model def
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['prices'] = Price.objects.get(pk=1)
        return context



@login_required(login_url='login')
def viewVideoList(request):
    return render(request, "videolist.html")


@login_required(login_url='login')
def searchResultsView(request):
    context = {}
    return render(request, 'results.html', context)


@login_required(login_url='login')
def videoView(request,pk):
    video = Video.objects.get(video_id=pk)
    context = {'video':video}
    return render(request, 'video.html', context)


@login_required(login_url='login')
def statsView(request):
    context = {}
    return render(request, 'stats.html', context)