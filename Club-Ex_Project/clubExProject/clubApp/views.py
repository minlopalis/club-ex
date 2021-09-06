from django import template
from django.db.models.query import QuerySet
from django.forms.forms import Form
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from .models import Price, Video
from accounts.models import Customer
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


class StatisticsView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = User
    context_object_name = 'user'
    template_name = 'stats.html'

    def test_func(self):
        obj = self.get_object()
        return obj == self.request.user