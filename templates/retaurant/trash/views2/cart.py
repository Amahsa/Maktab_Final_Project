from django.shortcuts import render , redirect

from django.contrib.auth.hashers import  check_password
from accounts.models import Customer,CustomerAddress
from django.views import  View
from ..models import MenuItem
from ..forms import AddAddressForm

# class Cart(View):
#     def get(self , request):
#         ids = list(request.session.get('cart').keys())
#         products = MenuItem.get_menuitem_by_id(ids)
#         print(products)
#         return render(request , 'cart.html' , {'products' : products})


class Cart(View):

    def get(self , request):
        
        products = ''
        if request.session['cart']:
            form=AddAddressForm
            ids = list(request.session.get('cart').keys()) 
            products = MenuItem.get_products_by_id(ids)
            print(products)
            if request.user.is_authenticated:
                customer = Customer.objects.get(pk=request.user.id)
                addresses = CustomerAddress.objects.filter(customer=customer)
                return render(request , 'cart.html' , {'products' : products ,
                'address_list':addresses ,'form':form} )
            #     print(444444,addresses)
        return render(request , 'cart.html' , {'products' : products} )


