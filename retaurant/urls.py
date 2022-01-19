from django.contrib import admin
from django.urls import path,include
from accounts.views import *
from .views import food,customer,restaurant,category,meal,menu_item,branch,site_admin,manager
from django.conf import settings
from django.conf.urls.static import static


from .views.home import store , Index
# from .views.cart import Index
from .views.signup import Signup
from .views.signup_manager import ManagerSignup
from .views.signup_manager_new_branch import ManagerSignupNewBranch
from .views.login import Login , logout
from .views.cart import Cart
from .views.checkout import CheckOut
from .views.orders import OrderView,ManagerOrderUpdatView,order_items,order_customer_info
from .middlewares.auth import  auth_middleware
from .views.signup_site_admin import SiteAdminSignupView

urlpatterns = [
 

    path('site_admin/customer/all',site_admin.CustomerList.as_view(),name='customer_list'),
    path('site_admin/customer/<int:pk>/detail',site_admin.CustomerDetailView.as_view(),name='customer_detail'),
    path('site_admin/customer/<int:pk>/delete',site_admin.CustomerDeleteView.as_view(),name='delete_customer'),
    path('site_admin/customer/<int:pk>/edit',site_admin.CustomerUpdateView.as_view(),name='edit_customer'),
    
    path('site_admin/food/all',site_admin.FoodList.as_view(),name='food_list'),
    path('site_admin/food/add',site_admin.AddFoodView.as_view(),name='add_food'),
    path('site_admin/food/<int:pk>/delete',site_admin.FoodDeleteView.as_view(),name='delete_food'),
    path('site_admin/food/<int:pk>/edit',site_admin.FoodUpdateView.as_view(),name='food_edit'),
    path('site_admin/food/<int:pk>/detail',site_admin.FoodDetailView.as_view(),name='food_detail'),
    
    path('site_admin/restaurant/all',site_admin.RestaurantList.as_view(),name='restaurant_list'),
    path('site_admin/restaurant/<int:pk>/edit',site_admin.RestaurantUpdateView.as_view(),name='restaurant_edit'),
    path('site_admin/restaurant/<int:pk>/delete',site_admin.RestaurantDeleteView.as_view(),name='delete_restaurant'),
    path('site_admin/restaurant/branch/<int:pk>',site_admin.restaurant_branches,name='restaurant_branch'),
    path('site_admin/restaurant/branch/<int:pk>/branch_menu',site_admin.branch_menu,name='restaurant_branch_menu'),
    path('site_admin/restaurant/branch/<int:pk>/edit',site_admin.BranchUpdateView.as_view(),name='restaurant_branch_edit'),
    path('site_admin/restaurant/branch/<int:pk>/delete',site_admin.BranchDeleteView.as_view(),name='restaurant_branch_delete'),

    path('site_admin/meal/all',site_admin.MealList.as_view(),name='meal_list'),
    path('site_admin/meal/<int:pk>/edit',site_admin.MealUpdateView.as_view(),name='meal_edit'),
    path('site_admin/meal/<int:pk>/delete',site_admin.DeleteMealView.as_view(),name='delete_meal'),
    path('site_admin/meal/add',site_admin.AddMealView.as_view(),name='add_meal'),
    

    path('site_admin/category/all',site_admin.CategoryList.as_view(),name='category_list'),
    path('site_admin/category/<int:pk>/edit',site_admin.CategoryEditView.as_view(),name='category_edit'),
    path('site_admin/category/<int:pk>/delete',site_admin.DeleteCategoryView.as_view(),name='delete_category'),
    path('site_admin/category/add',site_admin.AddCategoryView.as_view(),name='add_category'),

    path('site_admin/manager/all',site_admin.ManagerListView.as_view(),name='manager_list'),
    path('site_admin/manager/<int:pk>/edit',site_admin.ManagerEditView.as_view(),name='manager_edit'),
    path('site_admin/manager/<int:pk>/delete',site_admin.ManagerDeleteView.as_view(),name='delete_manager'),

    path('manager/edit',manager.manager_update_info,name='manager_edit_page'),
    path('manager/<int:pk>/update_info/',manager.ManagerEditView.as_view(),name='manager_update_info'),
    path('manager/address/<int:pk>/update/',manager.ManagerAddressEditView.as_view(),name='manager_update_address'),
    path('manager/branch/<int:pk>/update/',manager.ManagerBranchEditView.as_view(),name='manager_update_branch'),
    path('manager/branch/order/<int:pk>/update_status/',manager.change_order_status,name='manager_update_order_status'),



    path('menu_item/all/',menu_item.MenuItemList.as_view(),name='menu_item_list'),
    path('menu_item/<int:pk>/detail',menu_item.MenuItemDetail.as_view(),name='menu_item_detail'),
    path('menu_item/add/', menu_item.AddMenuItem.as_view(), name='add_menu_item'),
    path('menu_item/<int:pk>/delete', menu_item.MenuItemDeleteView.as_view(), name='delete_menu_item'),
    path('menu_item/<int:pk>/edit', menu_item.MenuItemUpdateView.as_view(), name='edit_menu_item'),
    path('menu_item/<int:pk>/buy', menu_item.BuyMenuItem.as_view(), name='add_menu_item_to_cart'),


    path('customer/all/',customer.CustomerList.as_view(),name='customers_list'),
    path('customer/<int:pk>/',customer.get_orders_by_customer_id,name='customers_orders'),
    # path('customer/<int:pk>/delete',customer.CustomerDeleteView.as_view(),name='delete_customer0'),
    path('customer/<int:pk>/detail',customer.CustomerDetailView.as_view(),name='customer_details'),
    path('restaurant/<int:pk>/menu_item',customer.branch_menu_item , name='restaurant_menu'),
    path('customer/orders',customer.customer_orders,name='customer_orders'),
    path('customer/edit_info',customer.customer_update_info,name='customer_edit_info'),
    path('customer/post_address',customer.post_address,name='post_address'),
    path('customer/check_out_post_address',customer.check_out_post_address,name='check_out_post_address'),
    path('customer/edit_cart_item/<int:pk>',customer.EditCartItem.as_view(),name='edit_cart_item'),
    path('customer/delete_cart_item',customer.delete_cart_item,name='delete_cart_item'),
    path('customer/search',customer.search,name='search'),
    path('customer/delete_address',customer.delete_address,name='delete_address'),
    path('customer/<int:pk>/update_form',customer.CustomerEditView.as_view(),name='customer_update_form'),
    path('customer/address/<int:pk>/update_form',customer.CustomerAddressEditView.as_view(),name='customer_address_update_form'),
    path('customer/order/<int:pk>/items',customer.order_items,name='customer_order_items'),
    path('customer/category_foods',customer.category_foods,name='category_foods'),
    path('customer/ordered_orders',customer.customer_ordered_orders,name='customer_ordered_orders'),
    path('customer/sent_orders',customer.customer_sent_orders,name='customer_sent_orders'),
    path('customer/delivered_orders',customer.customer_delivered_orders,name='customer_delivered_orders'),

    
    
    # path('customer/address/update_form2',customer.CustomerAddressEditView2.as_view(),name='customer_address_update_form2'),


    
    # path('restaurant/all/',restaurant.RestaurantList.as_view(),name='restaurants_list0'),
    path('restaurant/<int:pk>/branches/',restaurant.restaurant_branches,name='restaurant_branchs'),
    path('restaurant/<int:pk>/branches/<int:id>/edit',restaurant.BranchUpdateView.as_view(),name='restaurant_branch_edit'),
    # path('restaurant/<int:pk>/',menu_item.get_branch_menu,name='restaurant_menu'),
    # path('restaurant/<int:pk>/delete',restaurant.RestaurantDeleteView.as_view(),name='delete_restaurant0'),
    # path('restaurant/<int:pk>/edit',restaurant.RestaurantUpdateView.as_view(),name='restaurant_edit0'),

    path('branche/<int:pk>/edit',branch.BranchUpdateView.as_view(),name='branch_edit'),
    path('branche/menu',branch.branch_menu_item,name='branch_menu'),
    path('branche/order',branch.branch_orders,name='branch_orders'),
    path('branche/order/<int:pk>/order_items',order_items,name='order_items'),
    path('branche/order/ordered', branch.branch_ordered_orders, name='ordered_orders'),
    path('branche/order/all', branch.all_orders, name='branch_all_orders'),
    path('branche/order/sent', branch.branch_sent_orders, name='sent_orders'),
    path('branche/order/delivered', branch.branch_delivered_orders, name='delivered_orders'),
    path('branche/order/date_sort', branch.branch_orders_date_sort, name='orders_date_sort'),

    
    path('test/',restaurant.test_popular_in_total2,name='popular_foods'),
    path('test2/<int:pk>',restaurant.test_popular_each_restaurant,name='branch_popular_foods'),
    path('test3/',restaurant.test_popular_restaurants,name='popular_restarunts'),

    path('order/<int:pk>/edit/manager',ManagerOrderUpdatView.as_view(),name='manager_order_edit'),
    path('order/<int:pk>/customer_info',order_customer_info,name='order_customer_info'),


    path('store', store , name='store'),
    path('', Index.as_view(), name='homepage'),
    path('signup', Signup.as_view(), name='signup'),
    path('signup/manager', ManagerSignup.as_view(), name='signup_manager'),
    path('signup/managerr/new_branch', ManagerSignupNewBranch.as_view(), name='signup_manager_new_branch'),
    path('signup/admin', SiteAdminSignupView.as_view(), name='admin_signupp'),
    path('login', Login.as_view(), name='login'),
    path('logout', logout , name='logout'),
    path('cart/', Cart.as_view() , name='cart'),
    path('check-out', CheckOut.as_view() , name='checkout'),

    path('orders', auth_middleware(OrderView.as_view()), name='orders'),

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


