from django.shortcuts import render,redirect
from .models import *
from account.models import *
from user.models import *
from django.contrib.auth.decorators import login_required 
from django.shortcuts import render,redirect,HttpResponse,get_object_or_404
from django.db.models import Q
from django.contrib.auth import authenticate,login,logout
from django.views.decorators.cache import cache_control
from django.http import HttpResponseBadRequest


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
    