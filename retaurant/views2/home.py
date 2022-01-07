from django.shortcuts import render , redirect , HttpResponseRedirect
# from store.models.product import Products
# from store.models.category import Category
from django.contrib import messages
from ..models import Branch, MenuItem
from ..models import Category
from django.views import View
from ..models import MenuItem

# Create your views here.
class Index(View):

    def post(self , request):
        if request.POST.get('clean_cart'):
            print('rrrrrrrrr')
            print(request.POST.get('clean_cart'))
            cart = {}
        else:

            print('ffffffffffffff')

            product = request.POST.get('product')
            # print(3333,product)
            food = MenuItem.objects.get(pk=product)
            branch = food.branch.id

            # print(4444,food.count)
            remove = request.POST.get('remove')
            # cleane_cart = request.POST.get('clean_cart')
            cart = request.session.get('cart')


            if cart:
                print(999,request.session['shoping_branch'])
                if  request.session['shoping_branch'] == branch:
                    # print(cart)
                    quantity = cart.get(product) 
                    if quantity:
                        if remove:
                            if quantity<=1:
                                cart.pop(product)
                            else:
                                cart[product]  = quantity-1
                        elif quantity+1 <= food.count:
                            cart[product]  = quantity+1
                            messages.add_message(request, messages.SUCCESS,
                             'Added to your Cart')
                        else :
                            messages.add_message(request, messages.WARNING,
                             'The number of your orders is more than the desired food inventory')

                    else:
                        cart[product] = 1
                        messages.add_message(request, messages.SUCCESS, 'Added to Cart')
                    
            else:
                cart = {}
                cart[product] = 1
                request.session['shoping_branch'] = branch
                


# -------------------------------------------------------------------
        request.session['cart'] = cart
        print('cart' , request.session['cart'])
        return redirect('homepage')

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

    if categoryID:
        products = MenuItem.get_all_products_by_categoryid(categoryID)
        
    elif branch_id:
        products = MenuItem.get_all_products_by_branch_id(branch_id)     
    
    else:
        products = MenuItem.get_all_products();
    
    # print(77777,products)


    data = {}
    data['products'] = products
    data['categories'] = categories
    # ----------------------------------------------------------------------

    # ----------------------------------- Branches -----------------------------------
    

    # if branch_id:
    #     branch_foods = MenuItem.get_all_products_by_branch_id(branch_id)
    # else:
    #     branch_foods = MenuItem.get_all_products();


    # # data = {}
    # data['products'] = branch_foods
    data['branchs'] = branchs
    # ----------------------------------------------------------------------


    print('you are : ', request.session.get('email')) # ------------

    return render(request, 'index.html', data)


