from django.db import models
from django.db.models.base import Model
from django.db.models.deletion import CASCADE
from Visitor.models import *
from Admin.models import *
# Create your models here.
class AArtist(models.Model):
    admin = models.ForeignKey(AAdmin, on_delete=models.CASCADE, null=True)
    Profession = models.CharField(max_length=100, default="Profession")
    Firstname = models.CharField(max_length=100, default="First name")
    Lastname = models.CharField(max_length=100, default="Last name")
    Nationality = models.CharField(max_length=50, default="Country Name")
    Mobileno = models.BigIntegerField(default=123)
    Birthdate = models.DateField(auto_now_add=False)
    Currentaddr = models.CharField(max_length=255, default="Current Address")
    Permanentaddr = models.CharField(max_length=255, default="Permanent Address")
    Gender = models.CharField(max_length=10, default="Gender")
    ProfilePic = models.ImageField(upload_to="media/profile/", default="abc.png")
    Myself = models.CharField(max_length=255, default="I am....")

class BookingRequests(models.Model):
    artist = models.ForeignKey(AArtist, on_delete=models.CASCADE, null=True)
    visitor = models.ForeignKey(VVisitor, on_delete=models.CASCADE, null=True)
    Event = models.CharField(max_length=100, default="Event name")
    Place = models.CharField(max_length=200, default="Event place")
    Event_Date = models.DateField(auto_now_add=False)
    Request_Date = models.DateField(auto_now_add=True)
    Minimum_Budget = models.IntegerField(default=000)
    Maximum_Budget = models.IntegerField(default=000)
    Description = models.TextField(max_length=5000, default="About Event...")
    Status = models.CharField(max_length=15, default="Pending")
    Payment_Status = models.CharField(max_length=15, default="Pending")

class Reviews(models.Model):
    artist = models.ForeignKey(AArtist, on_delete=models.CASCADE, null=True)
    visitor = models.ForeignKey(VVisitor, on_delete=models.CASCADE, null=True)
    event = models.ForeignKey(BookingRequests, on_delete=models.CASCADE, null=True)
    On_Budget = models.BooleanField(default=True)
    On_Time = models.BooleanField(default=True)
    Rate = models.IntegerField()
    Review = models.TextField(max_length=5000, default="Your Comments....")
    Review_Created_Date = models.DateField(auto_now_add=True)
