from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db.models import manager
from orderonline.models import *
from .models import * 
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password


class CostumerSignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    state = forms.CharField(required=True)
    city = forms.CharField(required=True)
    street = forms.CharField(required=True)
    pluque = forms.IntegerField(required=True,min_value=1) 
    class Meta:
        model = Customer
        fields = ("username", "email", "password1", "password2","state","city","street","pluque")
        widgets = { 
             'password': forms.PasswordInput(), 
                } 

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']

        if commit:
            user.save()
        return user

class ManagerSignUpForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    username = forms.CharField(required=True)
    password = forms.CharField(required=True,widget=forms.PasswordInput)
    password2 = forms.CharField(required=True,widget=forms.PasswordInput)
    class Meta:
        model = RestaurantBranch
        fields = ("username", "email", "password", "password2","food_category","restaurant_id","restaurant_branch_name","address","restaurant_branch_description","restaurant_branch_status","is_main_branch")
        widgets = { 
             'password': forms.PasswordInput(), 
             'password2': forms.PasswordInput(),
                } 

    def save(self, commit=True):
        email = self.cleaned_data['email']
        username = self.cleaned_data['username']
        password = make_password(self.cleaned_data['password'])
        manager = RestaurantManager.objects.create(username = username, password = password,email  = email)
        manager.save()
        restaurant_branch_name = self.cleaned_data["restaurant_branch_name"]
        food_category = self.cleaned_data['food_category']
        restaurant_id = self.cleaned_data['restaurant_id']
        address = self.cleaned_data['address']
        restaurant_branch_description = self.cleaned_data['restaurant_branch_description']
        restaurant_branch_status = self.cleaned_data['restaurant_branch_status']
        is_main_branch = self.cleaned_data['is_main_branch']
        branch = RestaurantBranch.objects.create(food_category=food_category,address=address,restaurant_id=restaurant_id,restaurant_branch_name=restaurant_branch_name,restaurant_branch_description=restaurant_branch_description,manager=manager,is_main_branch=is_main_branch,restaurant_branch_status=restaurant_branch_status)
        branch.save()