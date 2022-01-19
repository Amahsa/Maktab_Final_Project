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


class Index(View):

    def post(self , request):
        if request.POST.get('clean_cart'):
           
            print(request.POST.get('clean_cart'))
            cart = {}
            # request.session['shoping_branch'] = ''

        else:
            if not request.POST.get('quantity') or request.POST.get('quantity') == '0':
                messages.add_message(request, messages.WARNING,'order count is not valid')
                return redirect('homepage')
            product = request.POST.get('product')           
            new_quantity= int(request.POST.get('quantity'))
            
            food = MenuItem.objects.get(pk=product)
            branch = food.branch.id
            cart = request.session.get('cart')

            if cart:
                if  request.session['shoping_branch'] == branch:
                        if new_quantity < 1:
                            cart.pop(product)

                        elif new_quantity <= food.count:
                            cart[product]  = new_quantity
                            messages.add_message(request, messages.SUCCESS,
                             'Added to your Cart')
                        elif new_quantity > food.count:
                            messages.add_message(request, messages.WARNING,
                             'The number of your orders is more than the desired food inventory')
        
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

        if request.POST.get('homepage'):
            return redirect('homepage')
        elif request.POST.get('cart'):
            return redirect('cart')
        else :
            return redirect('restaurant_menu',pk=request.session.get('shoping_branch'))
            
# -------------------------------------------------------------------


    def get(self , request):
        print('get get get')
        print(f'/store{request.get_full_path()[1:]}')
        return HttpResponseRedirect(f'/store{request.get_full_path()[1:]}')




def store(request):
    print('store')
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

    
    data['products'] = products
    data['categories'] = categories
    # ----------------------------------------------------------------------

    # ----------------------------------- Branches -----------------------------------
    data['branchs'] = branchs
    # ----------------------------------------------------------------------


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

