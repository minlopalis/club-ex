from django import template
from django.db.models.query import QuerySet
from django.db.models.query_utils import Q
from django.forms.forms import Form
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from .models import Price, Video, VideoCategory, VideoWatchTime, VideoRating
from accounts.models import Customer
from accounts.decorators import valid_subscription_required
import json 
from django.http import JsonResponse
import operator



# landing page/home page
class IndexView(TemplateView):
    template_name = "index.html"
    model = Price


@login_required(login_url='login')
@valid_subscription_required
def viewVideoList(request):
    current_user = request.user
    search_query = request.GET.get('search')
    order_query = request.GET.get('order')
    if not search_query:
        search_query = "NULL"
    if search_query:
        object_list = Video.objects.filter(
            Q(video_name__icontains=search_query) | Q(video_description__icontains=search_query)
        )

    if not order_query:
        order_query = "video_name"

    try:
        customer = Customer.objects.get(user=current_user.id)
    except:
        customer = None
    categories = VideoCategory.objects.all()
    videos = Video.objects.all()
    ordered = sorted(videos, key=operator.attrgetter(order_query))
    for video in ordered:
        existing_video_rating = VideoRating.objects.filter(video_id=video, customer_id=customer).values_list('rating').first()
       
        if(existing_video_rating):
            
            video.video_rating = existing_video_rating[0]
            video.save()
        else:
            video.video_rating = 0
            video.save()
    
    updated_videos = Video.objects.all()

    for video in updated_videos:
        print(video.video_rating)
    context={'videos':updated_videos, 'categories':categories, 'object_list':object_list}
    
    return render(request, "videolist.html",context)


@login_required(login_url='login')
@valid_subscription_required
def videoView(request,pk):
    video = Video.objects.get(video_id=pk).orderby('video_name')
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





def update_video_watch_time(request):
    current_user = request.user
   
    if request.method == 'POST':
        data = json.loads(request.body)
        
        second = data.get('seconds', None)
        user_id = data.get('currentUserId', None)
        video_id = data.get("selectedVideoId", None)
        
        video = Video.objects.get(video_id=video_id)
        customer = Customer.objects.get(user=current_user.id)
        
        selected_video = VideoWatchTime.objects.filter(video_id = video, customer_id = customer)
        if not selected_video:
            VideoWatchTime.objects.create(video_id = video, customer_id = customer, total_watch_time = second)
        else:
            update_video = VideoWatchTime.objects.get(video_id = video, customer_id = customer)
            new_watch_time = update_video.total_watch_time + second
            
            update_video.total_watch_time = new_watch_time
            update_video.save()
            
        return JsonResponse({"message": second}, status=200)

def update_video_views(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        print(data)
        video_id = data.get("selectedVideoId", None)
        video = Video.objects.get(video_id = video_id)
        print(video)
        return JsonResponse({"views": 1}, status=200)

def update_video_rating(request):
    current_user = request.user
    if request.method == 'POST':
        data = json.loads(request.body)
        print(data)

        rating = data.get('rating', None)
        video_id = data.get("selectedVideoId", None)

        video = Video.objects.get(video_id=video_id)
        customer = Customer.objects.get(user=current_user.id)
        selected_video = VideoRating.objects.filter(video_id = video, customer_id = customer)
        if not selected_video:
            VideoRating.objects.create(video_id = video, customer_id = customer, rating = 0)
        else:
            update_video = VideoRating.objects.get(video_id = video, customer_id = customer)
            update_video.rating = rating
            video.video_rating = rating
            update_video.save()
            video.save()
   
        return JsonResponse({},status=200)

def get_video_rating(request,pk):
    current_user = request.user
    if request.method == 'GET':
        video = Video.objects.get(video_id=pk)
        print()
    return JsonResponse({"rating": video.video_rating},status=200)