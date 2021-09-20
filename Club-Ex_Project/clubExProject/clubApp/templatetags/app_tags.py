from django import template
from datetime import date
from ..models import Video, VideoWatchTime, VideoRating
from ..models import Customer
from accounts.models import Subscription
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
def count_videos():
    return Video.objects.count()


@register.simple_tag()
def list_watch_time_all_videos():
    return Video.objects.annotate(watch_time=Sum('watch_times__total_watch_time')).order_by('-watch_times__total_watch_time')


@register.simple_tag()
def sum_all_watch_time():
    return VideoWatchTime.objects.aggregate(Sum('total_watch_time'))['total_watch_time__sum']


@register.simple_tag()
def sum_video_watch_time(video):
    watch_time = VideoWatchTime.objects.filter(video_id=video).aggregate(Sum('total_watch_time'))['total_watch_time__sum']
    if watch_time == None:
            return 0
    return watch_time


@register.simple_tag()
def list_video_category_watch_time():
    return VideoWatchTime.objects.values('video_id__video_category__video_category').annotate(Sum('total_watch_time'))


@register.simple_tag()
def sum_user_video_watch_time(video, user):
    try:
        watch_time = VideoWatchTime.objects.filter(video_id=video, customer_id=user.customer.id).aggregate(watch_time=Sum('total_watch_time'))['watch_time']
    except:
        return 0
    return watch_time


@register.simple_tag()
def is_user_customer(user):
    try:
        Customer.objects.get(id=user.customer.id)
    except:
        return False
    return True


@register.simple_tag()
def count_customers():
    return Customer.objects.count()


@register.simple_tag()
def count_valid_user_subscriptions(user):
    try:
        return Subscription.objects.filter(customer_id=user.customer.id, renewal_date__gte=date.today()).count()
    except:
        return 0
    


@register.simple_tag()
def get_valid_user_subscription(user):
    try:
        valid_subscription = Subscription.objects.filter(customer_id=user.customer.id, renewal_date__gte=date.today()).order_by('renewal_date')
        last_subscription = Subscription.objects.filter(customer_id=user.customer.id, renewal_date__gte=date.today()).order_by('renewal_date').count()
        subscription = valid_subscription[last_subscription-1]
    except: 
        subscription = None
    return subscription