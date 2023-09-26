from django.shortcuts import render,redirect,HttpResponseRedirect,get_object_or_404
from category.models import *
from .models import *
from django.contrib import messages
from django.urls import reverse
import json
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
# Create your views here.

def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart




def add_cart(request, product_id):
    color = request.GET.get('color')
    size = request.GET.get('size')

    print(color, size)
    
    product = Product.objects.get(product_id=product_id)
    
    try:
        variant = Variation.objects.get(id=size)
    except Variation.DoesNotExist:
        try:
            variant = Variation.objects.get(id=color)
        except Variation.DoesNotExist:
            # Handle the case where neither color nor size exists
            messages.warning(request, 'Invalid variation.')
            return redirect('product_detail', product_id)

    if variant.stock >= 1:
        if request.user.is_authenticated:
            is_cart_item_exists = CartItem.objects.filter(user=request.user, product=product, variations=variant).exists()
            if is_cart_item_exists:
                to_cart = CartItem.objects.get(user=request.user, product=product, variations=variant)
                to_cart.quantity += 1
            else:
                to_cart = CartItem(user=request.user, product=product, quantity=1)
                to_cart.save()
                to_cart.variations.set([variant])  # Use set() to manage the many-to-many relationship
            to_cart.save()
            return redirect('cart:shopping_cart')
        else:
            try:
                cart = Cart.objects.get(cart_id=_cart_id(request))
            except Cart.DoesNotExist:
                cart = Cart.objects.create(cart_id=_cart_id(request))
            
            is_cart_item_exists = CartItem.objects.filter(cart=cart, product=product, variations=variant).exists()
            if is_cart_item_exists:
                to_cart = CartItem.objects.get(cart=cart, product=product, variations=variant)
                to_cart.quantity += 1
            else:
                to_cart = CartItem(cart=cart, product=product, quantity=1)
                to_cart.save()
                to_cart.variations.set([variant])  # Use set() to manage the many-to-many relationship
            to_cart.save()
            return redirect('cart:shopping_cart')
    else:
        messages.warning(request, 'This item is out of stock.')
        return redirect('product_detail', product_id)






            



def add_quantity_to_cart(request, product_id, cart_item_id):
    product = get_object_or_404(Product, product_id=product_id)
    
    try:
        # Get the specific cart item by ID
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
        else:
            cart_item = CartItem.objects.get(product=product, cart__cart_id=_cart_id(request), id=cart_item_id)
        
        # Check if there are any variations associated with the product
        if product.variation_set.exists():
            # You may want to choose a specific variation to increment quantity
            # In this example, I'll just increment the quantity of the first variation
            first_variation = product.variation_set.first()
            if first_variation.stock >= 1 and cart_item.quantity < first_variation.stock:
                cart_item.quantity += 1
                cart_item.save()
            else:
                print("Not enough stock for the selected variation")
        else:
            # Handle products without variations here
            if cart_item.quantity < product.stock:
                cart_item.quantity += 1
                cart_item.save()
            else:
                print("Not enough stock for the product")
    
    except CartItem.DoesNotExist:
        pass  # Handle the case where the cart item doesn't exist

    # Redirect back to the shopping cart page
    return HttpResponseRedirect(reverse('cart:shopping_cart'))






def remove_cart(request, product_id, cart_item_id):
    
    product = get_object_or_404(Product, product_id=product_id)

    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
        if cart_item.quantity > 1:
            variant = cart_item.variations
            variant.stock += 1
            cart_item.quantity -= 1

            variant.save()
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass
    return redirect('cart:shopping_cart')



def remove_cart_item(request, product_id, cart_item_id):
    product = get_object_or_404(Product, product_id=product_id)

    try:
        if request.user.is_authenticated:
            # If the user is authenticated, remove the cart item associated with the user
            cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
        else:
            # If the user is not authenticated, remove the cart item associated with the session cart
            cart_item = CartItem.objects.get(product=product, cart__cart_id=_cart_id(request), id=cart_item_id)
        
        # Delete the cart item
        cart_item.delete()
    except CartItem.DoesNotExist:
        pass  # Handle the case where the cart item doesn't exist

    # Redirect back to the shopping cart page
    return redirect('cart:shopping_cart')



def cart(request, total=0, quantity=0, cart_items=None):
    try:
        tax=0
        grand_total=0
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id = _cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (2 * total)/100
        grand_total = total+tax
    except ObjectDoesNotExist:
        pass 

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total
    }

    return render(request, 'user_side/shoping-cart.html', context)


def get_cart_count(request):
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user, is_active=True)
    else:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
    
    count = cart_items.count()
    
    return JsonResponse({'count': count})
    



def newcart_update(request):
  new_quantity = 0
  if request.method == 'POST':
    if request.user.is_authenticated:
      prod_id = int(request.POST.get('product_id'))
      cart_item_id = int(request.POST.get('cart_id'))
      product = get_object_or_404(Product, product_id=prod_id)
      cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
      if product.variation_set.exists():
        first_variation = product.variation_set.first()
        if first_variation.stock >= 1 and cart_item.quantity < first_variation.stock:
          cart_item.quantity += 1
          cart_item.save()
          new_quantity = cart_item.quantity
        else:
          new_quantity = cart_item.quantity
      else:
        if cart_item.quantity < product.stock:
          cart_item.quantity += 1
          cart_item.save()
          new_quantity = cart_item.quantity
        else:
          new_quantity = cart_item.quantity

  if new_quantity == 0:
    return JsonResponse({'status': "out of stock"})
  else:
    return JsonResponse({'status': "success", 'new_quantity': new_quantity})

  # This code is unreachable because the return statement above will always execute
