from django.shortcuts import render , redirect , HttpResponseRedirect
# from store.models.product import Products
# from store.models.category import Category
from django.contrib import messages
from ..models import Branch, MenuItem
from ..models import Category
from django.views import View
from ..models import MenuItem
from ..models import OrderItem,MenuItem
from django.db.models import Avg,Sum,Max,Min,Count


# Create your views here.
class Index(View):

    def post(self , request):
        if request.POST.get('clean_cart'):
           
            print(request.POST.get('clean_cart'))
            cart = {}

        else:

            product = request.POST.get('product')
            
            new_quantity= int(request.POST.get('quantity'))

            print(new_quantity)
            # print(3333,product)
            food = MenuItem.objects.get(pk=product)
            branch = food.branch.id

            # print(4444,food.count)
            # remove = request.POST.get('remove')
            # cleane_cart = request.POST.get('clean_cart')
            cart = request.session.get('cart')


            if cart:
                # print(999,request.session['shoping_branch'])
                if  request.session['shoping_branch'] == branch:
                    # print(cart)
                    # quantity = cart.get(product) 
                    # if quantity:
                        # if remove:
                        if new_quantity < 1:
                            cart.pop(product)
                        # else:
                        #     cart[product]  = quantity-1
                        elif new_quantity <= food.count:
                            cart[product]  = new_quantity
                            messages.add_message(request, messages.SUCCESS,
                             'Added to your Cart')
                        elif new_quantity > food.count:
                            messages.add_message(request, messages.WARNING,
                             'The number of your orders is more than the desired food inventory')

                        # else:
                        #     cart[product] = new_quantity
                        #     messages.add_message(request, messages.SUCCESS, 'Added to Cart')
                else:
                    messages.add_message(request, messages.WARNING, 'You can not buy from several restaurants at the same time')  
                    message='Save complete'
            else:
                cart = {}
                cart[product] = new_quantity
                request.session['shoping_branch'] = branch
                messages.add_message(request, messages.SUCCESS,
                             'Added to your Cart')
                


# -------------------------------------------------------------------
        request.session['cart'] = cart
        print(111111111,request.POST.get('branch_id'))
        print(444444444444444,request.POST.get('cart'))
        # print('cart' , request.session['cart'])
        # next = request.POST.get('next', '/')
        # request.META.get('HTTP_REFERER')
        # return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        # next = request.POST.get('next', '/')
        # return HttpResponseRedirect(next)
        if request.POST.get('homepage'):
            return redirect('homepage')
        elif request.POST.get('cart'):
            return redirect('cart')
        else :
            return redirect('restaurant_menu',pk=request.session.get('shoping_branch'))
            
# -------------------------------------------------------------------


    def get(self , request):
        # print()
        return HttpResponseRedirect(f'/store{request.get_full_path()[1:]}')



def store(request):
    cart = request.session.get('cart')
    if not cart:
        request.session['cart'] = {}
    products = None

    # ---------------------------- Filters ------------------------------------------
    
    categories = Category.get_all_categories() # add category filters 
    categoryID = request.GET.get('category')
    branchs = Branch.get_all_branches() # add category filters 
    branch_id = request.GET.get('branch')

    qqqq = OrderItem.objects.\
    exclude(order__status__status='unordered').values('food').\
    annotate(Sum('order_count')).\
    values_list('food',flat=True).\
        order_by('-order_count__sum')[:10]
    
    popular_food_list = MenuItem.objects.filter(id__in=qqqq )

    data = {}

    if categoryID :  
        if categoryID.isnumeric() :
            products = MenuItem.get_all_products_by_categoryid(categoryID)
            cat_instance = Category.objects.get(pk=categoryID)
            category_name = cat_instance.name
            data['category'] = category_name
        elif categoryID == 'all':
            products = MenuItem.get_all_products();
            data['category'] = 'All Foods'
        else :
            products = popular_food_list
            data['category'] = 'Best Seller Foods'
        
    elif branch_id:
        products = MenuItem.get_all_products_by_branch_id(branch_id)     
    
    else:
        products = popular_food_list
        data['category'] = 'Best Seller Foods'


    
    # print(77777,products)


    
    data['products'] = products
    data['categories'] = categories
    # ----------------------------------------------------------------------

    # ----------------------------------- Branches -----------------------------------
    data['branchs'] = branchs
    # ----------------------------------------------------------------------

    # popular_foods= restaurant.test_popular_in_total2()



    


    qqq = OrderItem.objects.\
    exclude(order__status__status='unordered').\
        values('food__branch__name','food__branch__restaurant__name').\
    annotate(Sum('order_count')).\
        values_list('food__branch',flat=True).\
        order_by('-order_count__sum')[:10]
    branchs = Branch.objects.filter(id__in=qqq )


    data['popular_branch_list'] = branchs

    

    # print('you are : ', request.session.get('email')) # ------------
    print('you are : ', request.user)
    return render(request, 'index.html', data)


