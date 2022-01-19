from django.db import models
from django.db.models import fields
from django.db.models.expressions import Value
from django.http import response
from django.http.response import HttpResponse,JsonResponse,HttpResponseForbidden
from django.shortcuts import render
from django.utils.functional import lazy

from accounts.models import CustomerAddress
from ..models import Category, Customer, Order , Branch,MenuItem,OrderItem
from django.views.generic import DetailView,ListView,UpdateView,DeleteView
from django.urls import reverse_lazy,reverse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from ..decorators import *
from ..forms import AddAddressForm,CustomerUpdateForm
from django.template.loader import render_to_string
from django.db.models import Q
import operator
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Avg,Sum,Max,Min,Count
# from django.contrib.auth.decorators import login_required

@method_decorator([login_required, site_admin_required], name='dispatch')
class CustomerList(ListView):
    model = Customer
    template_name = 'manager/customer_list.html'


# XXXXXXXXXXXXXXXXX
# For Amin Panel But XXXXXXXX
@login_required
@user_passes_test(operator.attrgetter('is_customer'), 
login_url='/login',redirect_field_name='login')
def get_orders_by_customer_id(request,pk):
    customer_order = Customer.objects.values('address__state',
    'address__city','address__full_address','created_at').get(pk=pk)
    print(11,customer_order)
   
    return render(request,'manager/customer_detail.html',context={'orders':customer_order})

@method_decorator([login_required, site_admin_required], name='dispatch')
class CustomerDetailView(DetailView):
    model = Customer
    template_name = 'manager/customer_detail.html'



@method_decorator([login_required, admin_customer_required], name='dispatch')
class CustomerUpdateView(UpdateView):
    model = Customer
    template_name = 'manager/customer_edit.html'
    
@method_decorator([login_required, site_admin_required], name='dispatch')
class CustomerDeleteView(DeleteView): 
    model = Customer
    template_name = 'manager/customer_delete.html'
    success_url = reverse_lazy('customer_list')

#--------------------------------------------------------------
# For Customer and AnonymousUser
# @user_passes_test(operator.attrgetter('is_customer'), 
# login_url='/login',redirect_field_name='login')
def branch_menu_item(request,pk):
    branch = Branch.objects.get(pk=pk)
    food_list = MenuItem.objects.filter(branch=branch)
    category_list = Category.objects.all()

    qqqq = OrderItem.objects.\
    exclude(order__status__status='unordered').filter(food__branch=pk).\
        values('food__branch__name','food__branch__restaurant__name').\
    annotate(Sum('order_count')).\
        values_list('food',flat=True).\
        order_by('-order_count__sum')[:3]
    
    # foods = MenuItem.objects.filter(id__in=qqqq )
    popular_foods = MenuItem.objects.filter(id__in=qqqq )

   
    return render(request,'customer/branch_menu_item.html',
    context={'products': food_list , 'categories' :category_list ,
     'branch':branch , 'popular_foods':popular_foods})

#--------------------------------------------------------------
# Not Used
@user_passes_test(operator.attrgetter('is_customer'), 
login_url='/login',redirect_field_name='login')
def customer_orders(request):
    customer = Customer.objects.get(pk=request.user.id)
    orders=Order.objects.filter(costumer=customer).order_by('-created_at')
    return render(request,'customer/orders.html',context={'order_list': orders})
#--------------------------------------------------------------
# Not Used
@method_decorator([login_required, admin_customer_required], name='dispatch')
class CustomerInfoUpdateView(UpdateView):
    model = Customer
    # fields=['first_name','last_name','phone_number']
    template_name = 'customer/customer_edit_info.html'

    def get_success_url(self):
        return self.request.POST.get('previous_page')
    success_url = reverse_lazy('homepage') # -------------

#--------------------------------------------------------------
# load the form
# For Customer
@login_required
@user_passes_test(operator.attrgetter('is_customer'), 
login_url='/login',redirect_field_name='login')
def customer_update_info(request):
    customer = request.user
    address_list=CustomerAddress.objects.filter(customer=customer)
    form = AddAddressForm()
    mydictionary = {
        'values':customer,
        'address_list':address_list,
        'form': form ,
        'customer':customer
    }
    return render(request, "customer/customer_edit_info.html", context=mydictionary)



#--------------------------------------------------------------
@method_decorator([login_required, customer_required], name='dispatch')
class CustomerEditView(UpdateView):

    model = Customer
    template_name = 'customer/customer_update_form.html'
    fields=['first_name','last_name','phone_number']
    # fields = ['name','category','meal']
    success_url = reverse_lazy('customer_edit_info')

    def get_object(self, queryset=None):
        return self.request.user



#--------------------------------------------------------------
@method_decorator([login_required, customer_required], name='dispatch')
class CustomerAddressEditView(UpdateView):
    model = CustomerAddress
    fields=['state','city','full_address']
    template_name = 'customer/customer_address_update_form.html'  
    success_url = reverse_lazy('customer_edit_info')




@method_decorator([login_required, customer_required], name='dispatch')
class CustomerAddressEditView2(UpdateView):
    def get_object(self):
        print('aaaaaaaaaa',self.request.POST)
        return CustomerAddress.objects.get(pk=self.request.POST.get('pk'))
        # self.kwargs['pk_or_field_name']
    # model = CustomerAddress
    fields=['state','city','full_address']
    template_name = 'customer/customer_address_update_form.html'  
    success_url = reverse_lazy('customer_edit_info')
    # def get_object(self, *args, **kwargs):
    #     print(33333333333,self.request.GET.items )
    #     obj = self.model.objects.get(pk=self.kwargs['pk'])
    #     print(11111,obj)
    #      # instead of self.request.GET or self.request.POST
    #     return obj
        
    
#--------------------------------------------------------------    

def post_address(request):
    if request.is_ajax() and request.method == "POST":
       
        form = AddAddressForm(request.POST)

        if form.is_valid():
            
            obj = form.save(commit=False)
            obj.customer = Customer.objects.get(pk=request.user.id)
            obj.save()
            
            customer = request.user
            address_list=CustomerAddress.objects.filter(customer=customer)
            t= render_to_string('customer/address_list.html',
            {'address_list': address_list ,'request':request , 'values':customer  ,'customer' :customer})
            return JsonResponse({'data': t})

        else:
            
            return JsonResponse({"error": form.errors}, status=400)

    return JsonResponse({"error": ""}, status=400)


def check_out_post_address(request):
    if request.is_ajax() and request.method == "POST":
        form = AddAddressForm(request.POST)

        if form.is_valid():

            obj = form.save(commit=False)
            obj.customer = Customer.objects.get(pk=request.user.id)
            obj.save()
            
            customer = request.user
            address_list=CustomerAddress.objects.filter(customer=customer)
            t= render_to_string('customer/address_selector.html',{'address_list': address_list})
            return JsonResponse({'data': t})
        else:          
            return JsonResponse({"error": form.errors}, status=400)

    return JsonResponse({"error": ""}, status=400)



# @method_decorator([login_required, customer_required], name='dispatch')
class EditCartItem(DetailView):
    model = MenuItem
    template_name = 'customer/edit_cart_item.html'


def delete_cart_item(request):
    cart = request.session.get('cart')
    pk = request.GET.get('pk')
    cart.pop(pk)
    request.session['cart'] = cart
    products={}
    if request.session.get('cart') :
        ids = list(request.session.get('cart').keys()) 
        products = MenuItem.get_products_by_id(ids)
    t = render_to_string('customer/cart_items_table.html' ,
     {'products':products , 'request':request})
    t2 = render_to_string('customer/cart_len.html' ,
     {'products':products , 'request':request}) 
    print(t2)
    return JsonResponse({'data': t ,'data2':t2})



def search(request):
    q = request.GET.get('q')

    if q:
        items = MenuItem.objects.filter(Q(food__name__icontains = q)
         | Q(branch__name__icontains = q)  | Q(branch__restaurant__name__icontains = q))
        category = '  Results'
    else : 
        # items = MenuItem.objects.all()
        items = {}
        category = ''
  
    t = render_to_string('customer/search.html' , 
    {'products':items , 'request':request , 'category': category })
    return JsonResponse({'data': t})



def delete_address(request):
    customer_id = request.GET.get('customer_id')
    customer = Customer.objects.get(pk=customer_id)
    pk = request.GET.get('pk')
    if len(list(CustomerAddress.objects.filter(customer=customer_id)))>=2:
        CustomerAddress.objects.filter(pk=pk).delete()
    address_list = CustomerAddress.objects.filter(customer=customer_id)
    t = render_to_string('customer/address_list_info_page.html' , {'address_list':address_list ,
     'request':request , 'values':customer ,'customer' :customer})
    return JsonResponse({'data': t})




@login_required
@user_passes_test(operator.attrgetter('is_customer'), 
login_url='/login',redirect_field_name='login')
def order_items(request,pk):
    # order_items = OrderItem.objects.filter(order=pk)
    order_items=OrderItem.get_order_items_by_order_id(pk)
    total_price = Order.objects.filter(id=pk).values_list('total_price',flat=True)

    return render(request,'manager/order_items.html',context={'order_item_list': order_items,'total_price':total_price[0]})


# AJAX
def category_foods(request):
    category_id = request.GET.get('category_id')
    data={}
    if category_id.isnumeric() :
            products = MenuItem.get_all_products_by_categoryid(category_id)
            cat_instance = Category.objects.get(pk=category_id)
            category_name = cat_instance.name
            category= category_name
    elif category_id == 'all':
            products = MenuItem.get_all_products();
            category = 'All Foods'
    else :
        qqqq = OrderItem.objects.\
        exclude(order__status__status='unordered').values('food').\
        annotate(Sum('order_count')).\
        values_list('food',flat=True).\
        order_by('-order_count__sum')[:10]

        popular_food_list = MenuItem.objects.filter(id__in=qqqq )
        products = popular_food_list
        category = 'Best Seller Foods'
            # data['category'] = 'Best Seller Foods'
    t = render_to_string('customer/category_foods.html' , {'products':products , 'category':category})
    return JsonResponse({'data': t})        
     

def customer_ordered_orders(request):
    customer = Customer.objects.get(email=request.user.email)

    orders = Order.objects.filter(costumer=customer).filter(status__status='ordered')

    t= render_to_string('customer/customer_orders_list.html',{'order_list': orders})
    return JsonResponse({'data': t})

def customer_sent_orders(request):
    customer = Customer.objects.get(email=request.user.email) 
    orders = Order.objects.filter(costumer=customer).filter(status__status='sent')
    t= render_to_string('customer/customer_orders_list.html',{'order_list': orders})
    return JsonResponse({'data': t})

def customer_delivered_orders(request):
    customer = Customer.objects.get(email=request.user.email) 
    orders = Order.objects.filter(costumer=customer).filter(status__status='delivered')
    t= render_to_string('customer/customer_orders_list.html',{'order_list': orders})
    return JsonResponse({'data': t})

