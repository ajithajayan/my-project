from django.contrib import admin
from .models import Wallet,Coupon,Coupon_Redeemed_Details,WishList

# Register your models here.

admin.site.register(Wallet)
admin.site.register(Coupon)
admin.site.register(Coupon_Redeemed_Details)
admin.site.register(WishList)
