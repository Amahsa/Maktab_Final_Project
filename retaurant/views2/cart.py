from django.shortcuts import render , redirect

from django.contrib.auth.hashers import  check_password
from accounts.models import Customer
from django.views import  View
from ..models import MenuItem

class Cart(View):

    def get(self , request):
        # if request.user:
        #     addresses = Customer.address
        #     for address in addresses:
        #         print('addresses : ' , address)
        products = ''
        if request.session['cart']:
            ids = list(request.session.get('cart').keys()) 
            products = MenuItem.get_products_by_id(ids)
            print(products)
        return render(request , 'cart.html' , {'products' : products} )


