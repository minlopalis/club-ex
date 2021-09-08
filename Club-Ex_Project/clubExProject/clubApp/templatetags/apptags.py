from django import template
from ..models import Video, VideoWatchTime
from django.db.models import Sum

register = template.Library()

@register.simple_tag()
def get_all_videos():
    return Video.objects.all()

@register.simple_tag()
def count_videos():
    return Video.objects.count()

@register.simple_tag()
def sum_watch_time():
    return VideoWatchTime.objects.aggregate(Sum('total_watch_time'))['total_watch_time__sum']