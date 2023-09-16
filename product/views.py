from django.shortcuts import render,redirect,HttpResponse
from category.models import *
from django.contrib.auth.decorators import login_required
from .forms import *

# Create your views here.



@login_required(login_url='account:admin_login')
def product_list(request):
    search_query = request.GET.get('search', '')

    # Query the products based on the search query
    if search_query:
        products = Product.objects.filter(product_name__icontains=search_query)
    else:
        products = Product.objects.all()

    context = {
        'products': products
    }

    return render(request, 'admin_side/products.html', context)






@login_required(login_url='account:admin_login')
def add_product(request):
    categories = Category.objects.all()
    brands = Brand.objects.all()
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        product_name = request.POST.get('product_name')
        category_id = request.POST.get('category')
        description = request.POST.get('description')
        price = request.POST.get('price')
        brand_id = request.POST.get('brand')
        images = request.FILES.getlist('images[]')
        stock = request.POST.get('stock')

        brand = Brand.objects.get(id=brand_id)
        category = Category.objects.get(pk=category_id) 
        cropped_image_data = request.POST.get('cropped_image')

        product = Product(product_id=product_id,product_name=product_name, description=description,category=category, price=price,brand=brand, rprice=price)
        product.image=images[0]#cropped_image_data#images[0]
        product.save()

        for i in range(len(images)):
            prd_image = ProductImage(product=product, image=images[i])
            prd_image.save()

        return redirect('product:product-list')
    else:
        form=AddProductForm()

    context = {
        'form': form,
        'categories': categories,
        'brands': brands,
    }  
    return render(request, 'admin_side/add_product.html', context)


@login_required(login_url='account:admin_login')
def edit_product(request, product_id):
    categories = Category.objects.all()
    brands = Brand.objects.all()
    
    # Retrieve the product to be edited
    try:
        product = Product.objects.get(pk=product_id)
    except Product.DoesNotExist:
        # Handle the case where the product doesn't exist
        return HttpResponse("Product not found", status=404)

    if request.method == 'POST':
        # Update the product with the form data
        product.product_name = request.POST.get('product_name')
        product.category = Category.objects.get(pk=request.POST.get('category'))
        product.description = request.POST.get('description')
        product.price = request.POST.get('price')
        product.brand = Brand.objects.get(pk=request.POST.get('brand'))
        product.stock = request.POST.get('stock')

        # Handle image updates (if needed)
        new_images = request.FILES.getlist('images[]')
        if new_images:
            # Clear existing product images and add new ones
            ProductImage.objects.filter(product=product).delete()
            for image in new_images:
                prd_image = ProductImage(product=product, image=image)
                prd_image.save()

        # Save the updated product
        product.save()

        return redirect('product:product-list')
    else:
        # Populate the form with existing product data
        form = AddProductForm(instance=product)

    context = {
        'form': form,
        'categories': categories,
        'brands': brands,
        'product': product,  # Include the product object in the context for reference
    }  
    return render(request, 'admin_side/edit_product.html', context)

