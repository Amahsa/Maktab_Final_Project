from accounts.models import CustomerAddress,Customer
from .models import Food,Category,Meal, MenuItem
from django import forms
import datetime
from django.contrib.admin.widgets import AdminDateWidget
from urllib import request


class AddMenuItemForm(forms.ModelForm):

    class Meta:
        model = MenuItem
        fields = ("food","description","image",'price','count')



class AddFoodForm(forms.ModelForm):

    class Meta:
        model = Food
        fields = ("__all__")


class AddAddressForm(forms.ModelForm):
    
    class Meta:
        model = CustomerAddress
        fields = ('state','city','full_address')
    # def __init__(self, *args, **kwargs):
    #     super(AddAddressForm, self).__init__(*args, **kwargs)
    #     self.fields['customer'].disabled = True
    #     self.fields['customer'].initial = request.user


class AddCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ("__all__")

class AddMealForm(forms.ModelForm):
    class Meta:
        model = Meal
        fields = ("__all__")


class CustomerUpdateForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['first_name', 'last_name','phone_number']