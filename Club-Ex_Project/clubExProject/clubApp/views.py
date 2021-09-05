from django import template
from django.db.models.query import QuerySet
from django.forms.forms import Form
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView, ListView
from .models import Price, Video
from accounts.decorators import valid_subscription_required


# landing page/home page
class IndexView(TemplateView):
    template_name = "index.html"
    model = Price


@login_required(login_url='login')
@valid_subscription_required
def viewVideoList(request):
    return render(request, "videolist.html")


@login_required(login_url='login')
@valid_subscription_required
class SearchResultsView(ListView):
    model = Video
    template_name = "results.html"
    
    def get_queryset(self):
        query = self.request.GET.get('search')
        object_list = Video.objects.filter(
            QuerySet(video_name__icontains=query) | QuerySet(video_description__icontains=query)
        )
        return object_list


@login_required(login_url='login')
@valid_subscription_required
def videoView(request,pk):
    video = Video.objects.get(video_id=pk)
    context = {'video':video}
    return render(request, 'video.html', context)


@login_required(login_url='login')
def statsView(request):
    context = {}
    return render(request, 'stats.html', context)