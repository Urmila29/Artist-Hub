from django.db import models
from django.db.models.base import Model
from Admin.models import *
# Create your models here.
class VVisitor(models.Model):
    admin = models.ForeignKey(AAdmin, on_delete=models.CASCADE, null=True)
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