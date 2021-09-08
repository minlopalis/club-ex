from django import template
from ..models import Video, VideoWatchTime, VideoRating
from ..models import Customer
from django.db.models import Sum


register = template.Library()

@register.simple_tag
def get_video_views(video):
    return VideoWatchTime.objects.filter(video_id=video.video_id).count()


@register.simple_tag()
def get_all_videos():
    return Video.objects.all()

@register.simple_tag()
def sum_watch_time_by_videos():
    return Video.objects.annotate(watch_time=Sum('watch_times__total_watch_time')).order_by('video_name')


@register.simple_tag()
def count_videos():
    return Video.objects.count()


@register.simple_tag()
def sum_watch_time():
    return VideoWatchTime.objects.aggregate(Sum('total_watch_time'))['total_watch_time__sum']


@register.simple_tag()
def count_customers():
    return Customer.objects.count()


@register.inclusion_tag('ratings.html')
def show_ratings(video=1):
    rating = VideoRating.objects.get(video_id=video)
    return {'rating': rating}