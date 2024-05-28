from django import forms
from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import EmailValidator


    
class CustomRegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = CustomUser
        fields = ("username", "email", "password1", "password2")
        
    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'doctor'
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class PatientCreationForm(UserCreationForm):
    class Meta:
        #Specify model and fields to include in our form
        model = CustomUser
        fields = ("username", "password1", "password2")


class PatientEditForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['name', 'surname', 'email', 'age', 'pathology_details', 'number_objects', 'remote_difficulty']


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['age'].widget.attrs['min'] = 0
        self.fields['number_objects'].widget.attrs['min'] = 1
        self.fields['remote_difficulty'].widget.attrs['min'] = 1
        self.fields['remote_difficulty'].widget.attrs['max'] = 3
        self.fields['email'].validators.append(EmailValidator(message='Please enter a valid email address.'))

