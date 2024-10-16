from django.urls import path
from . import views

urlpatterns = [
     path('api/menu/<str:menuID>/', views.get_menu_price, name='get_menu_price'),
    #main section
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout, name='logout'),

    #user section
    path('menu/', views.usermenu, name='usermenu'),
    path('menu/user-order/<int:cafe_id>/', views.userorder, name='userorder'),
    path('menu/tracking-order/', views.trackingorder, name='trackingorder'),
    path('menu/user-profile/', views.userprofile, name='userprofile'),
    path('menu/user-cart/', views.usercart, name='usercart'),
    path('menu/receipt/', views.receipt, name='receipt'),

    #staff section
    path('staff-menu/', views.staffmenu, name='staffmenu'),
    path('staff-menu/menu-detail/', views.menudetail, name='menudetail'),
    path('staff-menu/order-detail/', views.orderdetail, name='orderdetail'),
    

    #admin section
    path('admin-menu/', views.adminmenu, name='adminmenu'),
    path('admin-menu/cafe-staff/', views.cafestaff, name='cafestaff'),
    path('admin-menu/cafe-staff/cafe-detail/', views.cafedetail, name='cafedetail'),
    path('admin-menu/cafe-staff/staff-detail/', views.staffdetail, name='staffdetail'),
    path('admin-menu/user-setting/', views.usersetting, name='usersetting'),
    
]