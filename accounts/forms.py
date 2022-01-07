from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
# from django.contrib.auth.models import User
# from django.contrib.auth import get_user_model
# User = get_user_model()
from .models import *
from django.db import transaction

#---------------------------------------------------
class AdminChangeForm(UserChangeForm):
    class Meta: 
        model = Admin
        fields = ('username', 'email') 

class AdminSignUpForm(UserCreationForm):
    class Meta(UserCreationForm): 
        model = Admin 
        fields = ('username', 'email')
     
    def save(self,commit=True):
        user = super().save(commit=False)
        user.is_site_admin = True
        if commit:
            user.save()
        return user
#---------------------------------------------------
class CustomUserChangeForm(UserChangeForm):
    class Meta: 
        model = Admin
        fields = ('username', 'email') 

class CustomUserSignUpForm(UserCreationForm):
    class Meta(UserCreationForm): 
        model = Admin 
        fields = ('username', 'email')
     
    def save(self,commit=True):
        user = super().save(commit=False)
        user.is_site_admin = True
        if commit:
            user.save()
        return user
#---------------------------------------------------
# class ManagerSignUpForm(UserCreationForm):
    
#     class Meta(UserCreationForm):
#         model = Manager
#         fields = ('username', 'email')

#     def save(self,commit=True):
#         user = super().save(commit=False)
#         user.is_restaurant_manager = True
#         if commit:
#             user.save()
#         return user




# class CustomerSignUpForm(UserCreationForm):
    
#     class Meta(UserCreationForm):
#         model = CustomUser
#         fields = ('username', 'email')

#     @transaction.atomic
#     def save(self):
#         user = super().save(commit=False)
#         user.is_customer = True
#         user.save()
#         student = Customer.objects.create(custom_user=user)
#         return user