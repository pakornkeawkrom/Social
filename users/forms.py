from django import forms
from django.contrib.auth import get_user_model
from .models import CustomUser

User = get_user_model()

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'profile_picture', 'bio']
