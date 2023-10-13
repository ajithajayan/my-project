from django.urls import path,include
from . import views

app_name = 'wallet'

urlpatterns = [

    path('apply_coupon/', views.apply_coupon, name='apply_coupon'),
    path('payment/<order_id>/', views.payment, name='payment'),

    path('wishlist/<product_id>/',views.addto_wishlist,name='add-wishlist'),
    path('display/wishlist',views.display_wishlist,name='wishlist_page'),
    path('wallet_coupon/remove/wishlist/<int:product_id>/', views.remove_wishlist, name='remove-wishlist'),

    
    path('wallet/', views.wallet, name='wallet'),
    path('pay_from_wallet/<int:order_id>/', views.pay_from_wallet, name='pay-from-wallet'),
    path('return_order/<int:order_id>/', views.return_order, name='return_order'),
]
 