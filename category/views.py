from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth.decorators import login_required 
from django.shortcuts import render,redirect,HttpResponse,get_object_or_404
from django.db.models import Q

# Create your views here.



def brand_list(request):
    search_query = request.GET.get('search')
    
    if search_query:
        brands = Brand.objects.filter(Q(brand_name__icontains=search_query))
    else:
        brands = Brand.objects.all()

    return render(request, 'admin_side/brand.html', {'brands': brands})


@login_required(login_url='account:admin_login')
def add_brand(request):
    if request.method=='POST':
        brand_name=request.POST['brand_name']
        brands=Brand(brand_name=brand_name)
        brands.save()   
        return redirect('category:brand-list')    
    return render(request, 'admin_side/add_brand.html')


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
def delete_brand(request, brand_name):
    brands = get_object_or_404(Brand, brand_name=brand_name)
    if request.method == 'POST':
        brands.delete()
        return redirect('category:brand-list')
    return redirect('category:brand-list')



# ---------------------------- category----------------------------


@login_required(login_url='account:admin_login')
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
def add_category(request):
    
    if request.method == 'POST':
        category_name = request.POST.get('category_name')

        category = Category(category_name=category_name)
        category.save()
        
        return redirect('category:category-list')
    
    return render(request, 'admin_side/add_category.html')


@login_required(login_url='account:admin_login')
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
def delete_category(request, category_name):
    category = get_object_or_404(Category, category_name=category_name)
    if request.method == 'POST':
        category.delete()
        return redirect('category:category-list')
    # return render(request, 'admin_side/category_list.html', {'category': category})
    return redirect('category:category-list')

