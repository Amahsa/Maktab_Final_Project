from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password
from accounts.models import Customer
from django.views import View
from ..models import MenuItem
from ..models import Order
# from ..middlewares.auth import auth_middleware

class OrderView(View):


    def get(self , request ):
        # customer = request.session.get('costumer')
        customer = request.user
        orders = Order.get_orders_by_customer(customer)
        print(orders)
        return render(request , 'orders.html'  , {'orders' : orders})
