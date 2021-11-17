from django.db import models
from django.db.models.base import Model
# Create your models here.
class AAdmin(models.Model):
    ACCOUNT_STATUS = (
        ("ACTIVE", "Active"),
        ("DEACTIVE", "Deactive"),
    )
    Email = models.EmailField(max_length=100, unique=True)
    Password = models.CharField(max_length=100, default="Password")
    Role = models.CharField(max_length=50, default="Role")
    OTP = models.BigIntegerField(default=123456)
    Is_Verified = models.BooleanField(default=False)
    Account_Status = models.CharField(max_length=10, choices=ACCOUNT_STATUS, default="ACTIVE")
    Account_Created_Date = models.DateField(auto_now_add=True)

class FeedbackOrComplaints(models.Model):
    User_Name = models.CharField(max_length=100, default="Name")
    Email = models.EmailField(max_length=200)
    Subject = models.CharField(max_length=100, default="Feedback")
    Message = models.TextField(max_length=5000)