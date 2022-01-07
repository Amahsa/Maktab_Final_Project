from django.shortcuts import render , redirect
from django.contrib.auth.hashers import  check_password

# from models import Customer
from django.views import  View
from models import MenuItem


class Cart(View):
    def get(self , request):
        ids = list(request.session.get('cart').keys())
        products = MenuItem.get_menuitem_by_id(ids)
        print(products)
        return render(request , 'cart.html' , {'products' : products})


