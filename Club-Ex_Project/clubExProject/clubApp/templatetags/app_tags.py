from django import template
from ..models import Video, VideoWatchTime, VideoRating
from ..models import Customer
from django.db.models import Sum


register = template.Library()

@register.simple_tag
def get_video_views(video):
    try:
        total_views = VideoWatchTime.objects.filter(video_id=video.video_id).count()
    except:
        total_views = 0
    return total_views


@register.simple_tag()
def get_all_videos():
    return Video.objects.all()


@register.simple_tag()
def count_videos():
    return Video.objects.count()


@register.simple_tag()
def list_watch_time_all_videos():
    return Video.objects.annotate(watch_time=Sum('watch_times__total_watch_time')).order_by('video_name')


@register.simple_tag()
def sum_watch_time():
    return VideoWatchTime.objects.aggregate(Sum('total_watch_time'))['total_watch_time__sum']


@register.simple_tag()
def sum_video_watch_time(video):
    try:
        watch_time = VideoWatchTime.objects.filter(video_id=video).aggregate(Sum('total_watch_time'))['total_watch_time__sum']
    except:
        watch_time = 0
    return watch_time



@register.simple_tag()
def sum_user_video_watch_time(video, user):
    try:
        customer = Customer.objects.get(user=user.id)
        watch_time = VideoWatchTime.objects.filter(video_id=video, customer_id=customer.id).aggregate(Sum('total_watch_time'))['total_watch_time__sum']
    except:
        watch_time = 0
    return watch_time



@register.simple_tag()
def count_customers():
    return Customer.objects.count()


@register.inclusion_tag('ratings.html')
def show_ratings(video):
    rating = VideoRating.objects.get(video_id=video)
    return {'rating': rating}