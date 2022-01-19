from django.db.models import fields
from django.db.models.base import Model
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password
from django.views.generic.edit import UpdateView
from accounts.models import Customer
from django.views import View

from retaurant.views.branch import branch_orders
from ..models import MenuItem, OrderItem
from ..models import Order
from django.urls import reverse_lazy
# from ..middlewares.auth import auth_middleware
from urllib import request
from ..decorators import customer_required, restaurant_manager_required, site_admin_required
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
import operator
from django.contrib.auth.decorators import user_passes_test


class OrderView(View):
    def get(self , request ):
        # customer = request.session.get('costumer')
        customer = request.user
        orders = Order.get_orders_by_customer(customer)
        print(orders)
        return render(request , 'orders.html'  , {'orders' : orders})


@method_decorator([login_required, restaurant_manager_required], name='dispatch')
class ManagerOrderUpdatView(UpdateView):
    model = Order
    fields=['status']
    template_name = 'retaurant/manager_order_edit.html'
    success_url = reverse_lazy(branch_orders)
    

# @user_passes_test(operator.attrgetter('is_restaurant_manager'), 
# login_url='/login',redirect_field_name='login')
def order_items(request,pk):
    # order_items = OrderItem.objects.filter(order=pk)
    order_items=OrderItem.get_order_items_by_order_id(pk)
    total_price = Order.objects.filter(id=pk).values_list('total_price',flat=True)

    return render(request,'retaurant/order_items.html',context={'order_item_list': order_items,'total_price':total_price[0]})


@user_passes_test(operator.attrgetter('is_restaurant_manager'), 
login_url='/login',redirect_field_name='login')
def order_customer_info(request,pk):
    customer = Customer.objects.get(pk=pk)
    print(customer)
    return render(request,'retaurant/order_customer_info.html',context={'customer': customer})
