import datetime
from django.db import models
from django.utils import timezone
from django.contrib import admin
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")
    def __str__(self):
        return self.question_text
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
    @admin.display(
        boolean=True,
        ordering="pub_date",
        description="Published recently?",
    )
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    def __str__(self):
        return self.choice_text
    
class CustomUser(AbstractUser):
    USER_TYPES = (
        ('patient', 'Patient'),
        ('admin', 'Admin'),
        ('doctor', 'Doctor'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPES, default="patient")
    assigned_doctor = models.ForeignKey(blank=True, null=True, to='self', on_delete=models.CASCADE, default=None)
    date_joined = models.DateTimeField(default=timezone.now)
    name = models.CharField(max_length=30, blank=True, default="")
    surname = models.CharField(max_length=30, blank=True, default="")
    email = models.EmailField(blank=True, default="")
    age = models.IntegerField(blank=True, null=True, default=None)
    pathology_details = models.TextField(blank=True, default="")
    number_objects = models.IntegerField(default=5)

    def __str__(self):
        return self.username
    


class GameSession(models.Model):
    patient = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    play_date = models.DateTimeField(auto_now_add=True)
    elapsed_time = models.FloatField()  
    number_objects = models.IntegerField(default=5)

    def __str__(self):
        return f"Game Session for {self.patient.username} on {self.play_date}"






