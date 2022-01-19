from django.db.models import fields
from django.db.models.base import Model
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password
from django.views.generic.edit import UpdateView
from accounts.models import Address
from accounts.models import Customer
from django.views import View

from retaurant.views.branch import branch_orders
from ..models import Branch, MenuItem, OrderItem
from ..models import Order
from django.urls import reverse_lazy
from accounts.models import Manager
# from ..middlewares.auth import auth_middleware
from urllib import request
from ..decorators import customer_required, restaurant_manager_required, site_admin_required
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
import operator
from django.contrib.auth.decorators import user_passes_test

@method_decorator([login_required, restaurant_manager_required], name='dispatch')
class OrderView(View):
    def get(self , request ):
        customer = request.user
        orders = Order.get_orders_by_customer(customer)
        print(orders)
        return render(request , 'orders.html'  , {'orders' : orders})


@method_decorator([login_required, restaurant_manager_required], name='dispatch')
class ManagerOrderUpdatView(UpdateView):
    model = Order
    fields=['status']
    template_name = 'manager/manager_order_edit.html'
    success_url = reverse_lazy(branch_orders)
    
@login_required
# @user_passes_test(operator.attrgetter('is_restaurant_manager'), 
# login_url='/login',redirect_field_name='login')
def order_items(request,pk):
    order_items=OrderItem.get_order_items_by_order_id(pk)
    total_price = Order.objects.filter(id=pk).values_list('total_price',flat=True)
    return render(request,'manager/order_items.html',context={'order_item_list': order_items,'total_price':total_price[0]})

@login_required
@user_passes_test(operator.attrgetter('is_restaurant_manager'), 
login_url='/login',redirect_field_name='login')
def order_customer_info(request,pk):
    customer = Customer.objects.get(pk=pk)
    print(customer)
    return render(request,'manager/order_customer_info.html',context={'customer': customer})


@method_decorator([login_required, restaurant_manager_required], name='dispatch')
class ManagerEditView(UpdateView):
    model = Manager
    template_name = 'restaurant/manager/manager_update_form.html'
    fields=['first_name','last_name','phone_number']
    success_url = reverse_lazy('manager_edit_page') # 000000000000

@method_decorator([login_required, restaurant_manager_required], name='dispatch')
class ManagerAddressEditView(UpdateView):
    model = Address
    fields=['state','city','full_address']
    template_name = 'restaurant/manager/manager_address_update_form.html'  
    success_url = reverse_lazy('manager_edit_page')

@method_decorator([login_required, restaurant_manager_required], name='dispatch')
class ManagerBranchEditView(UpdateView):
    model = Branch
    fields=['name',]
    template_name = 'restaurant/manager/manager_branch_update_form.html'  
    success_url = reverse_lazy('manager_edit_page')


@login_required
@user_passes_test(operator.attrgetter('is_restaurant_manager'), 
login_url='/login',redirect_field_name='login')
def manager_update_info(request):
    if request.method == 'GET':
        manager = request.user
        mydictionary = {
            'manager':manager,
            'branch' : Branch.objects.get(manager_id=manager.id)
        }
        return render(request, "restaurant/manager/manager_edit_info.html", context=mydictionary)


def change_order_status(request,pk):
    status = Order.objects.filter(pk=pk).values_list('status',flat=True)
    Order.objects.filter(pk=pk).update(status_id=status[0]+1)
    context = {}
    branch = Branch.get_branche_by_manager_email(request.user.email)
    orders_id = OrderItem.objects.filter(food__branch=branch).values_list('order_id').distinct()
    orders = Order.objects.filter(id__in=orders_id).order_by('status')

    return render(request,'manager/branch_orders.html', context={'order_list':orders})
    # order = Order.objects.filter(pk=pk).update(status_id=status_id+1)
    

