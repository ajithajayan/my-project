from django.shortcuts import render,redirect,get_object_or_404
from account.forms import CustomerForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.shortcuts import render,redirect,HttpResponseRedirect,get_object_or_404
from category.models import *
from account.models import *
from user.models import *
from cart.models import *
from wallet_coupon.models import *
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
import datetime
from django.http import HttpResponse, JsonResponse
import json
import random
from django.db.models import Q
from django.core.mail import send_mail
# custom_filters.py

from django.template.defaultfilters import register

@register.filter
def lte(value, arg):
    return value <= arg
@register.filter
def gte(value, arg):
    return value >= arg


# Create your views here.

def store(request, category_slug):
    # Retrieve all categories that match the provided slug
    categories = Category.objects.filter(Q(slug=category_slug) | Q(parent__slug=category_slug))

    # Check if any matching categories were found
    if categories.exists():
        # Filter products based on the selected category (if provided) and whether they are active
        products = Product.objects.filter(category__in=categories, is_active=True)
    else:
        # Handle the case where no matching categories were found (e.g., show all products)
        products = Product.objects.filter(is_active=True)

    context = {
        'category_slug': category_slug,  # Pass the selected category slug to the template
        'products': products,
    }

    return render(request, 'user_side/category_view.html', context)









def index(request, category_slug=None, price_range=None,sort_by=None):
    categories = None
    search_query = request.GET.get('search_product')
    # sort_by = request.GET.get('sort_by')

    # Initialize products as the complete Product queryset
    products = Product.objects.filter(is_active=True)

    if category_slug:
        categories = Category.objects.filter(Q(slug=category_slug) | Q(parent__slug=category_slug))
        # Filter products based on selected categories
        products = products.filter(category__in=categories)

    if price_range:
        # Parse and extract the minimum and maximum prices from the parameter
        min_price, max_price = price_range.split('-')
        # Filter products based on price range
        products = products.filter(price__gte=min_price, price__lte=max_price)

    if search_query:
        # Filter products based on search query
        products = products.filter(Q(product_name__icontains=search_query) | Q(description__icontains=search_query))

    # Define a default sorting order if sort_by is not provided
    # if not sort_by:
    #     sort_by = 'low_to_high'  # You can change this to your desired default sorting

    if sort_by == 'low_to_high':
        products = products.order_by('price')
    elif sort_by == 'high_to_low':
        products = products.order_by('-price')

    context = {
        'products': products
    }
    return render(request, 'user_side/index.html', context)



# @login_required(login_url='account:user_login')
def product_detail(request, product_id):
    products = get_object_or_404(Product, pk=product_id)
    product_variants = ProductVariant.objects.filter(product=products) 
    context = {
        'products': products,
        'productvarient':product_variants
    }
    return render(request, 'user_side/product-detail.html', context)


#---------------------------------------------------checkout--------------------------------------------------------

# @login_required(login_url='account:user_login')
def checkout(request, total=0, quantity=0, cart_items=None):
    try:
        tax = 0
        grand_total = 0
        coupon_discount = 0

        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
            
        else:
            pass


        # variant = cart_items.variations
        # if variant.stock >= 1:
        #     variant.stock -= cart_items.quantity
        #     variant.save()
        # else:
        #     print("Not enough stock!")


        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity

            try:
                variant = cart_item.variations
                if variant.stock <= 0:
                    # variant.stock -= cart_item.quantity
                    # variant.save()
                    print("Not enough stock!")
            except ObjectDoesNotExist:
                pass

        tax = (2 * total) / 100

        # Check if a coupon is applied
        # applied_coupon = request.session.get('coupon_id')
        # if applied_coupon:
        #     coupon = Coupon.objects.get(id=applied_coupon)
        #     coupon_discount = coupon.discount_amount
        # applied_coupon = request.session['coupon_code']
        # # print('********applied_coupon*********', applied_coupon)
        # if applied_coupon:
        #     coupon = Coupon.objects.get(coupon_code=applied_coupon)
        #     print('*********coupon***********',coupon)
        #     coupon_discount = coupon.discount_amount
        #     print('**********coupon_discount**********', coupon_discount)

        grand_total = total + tax  # Apply coupon discount to grand_total

        
    except ObjectDoesNotExist:
        pass

    address_list = AdressBook.objects.filter(user=request.user)
    default_address = address_list.filter(is_default=True).first()
    coupons = Coupon.objects.all()
    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total,
        'address_list': address_list,
        'default_address': default_address,  # Pass the default address to the context
        'coupons': coupons,
        # 'applied_coupon': applied_coupon,
        'coupon_discount':coupon_discount
    }
    return render(request, 'user_side/checkout.html', context)

#---------------------------------------------------user profile--------------------------------------------------------

@login_required(login_url='account:user_login')
def user_profile(request):
    user_profile = Account.objects.get(email=request.user.email)

    context = {
        'user_profile': user_profile,
    }
    return render(request, 'user_side/user_profile.html', context)


@login_required(login_url='account:user_login')
def edit_profile(request):
    user_profile = Account.objects.get(email=request.user.email) # Get the UserProfile instance for the logged-in user

    if request.method == 'POST':
        # Handle the form submission and update the user details
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        # email = request.POST.get('email')
        mobile = request.POST.get('mobile')

        # Update the user profile fields with the form data
        user_profile.first_name = first_name
        user_profile.last_name = last_name
        user_profile.username = username
        # user_profile.email = email
        user_profile.phone_number = mobile

        # Save the changes to the UserProfile and User models
        user_profile.save()

        return redirect('user:user_profile')  # Redirect to the user profile page after successful update
    else:
        return render(request, 'user_side/edit_profile.html', {'user_profile': user_profile})
    


@login_required(login_url='account:user_login')
def address_page(request):
    user = request.user
    addresses = AdressBook.objects.filter(user=user)
    default_address = addresses.filter(is_default=True).first()

    context = {
        'addresses': addresses,
        'default_address': default_address
    }
    return render(request, 'user_side/address_page.html', context)



@login_required(login_url='account:user_login')
def add_address(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        address_line_1 = request.POST.get('address_line_1')
        address_line_2 = request.POST.get('address_line_2')
        country = request.POST.get('country')
        state = request.POST.get('state')
        city = request.POST.get('city')
        pincode = request.POST.get('pincode')



        #Create a new shipping address instance
        address = AdressBook(user=request.user, first_name=first_name, last_name=last_name, phone=phone, email=email, address_line_1=address_line_1, address_line_2=address_line_2, country=country, state=state, city=city, pincode=pincode)
        address.save()


        # Set is_default attribute of the newly added address and reset previous default
        if request.user.is_authenticated:
            AdressBook.objects.filter(user=request.user, is_default=True).update(is_default=False)
            address.is_default = True
            address.save()

        if 'source' in request.GET and request.GET['source'] == 'checkout':
            # If the source is 'checkout', redirect back to the checkout page
            return redirect('user:checkout')  # Replace 'checkout' with your actual checkout view name

        return redirect('user:address_page')
    else:
        return render(request, 'user_side/add_address.html')
    

@login_required(login_url='account:user_login')
def edit_address(request, address_id):
    address = get_object_or_404(AdressBook, pk=address_id)

    if request.method == 'POST':
        # Handle the form submission and update the address details
        address.first_name = request.POST.get('first_name')
        address.last_name = request.POST.get('last_name')
        address.phone = request.POST.get('phone')
        address.email = request.POST.get('email')
        address.address_line_1 = request.POST.get('address_line_1')
        address.address_line_2 = request.POST.get('address_line_2')
        address.city = request.POST.get('city')
        address.state = request.POST.get('state')
        address.country = request.POST.get('country')
        address.pincode = request.POST.get('pincode')
        address.save()

        return redirect('user:address_page')  # Redirect to the address page after successful update

    return render(request, 'user_side/edit_address.html', {'address': address})



@login_required(login_url='account:user_login')
def delete_address(request, address_id):
    
    try:
        address = AdressBook.objects.get(id=address_id)
        address.delete()
    except AdressBook.DoesNotExist:
        pass

    return redirect('user:address_page')


@login_required(login_url='account:user_login')
def set_default_address(request, address_id):
    addr_list = AdressBook.objects.filter(user=request.user)
    for a in addr_list:
        a.is_default = False
        a.save()
    address = AdressBook.objects.get(id=address_id)
    address.is_default=True
    address.save()
    return redirect('user:checkout')


# ----------------------------------------------------------change-password----------------------------------------------------------

def change_password(request):
    if request.method != "POST":
        request.session['email']=request.user.email
        return render(request, "user_side/change_password.html")
    else:
        pass1 = request.POST["re_password"]
        pass2 = request.POST["password"]
        if pass1 != pass2:
            messages.warning(request, "password not correct")
            return redirect("user_side/change_password.html")
        request.session['password']=pass1
        return redirect('user:sent-otp-change-password') 
    

def sent_otp_change_password(request):
   random_num=random.randint(1000,9999)
   request.session['OTP_Key']=random_num
   send_mail(
   "OTP AUTHENTICATING fKart",
   f"{random_num} -OTP",
   "ajithajayan222aa@gmail.com",
   [request.session['email']],
   fail_silently=False,
    )
   return redirect('user:verify-otp-change-password')


def verify_otp_change_password(request):
   user=Account.objects.get(email=request.session['email'])
   if request.method=="POST":
      if str(request.session['OTP_Key']) != str(request.POST['otp']):
         print(request.session['OTP_Key'],request.POST['otp'])
         messages.success(request, "OTP verification failed")
         return redirect('user:user_profile') 
        #  user.is_active=True
      else:
         password=request.session['password']
         user.set_password(password)
         user.save()
         messages.success(request, "password changed successfully!")
         login(request,user)
         return redirect('user:user_profile')
   return render(request,'user_side/verify_otp.html')


#---------------------------------------------------place order--------------------------------------------------------

@login_required(login_url='account:user_login')
def place_order(request, total=0, quantity=0):
    current_user = request.user
    # coupons = Coupon.objects.all()

    #If the cart count is less than 0, then redirect back to home
    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('user:index')
    

    grand_total = 0
    tax = 0
    coupon_discount = 0
    
    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity
    tax = (2 * total)/100

   

    grand_total = total + tax 
    

    if request.method == 'POST':
        
        try:
            address = AdressBook.objects.get(user=request.user,is_default=True)
        except:
            messages.warning(request, 'No delivery address exixts! Add a address and try again')
            return redirect('checkout')
        
        
        data = Order()
        data.user = current_user
        data.first_name = address.first_name
        data.last_name = address.last_name
        data.phone = address.phone
        data.email = address.email
        data.address_line_1 = address.address_line_1
        data.address_line_2 = address.address_line_2
        data.city = address.city
        data.state = address.state
        data.country = address.country
        data.pincode = address.pincode
        data.order_total = grand_total
        data.tax = tax
        data.ip = request.META.get('REMOTE_ADDR')
        data.save()

        #Generate order number
        yr = int(datetime.date.today().strftime('%Y'))
        dt = int(datetime.date.today().strftime('%d'))
        mt = int(datetime.date.today().strftime('%m'))
        d = datetime.date(yr,mt,dt)
        current_date = d.strftime("%Y%m%d")
        order_number = current_date + str(data.id)
        data.order_number = order_number
        data.save()

    

        coupons=Coupon.objects.all()

        order = Order.objects.get(user=current_user, is_ordered=False, order_number=order_number)
        context = {
            'order': order,
            'cart_items': cart_items,
            'total': total,
            'tax': tax,
            'grand_total': grand_total,
            'coupons': coupons,
            'coupon_discount':coupon_discount
            
        }




        return render(request, 'user_side/payment.html', context)
    else:
        return redirect('user:checkout')
    





@login_required(login_url='account:user_login')
def order_confirmed(request):
    order_number = request.GET.get('order_number')
    transID = request.GET.get('payment_id')
   

    try:
        order = Order.objects.get(order_number=order_number, is_ordered=True)
        ordered_products = OrderProduct.objects.filter(order_id=order.id)
        print(order,ordered_products)
        subtotal = 0
        for i in ordered_products:
            subtotal += i.product_price * i.quantity
        print(subtotal)
        payment = Payment.objects.get(payment_id=transID)

        applied_coupon = request.session.get('coupon_code')
    
        if applied_coupon:
            coupon = Coupon.objects.get(coupon_code=applied_coupon)
            print('******coupon*******', coupon)

            coupon_discount = coupon.discount_amount
            print('*****coupon_discount*****', coupon_discount, coupon.discount_amount)
        else:
            coupon_discount = 0


        context = {
            'order': order,
            'ordered_products': ordered_products,
            'order_number': order.order_number,
            'transID': payment.payment_id,
            'subtotal': subtotal,
            'payment': payment,
            'coupon_discount':coupon_discount,
        }
        return render(request, 'user_side/order_confirmed.html', context)
    
    except (Payment.DoesNotExist, Order.DoesNotExist):
        return redirect('user:index')





@login_required(login_url='account:user_login')
def pay_with_cash_on_delivery(request, order_id):
    cur_user = request.user
    order = Order.objects.get(id=order_id)
    print('***************order*************',order)
    

    applied_coupon = request.session.get('coupon_code')
    coupon_discount=0


    if applied_coupon:
        coupon = Coupon.objects.get(coupon_code=applied_coupon)
        print('******coupon*******', coupon)
        
        coupon_discount = coupon.discount_amount
        print('*****coupon_discount*****', coupon_discount, coupon.discount_amount)

    payment_id = f'uw{order.order_number}{order_id}'
    payment = Payment.objects.create(user=cur_user, 
                                        payment_method='Cash on Delivery',payment_id=payment_id,
                                        amount_paid=order.order_total, status='COMPLETED',discount=coupon_discount )
    
    payment.save()
    order.is_ordered = True
    order.payment = payment
    order.save()


    cart_items = CartItem.objects.filter(user=request.user)

    for item in cart_items:
            orderproduct = OrderProduct()
            item.variations.stock-=item.quantity
            item.variations.save()
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


    # Clear the cart (adjust this based on your project structure)
    cart_items.delete()

    tax = 0
    total = 0
    quantity = 0
    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity
    tax = (2 * total)/100
    grand_total = total + tax
    print('******grand total*****', grand_total)

    ordered_products = OrderProduct.objects.filter(order_id=order_id)
    subtotal = 0
    for i in ordered_products:
            subtotal += i.product_price * i.quantity

    print('*****subtotal*****',subtotal)         

    context = {
        'order': order,
        'ordered_products': ordered_products,
        'order_number': order.order_number,
        'transID': payment.payment_id,
        'cart_items': cart_items,
        'total': total,
        'tax': tax,
        'grand_total': grand_total,
        'subtotal': subtotal,
        'coupon_discount':coupon_discount,
        'payment': payment,
        }

    # Redirect to the order confirmed page
    return render(request, 'user_side/order_confirmed.html', context)




#-------------------------------------------------------#order------------------------------------------------------------------


@login_required(login_url='account:user_login')
def order_history(request):
    orders = Order.objects.filter(user=request.user, is_ordered=True).order_by('-created_at')
    context = {
        'orders': orders,
    }
    return render(request, 'user_side/order_history.html', context)



@login_required(login_url='account:user_login')
def ordered_product_details(request, order_id):
    order = Order.objects.get(id=order_id)
    ordered_products = OrderProduct.objects.filter(order=order)
    context = {
        'order': order,
        'ordered_products': ordered_products,
    }
    return render(request, 'user_side/ordered_product_details.html', context)


@login_required(login_url='account:user_login')
def download_invoice(request, order_id):
    order_number = request.GET.get('order_number')
    transID = request.GET.get('payment_id')
   

    try:
        order = Order.objects.get(id=order_id, is_ordered=True)
        ordered_products = OrderProduct.objects.filter(order_id=order.id)

        subtotal = 0
        for i in ordered_products:
            subtotal += i.product_price * i.quantity

        payment = Payment.objects.get(id=order.payment.id)

       


        context = {
            'order': order,
            'ordered_products': ordered_products,
            'order_number': order.order_number,
            'transID': payment.payment_id,
            'subtotal': subtotal,

        }
        return render(request, 'user_side/order_confirmed.html', context)
    
    except (Payment.DoesNotExist, Order.DoesNotExist):
        return redirect('user:index')




def get_names(request):
    search = request.GET.get('search')
    
    # Check if 'search' is not None or empty
    if search:
        objs = Product.objects.filter(product_name__istartswith=search)
        payload = [{'name': obj.product_name} for obj in objs]
    else:
        payload = []

    return JsonResponse({
        'status': True,
        'payload': payload
    })

