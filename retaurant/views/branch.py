from django.http import request
from django.http.request import HttpRequest
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render
from ..models import Branch, Restaurant,OrderItem,Order,Food,MenuItem
from django.views.generic import DetailView,ListView,DeleteView,UpdateView
from django.db.models import Avg,Sum,Max,Min,Count, fields, manager
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from ..decorators import *
from django.core import serializers
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.template.loader import render_to_string
import operator
from django.contrib.auth.decorators import user_passes_test

# ------------------------------------------------------------------------

@method_decorator([login_required, site_admin_required], name='dispatch')
class BranchList(ListView):
    model = Restaurant


# ------------------------------------------------
@method_decorator([login_required, site_admin_required], name='dispatch')
class BranchDeleteView(LoggedInRedirectMixin,ISAdminRedirectMixin,DeleteView):
    model = Branch
    success_url = reverse_lazy('branch_list')
    template_name = 'manager/delete_branch.html'

# ------------------------------------------------
@method_decorator([login_required, admin_restaurant_manager_required], name='dispatch')
class BranchUpdateView(LoggedInRedirectMixin,UpdateView):
    model = Branch
    template_name = 'manager/branch_edit.html'
    fields = ['name','address','category']
    success_url = reverse_lazy('branch_list')

# @user_passes_test(operator.attrgetter('is_restaurant_manager'), 
# login_url='/login',redirect_field_name='login')
def branch_menu_item(request):
    print(request.user.is_authenticated)
    if request.user.is_authenticated :
        if request.user.is_restaurant_manager:     
            branch = Branch.get_branche_by_manager_email(request.user.email)
            food_list = MenuItem.objects.filter(branch=branch)
        
            return render(request,'manager/branch_menu_item_list.html',context={'food_list': food_list})
    return render(request,'login.html')    
# ------------------------------------------------------------------------------------
# OK
@login_required
@user_passes_test(operator.attrgetter('is_restaurant_manager'), 
login_url='/login',redirect_field_name='login')
def branch_orders(request):
    if request.method == 'GET'  and request.is_ajax():
        branch = Branch.get_branche_by_manager_email(request.user.email)
        orders_id = OrderItem.objects.filter(food__branch=branch).only('order_id').distinct()
        orders = Order.objects.filter(id__in=orders_id).values(
            'costumer__first_name','costumer__last_name','address','costumer__phone_number','created_at',
            'status__status','total_price'
        )
        a = []
        for item in orders :
            a.append(item)
        print(a)
        print('------------------------------')
        print(orders)
        print('------------------------------')
        # data = json.dumps(list(orders), cls=DjangoJSONEncoder)
        branch = Branch.get_branche_by_manager_email(request.user.email)
        orders_id = OrderItem.objects.filter(food__branch=branch).only('order_id').distinct()
        orders = Order.objects.filter(id__in=orders_id).all()
        # data = json.dumps(list(orders), cls=DjangoJSONEncoder)
        data =  serializers.serialize(a)
        # data = serializers.serialize('json', orders)
        print(88888888,data)
        if orders:
            return JsonResponse({'order_list':data})
        else:
            return JsonResponse({'order_list': [],'msg' : "doesn't match any files",
     
        })
    elif request.method == 'GET' and not request.is_ajax():
        branch = Branch.get_branche_by_manager_email(request.user.email)
        orders_id = OrderItem.objects.filter(food__branch=branch).values_list('order_id').distinct()
        orders = Order.objects.filter(id__in=orders_id).order_by('status')
        return render(request,'manager/branch_orders.html', context={'order_list':orders})

    return render(request,'manager/branch_orders.html')
    # return render(request,'retaurant/branch_orders.html', context={'order_list':orders})
# ------------------------------------------------------------------------------------
# Not Used
def branch_orders_0(request):
    if request.method == 'GET'  and request.is_ajax():
        branch = Branch.get_branche_by_manager_email(request.user.email)
        orders_id = OrderItem.objects.filter(food__branch=branch).values_list('order_id').distinct()
        orders = Order.objects.filter(id__in=orders_id)
        ser_orders=serializers.serialize("json", orders)
        # list(orders.values_list())
        if orders:
            return JsonResponse({'order_list':ser_orders})
        else:
            return JsonResponse({
            'order_list': [],
            'msg' : "doesn't match any files",
            
        })
    elif request.method == 'GET' and not request.is_ajax():
        branch = Branch.get_branche_by_manager_email(request.user.email)
        orders_id = OrderItem.objects.filter(food__branch=branch).values_list('order_id').distinct()
        orders = Order.objects.filter(id__in=orders_id)
        return render(request,'manager/branch_orders.html', context={'order_list':orders})

    # orders = OrderItem.objects.all().values('food__branch__restaurant')
    # print(orders_id)
    # return HttpResponse(orders)
    return render(request,'manager/branch_orders.html')
    # return render(request,'retaurant/branch_orders.html', context={'order_list':orders})
# ----------------------------------------------------------------------------
# Ajax
def branch_ordered_orders(request):
    branch = Branch.get_branche_by_manager_email(request.user.email)
    orders_id = OrderItem.objects.filter(food__branch=branch).values_list('order_id').distinct()
    orders = Order.objects.filter(id__in=orders_id).filter(status__status='ordered')
    t= render_to_string('manager/branch_orders_list.html',{'order_list': orders})
    return JsonResponse({'data': t})
# ------------------------------------------------
# Ajax 
def branch_sent_orders(request):
    branch = Branch.get_branche_by_manager_email(request.user.email)
    orders_id = OrderItem.objects.filter(food__branch=branch).values_list('order_id').distinct()
    orders = Order.objects.filter(id__in=orders_id).filter(status__status='sent')
    t= render_to_string('manager/branch_orders_list.html',{'order_list': orders})
    return JsonResponse({'data': t})
    
# ------------------------------------------------
# Ajax
def branch_delivered_orders(request):
    branch = Branch.get_branche_by_manager_email(request.user.email)
    orders_id = OrderItem.objects.filter(food__branch=branch).values_list('order_id').distinct()
    orders = Order.objects.filter(id__in=orders_id).filter(status__status='delivered')
    t= render_to_string('manager/branch_orders_list.html',{'order_list': orders})
    return JsonResponse({'data': t})    
# ------------------------------------------------
# Ajax
def branch_orders_date_sort(request):
    branch = Branch.get_branche_by_manager_email(request.user.email)
    orders_id = OrderItem.objects.filter(food__branch=branch).values_list('order_id').distinct()
    orders = Order.objects.filter(id__in=orders_id).order_by('-created_at')
    t= render_to_string('manager/branch_orders_list.html',{'order_list': orders})
    return JsonResponse({'data': t})


# ------------------------------------------------
# Ajax
def all_orders(request):
    print(request.user.email)
    branch = Branch.get_branche_by_manager_email(request.user.email)
    orders_id = OrderItem.objects.filter(food__branch=branch).values_list('order_id').distinct()
    orders = orders = Order.objects.filter(id__in=orders_id)
    t= render_to_string('manager/branch_orders_list.html',{'order_list': orders})
    return JsonResponse({'data': t})

# ------------------------------------------------
# Not Used
def sent_orders(request):
    print(request.user.email)
    branch = Branch.get_branche_by_manager_email(request.user.email)
    orders_id = OrderItem.objects.filter(food__branch=branch).values_list('order_id').distinct()
    orders = orders = Order.objects.filter(id__in=orders_id).filter()
    print(orders)
    t= render_to_string('manager/branch_orders_list.html',{'order_list': orders})
    return JsonResponse({'data': t})