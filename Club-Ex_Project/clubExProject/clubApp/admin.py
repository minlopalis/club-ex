from django.contrib import admin
from .models import Price, Customer, VideoCategory, Video, Subscription, CustomerSubscription, VideoRating, VideoWatchTime

# Register your models here.
admin.site.register(Price)
admin.site.register(Customer)
admin.site.register(VideoCategory)
admin.site.register(Video)
admin.site.register(Subscription)
admin.site.register(CustomerSubscription)
admin.site.register(VideoRating)
admin.site.register(VideoWatchTime)