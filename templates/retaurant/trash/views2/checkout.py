from django.shortcuts import render, redirect

from accounts.models import Customer,CustomUser,Address,CustomerAddress
from django.views import View

from ..models import MenuItem,OrderItem,Order,Status



class CheckOut(View):

    
    
    def post(self, request):

        address = CustomerAddress.objects.get(pk=request.POST.get('address_id'))
        print(1111111111111111,address)
        phone = request.POST.get('phone')


        # customer = CustomUser.objects.get(pk=8)
        customer = request.user
        print(11111110000011111,customer)
        # print(111111 , customer.is_customer)
        # customer = request.session.get('customer') # -----------------------

        cart = request.session.get('cart')
        total_price=request.POST.get('total_price')
        print(2222222222222,total_price)
        print(customer)
        products = MenuItem.get_products_by_id(list(cart.keys()))

        print(address, phone, customer, cart, products)
        print(2222, CustomUser.objects.get(pk=customer.id))
        order = Order(
                     costumer= Customer.objects.get(pk=customer.id),
                    #   costumer = customer,
                      address = address,
                      status = Status.objects.get(pk=2),
                      total_price= total_price
        )
        order.save()
        for product in products:
            new_quantity = product.count - cart.get(str(product.id))
            MenuItem.objects.filter(pk=product.id).update(count=new_quantity)
            order_item = OrderItem(
                   order=order,
                   food = product,
                   order_count =  cart.get(str(product.id)),
            )
            order_item.save()
            
            
            
            # print(cart.get(str(product.id)))
            # order = Order(costumer=Customer(id=customer),
            #               product=product,
            #               price=product.price,
            #               address=address,
            #               phone=phone,
            #               quantity=cart.get(str(product.id)))
            # order.save()

        request.session['cart'] = {}

        return redirect('cart')
