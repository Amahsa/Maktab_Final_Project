from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import render
from ..models import Branch, Restaurant,OrderItem,Order,Food,MenuItem
from django.views.generic import DetailView,ListView,DeleteView
from django.db.models import Avg,Sum,Max,Min,Count
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from ..decorators import site_admin_required

class RestaurantList(ListView):
    model = Restaurant

@method_decorator([login_required, site_admin_required], name='dispatch')
class RestaurantDeleteView(DeleteView):
    model = Restaurant
    success_url = reverse_lazy('restaurant_list')
    template_name = 'retaurant/delete_restaurant.html'


def restaurant_branches(request,pk):
    obj = Restaurant.objects.get(pk=pk)
    
    mydictionary = {
        "restaurant" : obj.name,
        "branch_list" : obj.branchs.all(),
    }
    return render(request,'retaurant/branch_list.html',context=mydictionary)


# -------------------------------------------------
def test_popular_in_total2(req):
    qqqq = OrderItem.objects.\
    exclude(order__status__status='ثبت نشده').values('food').\
    annotate(Sum('order_count')).\
    values_list('food',flat=True).\
        order_by('-order_count__sum')[:10]
    
    foods = MenuItem.objects.filter(id__in=qqqq )
    print(foods)
    print(4,qqqq)
    return render(req,'retaurant/popular_foods_list.html',context={'food_list':foods})

#---------------------------------------------

def test_popular_each_restaurant(req,pk):
    qqqq = OrderItem.objects.\
    exclude(order__status__status='ثبت نشده').filter(food__branch=pk).\
        values('food__branch__name','food__branch__restaurant__name').\
    annotate(Sum('order_count')).\
        values_list('food',flat=True).\
        order_by('-order_count__sum')[:10]
    
    foods = MenuItem.objects.filter(id__in=qqqq )
    print(foods)
    print(4,qqqq)
    # return HttpResponse(foods)
    return render(req,'retaurant/popular_foods_list.html',context={'food_list':foods})
#---------------------------------------------
def test_popular_restaurants(req):
     
    qqq = OrderItem.objects.\
    exclude(order__status__status='ثبت نشده').\
        values('food__branch__name','food__branch__restaurant__name').\
    annotate(Sum('order_count')).\
        values_list('food__branch',flat=True).\
        order_by('-order_count__sum')[:10]
    branchs = Branch.objects.filter(id__in=qqq )
    print(qqq)
    return render(req,'retaurant/popular_branch_list.html',context={'branch_list':branchs})

#-------------------------------------------------------------------------

# def popular_foods(request):

#     listt = []
#     for branch in Branch.objects.all():
#         mydict = {}
#         q1 = branch.menu_items().all()
#         for item in q1:
#             q2 = OrderItem.objects.filter(food=item).aggregate(Sum('order_count'))
#             mydict[item] = q2['order_count__sum']
#         listt.append(mydict)
    
#     print(4444,listt)


    # print(222,MenuItem.objects.filter(food=OrderItem.objects.values('food').
    # annotate(Sum('order_count')).order_by('-order_count__sum')[:10]))
    # print(3333,OrderItem.objects.values('food').
    # annotate(Sum('order_count')).order_by('-order_count__sum'))

    # mydictionary = {
    #     'food_list' : OrderItem.objects.values('food').
    # annotate(Sum('order_count')).order_by('-order_count__sum')[:10]
    #     #  MenuItem.objects.values('food').annotate(Count(
    #     #     'food_order_items')).order_by('-food_order_items__count')[:10]
        
    # }
    # return render(request,'retaurant/popular_foods_list.html',context=mydictionary)

# def popular_foods2(request):


#     mydict = {}
#     # print(222,OrderItem.objects.annotate().aggregate(Sum('order_count')))
#     # print(222,OrderItem.objects.values('food').
#     # annotate(Sum('order_count')).order_by('-order_count__sum').query())



#     for item in MenuItem.objects.all():
#         q = OrderItem.objects.filter(food=item).aggregate(Sum('order_count'))
#         if q['order_count__sum'] == None :

#             mydict[item] = 0
#         else : 
#             mydict[item] = q['order_count__sum']
#         print(item)
#         # print(OrderItem.objects.values('order_count').filter(food=item))
#         print(OrderItem.objects.filter(food=item).aggregate(Sum('order_count')))
#         # .aggregate(Sum('oreder_items'))
#     print('---------------------------------')
#     print(mydict)



#     q1 = Order.objects.annotate(item_count=Count('order_items')).annotate(sum=Sum('order_items__order_count')).all()
#     print(11,q1)
#     # for item in q1 :
#         # print(item.order_items)
#     print(12,Order.objects.aggregate(item_count=Count('order_items')))
#     print(OrderItem.order)
#     print(MenuItem.food_order_items)

#     # orders_items = []
#     # for item in Order.objects.all():
#     #      orders_items.append(item)
#     #     # print(1 , item.order_items.all())
#     # for item in orders_items :
#     #     for order in item.all() :
#     #         print(order.food.all())

    

#     print(Order.objects.all())
#     print(MenuItem.objects.all())
#     print(OrderItem.objects.annotate(sum=Sum('order_count')).values('order_count'))
#     # print(MenuItem.objects.)

#     # print(MenuItem.objects.annotate(c=Count('food_order_items')))
#     print(3,MenuItem.objects.annotate(Count(
#             'food_order_items')).order_by('-food_order_items__count'))
#     print(MenuItem.objects.values('food').annotate(Count(
#             'food_order_items')).order_by('-food_order_items__count'))

#     mydictionary = {
#         'food_list1' : MenuItem.objects.values('food').annotate(Count(
#             'food_order_items')).order_by('-food_order_items__count')[:10],

#         #  p = Category.objects.values('category_name').annotate(
#         #     Count('category')).order_by('-category__count')[:3]

#         'order_items' :Order.objects.filter(status__status = 'سفارش'),

#         'food_list2' : OrderItem.objects.exclude(order__status__status = 'ثبت نشده').
#         annotate(Count(
#             'food')).order_by('-food__count')[:10],

#         'food_list3' : MenuItem.objects.values('food').annotate(Count(
#             'food_order_items')).order_by('-food_order_items__count')[:10],
        
#         # Question.objects.annotate(avg_votes=Avg('choice__votes'))

#         # 'restaurant_list3' : OrderItem.objects.filter(order_status__eq = 'done').
#         # annotate(Count(
#         #     'food_branch')).order_by('-food_branch__count')[:10]
        
#     }
#     return render(request,'retaurant/popular_foods_list.html',context=mydictionary)
# # def popular_foods(List):
# #     # print('inside veiews popular_categories func')
# #     # if req.method == 'GET'  and req.is_ajax():
# #         p = Category.objects.values('category_name').annotate(
# #             Count('category')).order_by('-category__count')[:3]

# #         if p:
# #             return JsonResponse({
# #             'categories':list(p.values_list())
# #         })
# #     else:
# #         return JsonResponse({
# #             'categories': [],
# #             'msg' : "doesn't match any files",
            
# #         })

# #     return render(req,'todo/category_list.html',{
# #         'test' : "testtttt"
# #     })

# def test_popular_in_total(req):
    #     q = OrderItem.objects.exclude(order__status__status='ثبت نشده').\
#     values('food__food__name')
#     qq = OrderItem.objects.\
#     exclude(order__status__status='ثبت نشده').\
#     annotate(Sum('order_count')).\
#     values('food__food__name')
#     print(q)
#     print(qq)

#     qqq = OrderItem.objects.\
#     exclude(order__status__status='ثبت نشده').values('food').\
#     annotate(Sum('order_count')).\
#     values('food__food__name','food__branch__name','food__branch__restaurant__name').\
#         order_by('-order_count__sum')[:10]

#     qqqq = OrderItem.objects.\
#     exclude(order__status__status='ثبت نشده').values('food').\
#     annotate(Sum('order_count')).\
#     values_list('food',flat=True).\
#         order_by('-order_count__sum')[:10]
    
#     foods = MenuItem.objects.filter(id__in=qqqq )
#     print(foods)
#     print(4,qqqq)
#     return HttpResponse(qqqq)
#     # render(req,'retaurant/popular_foods_list.html')

# def test_popular_each_restaurant(req):
#     # q = OrderItem.objects.exclude(order__status__status='ثبت نشده').\
#     # values('food__food__name')
#     # qq = OrderItem.objects.\
#     # exclude(order__status__status='ثبت نشده').\
#     # annotate(Sum('order_count')).\
#     # values('food__food__name')

#     qqq = OrderItem.objects.\
#     exclude(order__status__status='ثبت نشده').\
#         values('food__branch__name','food__branch__restaurant__name').\
#     annotate(Sum('order_count')).\
#     values('food__food__name','food__branch__name',
#     'food__branch__restaurant__name').\
#         order_by('-order_count__sum')[:10]
#     # print(q)
#     # print(qq)
#     print(qqq)
#     return HttpResponse(qqq)

# def test_popular_restaurants(req):
 
#     qqq = OrderItem.objects.\
#     exclude(order__status__status='ثبت نشده').\
#         values('food__branch__name','food__branch__restaurant__name').\
#     annotate(Sum('order_count')).\
#         order_by('-order_count__sum')[:10]
#     print(qqq)
#     return HttpResponse(qqq)

