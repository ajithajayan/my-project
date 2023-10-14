from django.shortcuts import render,redirect
from .models import *
from account.models import *
from user.models import *
from wallet_coupon.models import *
from django.contrib.auth.decorators import login_required 
from django.shortcuts import render,redirect,HttpResponse,get_object_or_404
from django.db.models import Q
from django.contrib.auth import authenticate,login,logout
from django.views.decorators.cache import cache_control
from django.http import HttpResponseBadRequest
from django.contrib import messages

# Create your views here.


@login_required(login_url='account:admin-login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def brand_list(request):
    search_query = request.GET.get('search')
    
    if search_query:
        brands = Brand.objects.filter(Q(brand_name__icontains=search_query))
    else:
        brands = Brand.objects.all()

    return render(request, 'admin_side/brand.html', {'brands': brands})


@login_required(login_url='account:admin_login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def add_brand(request):
    if request.method=='POST':
        brand_name=request.POST['brand_name']
        brands=Brand(brand_name=brand_name)
        brands.save()   
        return redirect('category:brand-list')    
    return render(request, 'admin_side/add_brand.html')

@login_required(login_url='account:admin-login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def edit_brand(request,brand_name):
    brands = get_object_or_404(Brand, brand_name=brand_name)
    if request.method=='POST':
        brand_name = request.POST.get('brand_name')
        brands.brand_name = brand_name
        brands.save()
        return redirect('category:brand-list')

    else:

        context = {
            'brands':brands
        }

    return render(request, 'admin_side/edit_brand.html', context)    


@login_required(login_url='admin_login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def delete_brand(request, brand_name):
    brands = get_object_or_404(Brand, brand_name=brand_name)
    if request.method == 'POST':
        brands.delete()
        return redirect('category:brand-list')
    return redirect('category:brand-list')



# ---------------------------- category----------------------------


@login_required(login_url='account:admin_login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def category_list(request):
    search_query = request.GET.get('search')

    if search_query:
        categories = Category.objects.filter(Q(category_name__icontains=search_query))
    else:
        categories = Category.objects.all()

    context={
        'categories':categories
    } 

    return render(request,'admin_side/category.html',context)     


@login_required(login_url='account:admin_login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def add_category(request):
    
    if request.method == 'POST':
        category_name = request.POST.get('category_name')

        category = Category(category_name=category_name)
        category.save()
        
        return redirect('category:category-list')
    
    return render(request, 'admin_side/add_category.html')


@login_required(login_url='account:admin_login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def edit_category(request,category_name):
    category=get_object_or_404(Category, category_name=category_name)
    if request.method=='POST':
        category_name=request.POST['category_name']
        category.category_name = category_name
        category.save()

        return redirect('category:category-list')
    else:
        context = {
            'category':category
        }
    
    return render(request, 'admin_side/edit_category.html', context)


@login_required(login_url='account:admin_login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def delete_category(request, category_name):
    category = get_object_or_404(Category, category_name=category_name)
    if request.method == 'POST':
        category.delete()
        return redirect('category:category-list')
    # return render(request, 'admin_side/category_list.html', {'category': category})
    return redirect('category:category-list')




#------------------------------------------------------user listing-----------------------------------------------------------------


@login_required(login_url='account:admin-login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def user_list(request):
    
    search_query = request.GET.get('search', '')

    # Query the users based on the search query
    if search_query:
        users = Account.objects.filter(name__icontains=search_query)
    else:
        users = Account.objects.all()

    context = {
        'users': users
    }

    return render(request, 'admin_side/user_list.html', context)


@login_required(login_url='account:admin-login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def block_unblock_user(request, user_id):
    user = get_object_or_404(Account, id=user_id)

    # Toggle the is_blocked status of the user
    if user.is_active:
        user.is_active=False
        if request.user == user:
            logout(request)

    else:
        user.is_active=True
        
    user.save()
        

    return redirect('category:user_list')



#-------------------------------------------------------order-listing----------------------------------------------------------------------------

@login_required(login_url='account:admin-login')
def order_list(request):
    orders = Order.objects.all().order_by('-created_at')  # Fetch all orders from the Order model
    context = {'orders': orders}
    return render(request, 'admin_side/order_list.html', context)



@login_required(login_url='account:admin-login')
def ordered_product_details(request, order_id):
    order = Order.objects.get(id=order_id)
    ordered_products = OrderProduct.objects.filter(order=order)
    for i in ordered_products:
        total=+i.product_price

    context = {
        'order': order,
        'ordered_products': ordered_products,
    }
    return render(request, 'admin_side/ordered_product_details.html', context)



@login_required(login_url='account:admin-login')
def update_order_status(request, order_id):
    if request.method == 'POST':
        order = get_object_or_404(Order, id=int(order_id))
        status = request.POST['status']
        order.status = status
        order.save()
        return redirect('category:order_list')
    else:
        return HttpResponseBadRequest("Bad request.")
    


# -----------------------------------------------------------coupon---------------------------------------------------------



@login_required(login_url='account:admin-login')
def coupon_list(request):
    coupons = Coupon.objects.all()
    context = {
        'coupons': coupons
    }
    return render(request, 'admin_side/coupon_list.html', context)



@login_required(login_url='account:admin-login')
def add_coupon(request):
    if request.method == 'POST':
        coupon_code = request.POST.get('coupon_code')
        discount_amount = request.POST.get('discount_amount')
        minimum_amount = request.POST.get('minimum_amount')
        valid_from = request.POST.get('valid_from')
        valid_to = request.POST.get('valid_to')

        coupon = Coupon(
            coupon_code=coupon_code,
            discount_amount=discount_amount,
            minimum_amount=minimum_amount,
            valid_from=valid_from,
            valid_to=valid_to
        )
        coupon.save()

        return redirect('category:coupon_list')

    return render(request, 'admin_side/add_coupon.html')


@login_required(login_url='account:admin-login')
def edit_coupon(request, coupon_id):
    try:
        # Get the coupon instance by its ID
        coupon = Coupon.objects.get(pk=coupon_id)

        # Check if the request method is POST (form submission)
        if request.method == 'POST':
            # Retrieve the data from the POST request
            coupon_code = request.POST.get('coupon_code')
            discount_amount = request.POST.get('discount_amount')
            minimum_amount = request.POST.get('minimum_amount')
            valid_from = request.POST.get('valid_from')
            valid_to = request.POST.get('valid_to')

            # Update the coupon instance with the new data
            coupon.coupon_code = coupon_code
            coupon.discount_amount = discount_amount
            coupon.minimum_amount = minimum_amount
            coupon.valid_from = valid_from
            coupon.valid_to = valid_to

            # Save the updated coupon instance
            coupon.save()

            return redirect('category:coupon_list')  # Redirect to the coupon list view after editing

        return render(request, 'admin_side/edit_coupon.html', {'coupon': coupon})
    
    except Coupon.DoesNotExist:
        return HttpResponseBadRequest("Coupon does not exist")
    


@login_required(login_url='account:admin-login')
def delete_coupon(request, coupon_id):
    coupon = get_object_or_404(Coupon, id=coupon_id)

    if request.method == 'POST':
        coupon.delete()
        return redirect('category:coupon_list')

    return redirect('category:coupon_list')





# ----------------------------------------------------------- offer--------------------------------------------------------------------


@login_required(login_url='account:admin-login')
def category_offer(request):
    if request.method == 'POST':

        category_id = request.POST.get('category')
        discount = float(request.POST.get('discount'))
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

        category = Category.objects.get(id=category_id)
        if Offer.objects.filter(category=category).exists():
            messages.warning(request, "There is Already One Discount offer on this product")
            return redirect('category:category_offer')
        # if len(str(discount)) <= 2 or discount == 100:
        print(category_id, discount, start_date, end_date)
        discount = int(discount) / 100
        category = Category.objects.get(id=category_id)
        dis = Offer(discount=(discount * 100), category=category, start_date=start_date, end_date=end_date)
        dis.save()
        product_list = Product.objects.filter(category=category)
        for product in product_list:
            product.discount = discount*100
            product.rprice = product.price
            product.price = product.rprice - round(product.rprice*discount,2)
            product.save()
            
            
        messages.success(request, f'{discount*100}% Discount Added for all Products under {category.category_name}')
        return redirect('category:category_offer')



        # offer = Offer.objects.create(category=category, discount_percentage=discount_percentage, start_date=start_date, end_date=end_date)
        # offer.save()

        # Redirect to the same page to show the updated offers
        return redirect('adminpanel:category_offer')

    categories = Category.objects.all()
    added_offers = Offer.objects.all()

    context = {'categories': categories, 'added_offers': added_offers,}
    return render(request, 'admin_side/category_offer.html', context)



@login_required(login_url='account:admin-login')
def admin_discount_add(request):
    if request.method == 'POST':
        discount = request.POST.get('discount')
        category_id = request.POST.get('category')
        category = Category.objects.get(uid=category_id)
        if Offer.objects.filter(category=category).exists():
            messages.warning(request, "There is Already One Discount offer on this product")
            return redirect('admin_manage_offers')
        if len(str(discount)) <=2 or discount == 100:
            discount = int(discount) / 100
            category = Category.objects.get(uid=category_id)
            dis = Offer(discount=(discount * 100), category=category)
            dis.save()
            product_list = Product.objects.filter(category=category)
            for product in product_list:
                product.discount = discount*100
                product.price = product.rprice - round(product.rprice*discount,2)
                product.save()
                variant_list = ProductVariant.objects.filter(product_id=product)
                for var in variant_list:
                    var.price = round(var.rprice*discount,2)
                    var.save()

            messages.success(request, f'{discount*100}% Discount Added for all Products under {category.category_name}')
        return redirect('admin_manage_offers')




@login_required(login_url='account:admin-login')
def edit_offer(request, offer_id):
    offer = get_object_or_404(Offer, id=offer_id)

    if request.method == 'POST':
        # Process the form data to update the offer
        offer.discount_percentage = float(request.POST.get('discount_percentage'))
        offer.start_date = request.POST.get('start_date')
        offer.end_date = request.POST.get('end_date')
        offer.save()
        return redirect('category:category_offer')
    
    categories = Category.objects.all()

    context = {
        'offer': offer,
        'categories':categories,
               }
    return render(request, 'admin_side/edit_offer.html', context)



@login_required(login_url='account:admin-login')
def delete_offer(request, offer_id):
    offer = get_object_or_404(Offer, id=offer_id)

    if request.method == 'POST':
        product_list = Product.objects.filter(category=offer.category)
        for product in product_list:
            product.discount = 0
            product.price = product.rprice
            product.save()
        offer.delete()
        return redirect('category:category_offer') 

    return redirect('category:category_offer')