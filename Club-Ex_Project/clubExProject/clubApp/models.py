from django.db import models

# Create your models here.
# Price model
class Price(models.Model):
    onlineMonthlySub = models.IntegerField()
    onlineAnnualSub = models.IntegerField()
    gymMonthlySub = models.IntegerField()
    gymAnnualSub = models.IntegerField()

    # def __str__(self):
    #     onlineMonthStr = str(self.onlineMonthlySub)
    #     onlineAnnualStr = str(self.onlineAnnualSub)
    #     gymMonthStr = str(self.gymMonthlySub)
    #     gymAnnualStr = str(self.onlineAnnualSub)
    #     returnString = ("online monthly: {}, online annual: {}, gym monthly: {}, gym annual: {}", onlineMonthStr, onlineAnnualStr, gymMonthStr,gymAnnualStr)