from category.models import Category,Brand
from wallet_coupon.models import Coupon,WishList
from django.db.models import Count
from cart.models import CartItem
from django.contrib.auth import authenticate

def menu_links(request):

    links=Category.objects.all()
    brands=Brand.objects.all()
    wishlist_count=0
    cart_count=0
    if request.user.is_authenticated:
       
        user_wishlist = WishList.objects.filter(user=request.user)
        wishlist_count = user_wishlist.aggregate(total_count=Count('product'))['total_count']
        user_cart_items = CartItem.objects.filter(user=request.user)
        cart_count = user_cart_items.aggregate(total_count=Count('product'))['total_count']



    return {
        'links': links,
        'brands': brands,
        'wishlist_count': wishlist_count ,
        'cart_count':cart_count,

    }



