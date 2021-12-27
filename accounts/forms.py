from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import *


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm): 
        model = CustomUser 
        fields = ('email', 'age',)


class CustomUserChangeForm(UserChangeForm):
    class Meta: 
        model = CustomUser
        fields = ('email', 'age',) 