from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from wallet_coupon.models import *
from user.models import *
from category.views import *
from cart.models import *
from django.utils import timezone
from django.contrib import messages

# Create your views here.


@login_required(login_url='login')
def apply_coupon(request):

    if request.method == 'POST':
        coupon_code = request.POST.get('coupon_code')
        order_id = request.POST.get('order_id')
        print(coupon_code,order_id)
        request.session['coupon_code'] = coupon_code

        try:
            coupon = Coupon.objects.get(coupon_code=coupon_code)
            order = Order.objects.get(id=order_id)

            if coupon.valid_from <= timezone.now().date() <= coupon.valid_to:
                if order.order_total >= coupon.minimum_amount:
                    # Check if the coupon is already redeemed by the user
                    if coupon.is_redeemed_by_user(request.user):
                        messages.error(request, 'Coupon has already been redeemed by you.')
                    else:
                        # Apply the coupon and calculate updated total
                        updated_total = order.order_total - float(coupon.discount_amount)
                        order.order_total = updated_total
                        order.save()

                        # Mark the coupon as redeemed for the user
                        redeemed_details = Coupon_Redeemed_Details(user=request.user, coupon=coupon, is_redeemed=True)
                        redeemed_details.save()
                        messages.error(request, 'Coupon applied.')
                        # Redirect to payment page with updated order total
                        return redirect('wallet:payment', order_id)

                else:
                    messages.error(request, 'Coupon is not applicable for the order total.')
            else:
                messages.error(request, 'Coupon is not applicable for the current date.')

        except Coupon.DoesNotExist:
            messages.error(request, 'Invalid coupon code.')

    

    # Redirect back to the payment page if coupon application fails
    return redirect('wallet:payment', order_id)





@login_required(login_url='login')
def payment(request, order_id):
    
    # try:
    order = Order.objects.get(id=order_id)
    # Check if the coupon is valid for the cart total
        # Redirect back to the cart with the updated total and applied coupon
    current_user = request.user
    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('user:index')
        

    grand_total = 0
    tax = 0
    total = 0
    quantity = 0
    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity
    tax = (2 * total)/100
    grand_total = total + tax

    try:

        applied_coupon = request.session['coupon_code']

        if applied_coupon:
            coupon = Coupon.objects.get(coupon_code=applied_coupon)
            print('*********coupon***********',coupon)
            coupon_discount = coupon.discount_amount
            print('**********coupon_discount**********', coupon_discount)

        context = {
        'order': order,
        'cart_items': cart_items,
        'total': total,
        'tax': tax,
        'grand_total': order.order_total,
        'coupon_discount':coupon_discount
    }    
    except :
        context = {
        'order': order,
        'cart_items': cart_items,
        'total': total,
        'tax': tax,
        'grand_total': order.order_total,
    }
    # print('********applied_coupon*********', applied_coupon)
    



    


    return render(request, 'user_side/payment.html', context)



# ---------------------------------------------------------wishlist------------------------------------------------------



def addto_wishlist(request,product_id):
    product=Product.objects.get(product_id=product_id)
    if WishList.objects.filter(user=request.user, product=product).exists():
        messages.success(request, 'Item is already in your wishlist.')
    else:
        # If it's not in the wishlist, create a new WishlistItem
        WishList.objects.create(user=request.user, product=product)
        messages.success(request, 'Item added to your wishlist.')

    return redirect(request.META.get('HTTP_REFERER', 'wallet:wishlist_page'))


def display_wishlist(request):
    wishlist_items=WishList.objects.all()
    user_wishlist_products = [item.product for item in wishlist_items]
    context = {
        'wishlist_items': wishlist_items,
        'user_wishlist_products': user_wishlist_products,
    }

    return render(request, 'user_side/wishlist_page.html', context)


def remove_wishlist(request,product_id):
    product = get_object_or_404(Product, product_id=product_id)
    
    # Check if the item is in the user's wishlist
    try:
        wishlist_item = WishList.objects.get(user=request.user, product=product)
        wishlist_item.delete()  # Remove the item from the wishlist
        messages.success(request, 'Item removed from your wishlist.')
    except WishList.DoesNotExist:
        messages.error(request, 'Item is not in your wishlist.')
    
    return redirect(request.META.get('HTTP_REFERER', 'wallet:wishlist_page'))





#----------------------------------------------------------------Wallet------------------------------------------------------

# @login_required(login_url='login')
def wallet(request):
    cur_user = request.user
    try:
        wallet = Wallet.objects.get(user=cur_user)
    except Wallet.DoesNotExist:
        wallet = Wallet.objects.create(user=cur_user, amount=0)
    wallet_amount = wallet.amount

    # Retrieve the referral ID from the user's profile
    user = Account.objects.get(email=cur_user)
    referral_id = user.referral_id
    

    context = {'wallet_amount': wallet_amount, 'referral_id': referral_id}
    return render(request, 'user_side/wallet.html', context)




@login_required(login_url='login')
def pay_from_wallet(request, order_id):
    cur_user = request.user
    order = Order.objects.get(id=order_id)
    try:
        wallet = Wallet.objects.get(user=cur_user)
        
    except:
        wallet = Wallet.objects.create(user=cur_user, amount=0)
        wallet.save()
        
    if wallet.amount>order.order_total:
        payment_id = f'uw{order.order_number}{order_id}'
        payment = Payment.objects.create(user=cur_user, 
                                         payment_method='Wallet',payment_id=payment_id,
                                         amount_paid=order.order_total, status='COMPLETED')

        payment.save()
        order.is_ordered = True
        
        order.payment = payment
        order.save()
        wallet.amount -= order.order_total
        wallet.save()

        cart_items = CartItem.objects.filter(user=request.user)

        for item in cart_items:
            orderproduct = OrderProduct()
            orderproduct.order_id = order.id
            orderproduct.payment = payment
            orderproduct.user_id = request.user.id
            orderproduct.product_id = item.product_id
            orderproduct.quantity = item.quantity
            orderproduct.product_price = item.product.price
            orderproduct.ordered = True
            orderproduct.size = item.variations.size
            orderproduct.color = item.variations.color
            orderproduct.save()




        
        cart_items.delete()
        
    else:
        messages.warning(request, 'Not Enough Balance in Wallet')
        return redirect('wallet:payment', order_id)
    context = {
        'order': order,
        'order_number': order.order_number,
        'transID': payment.payment_id,
        }
    return render(request, 'user_side/order_confirmed.html', context)



@login_required(login_url='login')
def return_order(request, order_id):
    order = Order.objects.get(id=order_id)
    order_method=order.payment.payment_method
    if  order_method!='Cash on Delivery'and order.status == 'Delivered':
        user_profile = request.user
        wallet, created = Wallet.objects.get_or_create(user=user_profile)

        # Credit the purchased amount back to the wallet
        wallet.amount += order.order_total
        wallet.amount = round(wallet.amount, 2)
        wallet.save()
       
        # Update the order status to 'Returned'
        order.status = 'Returned'
        order.save()
        for order_product in order.orderproduct_set.all():
            if order_product.variations.exists():
                for variation in order_product.variations.all():
                    variation.stock += order_product.quantity
                    variation.save()
        messages.warning(request, 'return request has been send. amount sucessfully returned to your wallet')

    elif order_method=='Cash on Delivery' and order.status == 'Delivered':
        order.status = 'Returned'
        order.save()
        messages.warning(request, 'return request has been send.')

    elif order_method=='Cash on Delivery' and order.status != 'Delivered' :
        order.status = 'Cancelled'
        order.save()
        messages.warning(request, 'return request has been send.')
    else:
        user_profile = request.user
        wallet, created = Wallet.objects.get_or_create(user=user_profile)

        # Credit the purchased amount back to the wallet
        wallet.amount += order.order_total
        wallet.amount = round(wallet.amount, 2)
        wallet.save()

        order.status = 'Cancelled'
        order.save()
        for order_product in order.orderproduct_set.all():
            if order_product.variations.exists():
                for variation in order_product.variations.all():
                    variation.stock += order_product.quantity
                    variation.save()
        messages.warning(request, 'cancel request has been send. amount sucessfully returned to your wallet')

    
    
        
    return redirect('user:order_history') 


