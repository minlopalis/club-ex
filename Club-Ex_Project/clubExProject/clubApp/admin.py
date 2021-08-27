from django.contrib import admin
from .models import Price,VideoCategory, Video, VideoRating, VideoWatchTime
# from .models import Customer,  Subscription, CustomerSubscription
# Register your models here.
admin.site.register(Price)
# admin.site.register(Customer)
admin.site.register(VideoCategory)
admin.site.register(Video)
# admin.site.register(Subscription)
# admin.site.register(CustomerSubscription)
admin.site.register(VideoRating)
admin.site.register(VideoWatchTime)