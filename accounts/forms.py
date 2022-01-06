from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import MinValueValidator
from .models import * 
class CostumerSignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = Customer
        fields = ("username", "email", "password1", "password2")
        widgets = { 
             'password': forms.PasswordInput(), 
                } 

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email'] 
        if commit:
            user.save()
        return user

class ManagerSignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = RestaurantManager
        fields = ("username", "email", "password1", "password2")
        widgets = { 
             'password': forms.PasswordInput(), 
                } 

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
