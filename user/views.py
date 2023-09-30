from django.shortcuts import render,redirect,get_object_or_404
from account.forms import CustomerForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from category.models import *
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
# Create your views here.

def index(request):
    products=Product.objects.all()
    
    context={'products':products}

    return render(request,'user_side/index.html',context)



# @login_required(login_url='account:user_login')
def product_detail(request, product_id):
    products = get_object_or_404(Product, pk=product_id)
    product_variants = ProductVariant.objects.filter(product=products) 
    context = {
        'products': products,
        'productvarient':product_variants
    }
    return render(request, 'user_side/product-detail.html', context)
