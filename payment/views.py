from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse, FileResponse, HttpResponseRedirect
from cart.models import *
from category.models import*
from account.models import *
from user.models import *
import json
import razorpay
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.contrib import messages


@login_required(login_url='login')    
def payments(request):
    id=request.GET.get('order_id')
    payment_id=request.GET.get('payment_id')
    payment_method=request.GET.get('method')
    payment_order_id=request.GET.get('payment_order_id')
    discount=request.GET.get('discount')
    status=request.GET.get('status')

    print(id,payment_id,payment_method,payment_order_id)
    try:
        order = Order.objects.get(user=request.user, is_ordered=False, order_number=id)
    except Order.DoesNotExist:
        pass

    #Store transaction details inside Payment model
    payment = Payment(
        user = request.user,
        payment_id =payment_id,
        payment_method = payment_method,
        amount_paid = order.order_total,
        status = status,
        discount = discount,
    )
    print(payment)
    payment.save()

    order.payment = payment
    order.is_ordered = True
    order.save()


    #Move the cart items to orderproduct table

    cart_items = CartItem.objects.filter(user=request.user)

    for item in cart_items:
        item.variations.stock-=item.quantity
        print(item.variations.stock,item.quantity,item)
        item.variations.save()
        orderproduct = OrderProduct()
        orderproduct.order_id = order.id 
        orderproduct.payment = payment
        orderproduct.user_id = request.user.id
        orderproduct.product_id = item.product_id
        orderproduct.quantity = item.quantity
        orderproduct.product_price = item.product.price
        orderproduct.ordered = True
        orderproduct.save()



    #Clear cart
    cart_items.delete()
    

    #Send order received email to customer
    mail_subject = 'Thank you for your order!'
    message = render_to_string('user_side/order_received_email.html', {
        'user': request.user,
        'order':order
    })
    to_email = request.user.email
    email = EmailMessage(mail_subject, message, to=[to_email])
    email.send()
    ordered_products = OrderProduct.objects.filter(order_id=order.id)
    subtotal = 0
    for i in ordered_products:
            subtotal += i.product_price * i.quantity
    context = {
            'order': order,
            'ordered_products': ordered_products,
            'order_number': order.order_number,
            'transID': payment.payment_id,
            'subtotal': subtotal,
            'payment': payment,

        }
    messages.success(request, 'Payment successful...')
    

    return render(request, 'user_side/order_confirmed.html',context)


