from django.shortcuts import render, redirect

from django.contrib.auth.hashers import check_password
from accounts.models import Customer
from django.views import View

from models import MenuItem
from models import Order,OrderItem


class CheckOut(View):
    def post(self, request):

        address = request.POST.get('address') # 
        # address = request.POST.get('address')

        phone = request.POST.get('phone')

        customer = request.session.get('customer')#
        # customer = request.session.get('customer')

        cart = request.session.get('cart') #
        # cart = request.session.get('cart')

        products = MenuItem.get_products_by_id(list(cart.keys()))#
        # products = Products.get_products_by_id(list(cart.keys()))
        print(address, customer, cart, products)

        for product in products:
            print(cart.get(str(product.id)))
            order_item = OrderItem(
                        #   customer=Customer(id=customer),
                        #   address=address,
                          
                          food=product,
                        #   price=product.price,
                          
                        #   phone=phone,
                          order_count=cart.get(str(product.id))
                          )
            order_item.save()
        request.session['cart'] = {}

        return redirect('cart')
