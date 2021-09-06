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

# # Customer Model
# class Customer(models.Model):
#     customer_id = models.AutoField(primary_key=True)
#     first_name = models.CharField(max_length=50, null=False)
#     last_name = models.CharField(max_length=50, null=False)
#     address_1 = models.CharField(max_length=50, null=False)
#     address_2 = models.CharField(max_length=50, null=True, blank=True)
#     city = models.CharField(max_length=50, null=False)
#     country = models.CharField(max_length=50, null=False)
#     zip_address = models.CharField(max_length=10)
#     email = models.EmailField(max_length=100)
#     phone = models.CharField(max_length=20)

#     def __str__(self):
#         return "Customer ID: " + str(self.customer_id) + ", Customer Name: " + self.first_name + " " + self.last_name

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
    video_image_URL=models.URLField(max_length=500)
    videoCategory = models.ForeignKey(VideoCategory, on_delete=CASCADE, null=False)

# # Subscription Model
# class Subscription(models.Model):
#     subscription_id = models.AutoField(primary_key=True)
#     subscription = models.CharField(max_length=50, null=False)
#     billing_cycle_days = models.IntegerField(null=False)
#     gym_access = models.BooleanField(default=False, null=False)

# # Customer Subsription Model
# class CustomerSubscription(models.Model):
#     customer_subscription_id = models.AutoField(primary_key=True)
#     customer_id = models.ForeignKey(Customer, on_delete=CASCADE, null=False)
#     subscription_id = models.ForeignKey(Subscription, on_delete=CASCADE, null=False)
#     start_date = models.DateField(default=datetime.date.today, null=False)
#     auto_reccurring_subscription = models.BooleanField(default=True, null=False)

# Video Watch Time Model
class VideoWatchTime(models.Model):
    video_watch_time_id = models.AutoField(primary_key=True)
    customer_id = models.ForeignKey(Customer, on_delete=CASCADE, null=False)
    video_id = models.ForeignKey(Video, on_delete=CASCADE, null=False)
    videoCategory = models.ForeignKey(VideoCategory, on_delete=CASCADE, null=False)
    total_watch_time = models.IntegerField()

# Video Ratings Model
class VideoRating(models.Model):
    video_rating_id = models.AutoField(primary_key=True)
    customer_id = models.ForeignKey(Customer, on_delete=CASCADE, null=False)
    video_id = models.ForeignKey(Video, on_delete=CASCADE, null=False)
    videoCategory = models.ForeignKey(VideoCategory, on_delete=CASCADE, null=False)
    rating = models.IntegerField()