from django import forms
from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm

class CustomRegistrationForm(UserCreationForm):
    USER_TYPES = (
        ('patient', 'Patient'),
        ('admin', 'Admin'),
        ('doctor', 'Doctor'),
    )
    user_type = forms.ChoiceField(choices=USER_TYPES, label="User Type")

    class Meta:
        model = CustomUser
        fields = ("username", "password1", "password2", "user_type")

        

