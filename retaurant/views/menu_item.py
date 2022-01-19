from django.core.checks import messages
from django.db.models import fields
from django.shortcuts import render
from ..models import Branch, Food, MenuItem
from django.views.generic import DetailView,ListView,CreateView,UpdateView,DeleteView
from ..forms import AddMenuItemForm
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views import View
from django.http import JsonResponse 
from ..decorators import admin_restaurant_manager_required, customer_required, restaurant_manager_required, site_admin_required
import operator
from django.contrib.auth.decorators import user_passes_test

@method_decorator([login_required, site_admin_required], name='dispatch')
class MenuItemList(ListView):
    model = MenuItem


# @method_decorator([login_required, site_admin_required], name='dispatch')

# @method_decorator([login_required, customer_required], name='dispatch')
# For Customer And 
class MenuItemDetail(DetailView):
    model = MenuItem
    template_name = 'manager/menuitem_detail.html'

    def get_context_data(self, **kwargs):
        context = super(MenuItemDetail, self).get_context_data(**kwargs)
        context['path'] = self.request.POST.get('next')
        return context

        
# @method_decorator([login_required, customer_required], name='dispatch')    
class BuyMenuItem(DetailView):
    model = MenuItem
    template_name = 'manager/add_menuitem_to_cart.html'

# not used 
class AddMenuItemView(CreateView):
    model = MenuItem
    fields=['food','description','price','image','count']
    template_name = 'manager/add_menuitem1.html'

# Not used
@user_passes_test(operator.attrgetter('is_restaurant_manager'), 
login_url='/login',redirect_field_name='login')
def AddMenuItemView2(request):
    if request.method == "POST":
        form = AddMenuItemForm()
        if form.is_valid():
            menuitem = MenuItem(
                    food = form.cleaned_data['food'],
                    image = form.changed_data['image'],
                    price= form.changed_data['price'],
                    count= form.changed_data['count'],
                    description= form.changed_data['description'],
                    manager = Branch.get_branche_by_manager_email(request.user.email)
            )
            menuitem.save()
            return render (request, 'index.html')
        else:
            return JsonResponse({"error": form.errors}, status=400)
    form = AddMenuItemForm
    return render (request, 'manager/add_menuitem1.html' ,context={'form':form})      



@method_decorator([login_required, restaurant_manager_required], name='dispatch')
class AddMenuItem(View):


    def get(self, request):
        food_list = Food.objects.all
        return render (request, 'manager/add_menuitem.html' ,{'food_list': food_list})
        

    def post(self, request):
        postData = request.POST  
        error_message = None    

        food = postData.get ('food')
        # if len(Food.objects.filter(name=food)) == 0:
        #     Food.objects.create(pk=food) # 3333333333333333333333333
        description = postData.get ('description')
        price = postData.get ('price')
        # image = postData.get ('image')
        count = postData.get ('count')
        if len(request.FILES) != 0:
            image = request.FILES['image']

            # print('iiiiiiiiiiiiiiii',image)
            # validation
            value = {
                'food': Food.objects.get(pk=food),
                'description': description,
                'image': image,
                'price': price,
                'count': count,           
            }
            print(Branch.get_branche_by_manager_email(request.user.email))
            menuitem = MenuItem(
                branch= Branch.get_branche_by_manager_email(request.user.email), #======================
                food=Food.objects.get(pk=food),
                description=description,
                image=image,
                price=price,
                count=count,
                )
        
            error_message = self.validateMenuItem (menuitem)

            if not error_message :
                print (food, description, price, count)
                menuitem.save()
                # messages.seccess(request,'added   !!!!')
                # messages.INFO(request,'added   !!!!')
                return render (request, 'index.html')
                
            else :
                data = {
                    'error': error_message,
                    'values': value
                }
                return render (request, 'index.html', data)

        return render (request, 'index.html')
        

    def validateMenuItem(self, menuitem):
        error_message = None
        if (not menuitem.food):
            error_message = "Please Enter Food Name !!"
        # elif len (menuitem.price) < 4:
        #     manager = 'Huuum !!'
        # elif not menuitem.description:
        #     error_message = 'Please Enter some description'
        elif not menuitem.image :
            error_message = 'upload an image'
        # elif not menuitem.count:
        #     error_message = 'Enter count'
        # elif menuitem.count < 0:
        #     error_message = 'count must be positive'

        # if (not address.state):
        #     error_message = "Please Enter your State !!"
        # elif len (address.state) < 3:
        #     error_message = 'First State must be 3 char long or more'
        # elif not address.city:
        #     error_message = 'Please Enter your City'
        # elif len (address.city) < 3:
        #     error_message = 'Last City must be 3 char long or more'
        # elif not address.full_address:
        #     error_message = 'Enter your Full Address'
        # elif not address.full_address:
        #     error_message = 'Enter your Full Address'
        # saving manager

        return error_message




@method_decorator([login_required, restaurant_manager_required], name='dispatch')
class MenuItemDeleteView(DeleteView):
    model = MenuItem
    template_name = 'manager/menu_item_delete.html'
    success_url = reverse_lazy('branch_menu')

@method_decorator([login_required, admin_restaurant_manager_required], name='dispatch')
class MenuItemUpdateView(UpdateView):
    model = MenuItem
    template_name = 'manager/menu_item_edit.html'
    fields = ['food','price','count','image','description']
    success_url = reverse_lazy('branch_menu')


    

