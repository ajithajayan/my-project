from django.urls import path,include
from . import views

app_name = 'user'

urlpatterns = [
    path('',views.index,name='index'),
    path('home/<slug:category_slug>/',views.index,name='filter_product'),
    path('product-detail/<int:product_id>/', views.product_detail, name='product-detail'),

    path('store',views.store,name='store'),
    path('store/<slug:category_slug>/',views.store,name='product_by_category'),

    

    path('user_profile/', views.user_profile, name='user_profile'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('address/', views.address_page, name='address_page'),
    path('add_address/', views.add_address, name='add_address'),
    path('edit_address/<int:address_id>/', views.edit_address, name='edit_address'),
    path('delete_address/<int:address_id>/', views.delete_address, name='delete_address'),
    path('set_default_address/<int:address_id>/', views.set_default_address, name='set_default_address'),
    path('order_history/', views.order_history, name='order_history'),
     path('change_password/', views.change_password, name='change_password'),
    path('verify-otp/change_password',views.verify_otp_change_password,name='verify-otp-change-password'),
    path('sent-otp/change_password',views.sent_otp_change_password,name='sent-otp-change-password'),


    path('checkout/', views.checkout, name='checkout'),
    path('place_order/', views.place_order, name='place_order'),
    path('payments/', views.payments, name='payments'),
    path('order_confirmed/', views.order_confirmed, name='order_confirmed'),
    path('download_invoice/<int:order_id>/', views.download_invoice, name='download_invoice'),
    path('ordered_product_details/<int:order_id>', views.ordered_product_details, name='ordered_product_details'),

    path('pay_with_cash_on_delivery/<int:order_id>/', views.pay_with_cash_on_delivery, name='pay_with_cash_on_delivery'),
    
    
]
