from os import truncate
from django.db import models
from django.db.models.deletion import CASCADE
import datetime
from accounts.models import Customer

# Create your models here.
# Price model
class Price(models.Model):
    onlineMonthlySub = models.IntegerField()
    onlineAnnualSub = models.IntegerField()
    gymMonthlySub = models.IntegerField()
    gymAnnualSub = models.IntegerField()


# Video Category Model
class VideoCategory(models.Model):
    video_category_id = models.AutoField(primary_key=True)
    video_category = models.CharField(max_length=200, null=False)

    def __str__(self):
        return self.video_category


# Video Model
class Video(models.Model):
    video_id = models.AutoField(primary_key=True)
    video_name = models.CharField(max_length=200, null=False)
    video_description = models.CharField(max_length=500, null=False)
    video_URL = models.URLField(max_length=500)
    videoCategory = models.ForeignKey(VideoCategory, on_delete=CASCADE, null=False)



# Video Watch Time Model
class VideoWatchTime(models.Model):
    video_id = models.ForeignKey(Video, on_delete=CASCADE, null=False, related_name="watch_times")
    video_watch_time_id = models.AutoField(primary_key=True)
    customer_id = models.ForeignKey(Customer, on_delete=CASCADE, null=False, related_name="customer_watch_times")
    videoCategory = models.ForeignKey(VideoCategory, on_delete=CASCADE, null=False) ## DO WE NEED THIS FIELD???
    total_watch_time = models.IntegerField()


# Video Ratings Model
class VideoRating(models.Model):
    video_id = models.ForeignKey(Video, on_delete=CASCADE, null=False, related_name="ratings")
    video_rating_id = models.AutoField(primary_key=True)
    customer_id = models.ForeignKey(Customer, on_delete=CASCADE, null=False, related_name="customer_ratings")
    videoCategory = models.ForeignKey(VideoCategory, on_delete=CASCADE, null=False)
    rating = models.IntegerField()