from django import forms
from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm

from django import forms
from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm

class CustomRegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ("username", "password1", "password2")

    def save(self, commit=True):
        # Set the user type to "doctor" when saving the form
        user = super().save(commit=False)
        user.user_type = 'doctor'
        if commit:
            user.save()
        return user
