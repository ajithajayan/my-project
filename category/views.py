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
    brands = Brand.objects.filter(brand_name=brand_name)
    if request.method == 'POST':
        brands.delete()
        return redirect('category:brand-list')
    return redirect('category:brand-list')
