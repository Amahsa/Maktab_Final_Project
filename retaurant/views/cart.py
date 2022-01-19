from django.shortcuts import render , redirect
from django.shortcuts import render , redirect , HttpResponseRedirect
from django.contrib.auth.hashers import  check_password
from accounts.models import Customer,CustomerAddress
from django.views import  View
from ..models import MenuItem
from ..forms import AddAddressForm
from django.contrib import messages
from ..models import Branch, MenuItem
from ..models import Category
from django.views import View
from ..models import MenuItem
from ..models import OrderItem,MenuItem
from django.db.models import Avg,Sum,Max,Min,Count

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
        return render(request , 'cart.html' , {'products' : products} )


# class Index(View):
    
#     def post(self , request):
#         if request.POST.get('clean_cart'):
           
#             print(request.POST.get('clean_cart'))
#             cart = {}

#         else:
#             if not request.POST.get('quantity') or request.POST.get('quantity') == '0':
#                 messages.add_message(request, messages.WARNING,'order count is not valid')
#                 return redirect('homepage')
#             product = request.POST.get('product')           
#             new_quantity= int(request.POST.get('quantity'))
            
#             food = MenuItem.objects.get(pk=product)
#             branch = food.branch.id
#             cart = request.session.get('cart')

#             if cart:
#                 if  request.session['shoping_branch'] == branch:
#                         if new_quantity < 1:
#                             cart.pop(product)

#                         elif new_quantity <= food.count:
#                             cart[product]  = new_quantity
#                             messages.add_message(request, messages.SUCCESS,
#                              'Added to your Cart')
#                         elif new_quantity > food.count:
#                             messages.add_message(request, messages.WARNING,
#                              'The number of your orders is more than the desired food inventory')
        
#                 else:
#                     messages.add_message(request, messages.WARNING, 'You can not buy from several restaurants at the same time')  
#                     message='Save complete'
#             else:
#                 cart = {}
#                 cart[product] = new_quantity
#                 request.session['shoping_branch'] = branch
#                 messages.add_message(request, messages.SUCCESS,
#                              'Added to your Cart')
                

#         request.session['cart'] = cart

#         if request.POST.get('homepage'):
#             return redirect('homepage')
#         elif request.POST.get('cart'):
#             return redirect('cart')
#         else :
#             return redirect('restaurant_menu',pk=request.session.get('shoping_branch'))
            

#     def get(self , request):
#         print('GET')
#         print(request.get_full_path())
#         # print(f'/store{request.get_full_path()[1:]}')
#         return HttpResponseRedirect(f'/store{request.get_full_path()[1:]}')
#         # return render(request,'index.html')

