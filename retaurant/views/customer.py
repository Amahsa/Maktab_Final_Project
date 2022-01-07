from django.http import response
from django.http.response import HttpResponse
from django.shortcuts import render
from django.utils.functional import lazy
from ..models import Customer, Order
from django.views.generic import DetailView,ListView,UpdateView,DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from ..decorators import site_admin_required


@method_decorator([login_required, site_admin_required], name='dispatch')
class CustomerList(ListView):
    model = Customer
    template_name = 'retaurant/customer_list.html'

   
def get_orders_by_customer_id(request,pk):
    # obj = Customer.objects.customer_orders.all()
    customer_order = Customer.objects.values('address__state',
    'address__city','address__full_address','created_at').get(pk=pk)
    # get(pk=pk).customer_orders
    print(11,customer_order)
    # print(obj)
    # return render(response,'retaurant/customer_detail.html')
    return render(request,'retaurant/customer_detail.html',context={'orders':customer_order})

@method_decorator([login_required, site_admin_required], name='dispatch')
class CustomerDetailView(DetailView):
    model = Customer
    template_name = 'retaurant/customer_detail.html'

@method_decorator([login_required, site_admin_required], name='dispatch')
class CustomerUpdateView(UpdateView):
    model = Customer
    template_name = 'retaurant/customer_edit.html'
    
@method_decorator([login_required, site_admin_required], name='dispatch')
class CustomerDeleteView(DeleteView): # new
    model = Customer
    template_name = 'retaurant/customer_delete.html'
    success_url = reverse_lazy('customer_list')
