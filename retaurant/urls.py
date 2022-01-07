from django.contrib import admin
from django.urls import path,include
from accounts.views import *
from .views import food,customer,restaurant,category,meal,menu_item
from django.conf import settings
from django.conf.urls.static import static


from .views2.home import Index , store
from .views2.signup import Signup
from .views2.login import Login , logout
from .views2.cart import Cart
from .views2.checkout import CheckOut
from .views2.orders import OrderView
from .middlewares.auth import  auth_middleware

urlpatterns = [
    # path('', HomePageView.as_view(),name='home'),

    path('food/all/',food.FoodList.as_view(),name='foods_list'),
    path('food/add/',food.AddFoodView.as_view(),name='add_food'),
    path('food/<int:pk>/',food.FoodDetailView.as_view(),name='food_datail'),
    path('food/<int:pk>/edit',food.FoodUpdateView.as_view(),name='edite_food'),
    path('food/<int:pk>/delete',food.FoodDeleteView.as_view(),name='delete_food'),
    path('food/<int:pk>/detail',food.FoodDetailView.as_view(),name='food_detail'),


    path('menu_item/all/',menu_item.MenuItemList.as_view(),name='menu_item_list'),

    path('category/all/',category.CategoryList.as_view(),name='category_list'),
    path('category/add/',category.AddCategoryView.as_view(),name='add_category'),
    path('category/<int:pk>/delete',category.DeleteCategoryView.as_view(),name='delete_category'),

    path('meal/all/',meal.MealList.as_view(),name='meals_list'),
    path('meal/add/',meal.AddMealView.as_view(),name='add_meal'),
    path('meal/<int:pk>/delete',meal.DeleteMealView.as_view(),name='delete_meal'),
    

    path('customer/all/',customer.CustomerList.as_view(),name='customers_list'),
    path('customer/<int:pk>/',customer.get_orders_by_customer_id,name='customers_orders'),
    path('customer/<int:pk>/delete',customer.CustomerDeleteView.as_view(),name='delete_customer'),
    path('customer/<int:pk>/detail',customer.CustomerDetailView.as_view(),name='customer_details'),

    path('restaurant/all/',restaurant.RestaurantList.as_view(),name='restaurants_list'),
    path('restaurant/<int:pk>/branches/',restaurant.restaurant_branches,name='restaurant_branchs'),
    path('restaurant/<int:pk>/',menu_item.get_branch_menu,name='restaurant_menu'),
    path('restaurant/<int:pk>/delete',restaurant.RestaurantDeleteView.as_view(),name='delete_restaurant'),


    path('test/',restaurant.test_popular_in_total2,name='popular_foods'),
    path('test2/<int:pk>',restaurant.test_popular_each_restaurant,name='branch_popular_foods'),
    path('test3/',restaurant.test_popular_restaurants,name='popular_restarunts'),



    path('store', store , name='store'),
    path('', Index.as_view(), name='homepage'),
    path('signup', Signup.as_view(), name='signup'),
    path('login', Login.as_view(), name='login'),
    # path('login', login , name='login'),
    path('logout', logout , name='logout'),
    path('cart/', Cart.as_view() , name='cart'),
    # path('cart', auth_middleware(Cart.as_view()) , name='cart'),
    path('check-out', CheckOut.as_view() , name='checkout'),
    path('orders', auth_middleware(OrderView.as_view()), name='orders'),

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
