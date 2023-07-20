from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages
from ecommerce.models import *
from ecommerce.forms import *
import logging

logger = logging.getLogger(__name__)



def home(request):

    return redirect('shop')
    # return render(request, 'ecommerce/home.html')



def sign_in(request):

    if request.method == "POST":
        r = request.build_absolute_uri()
        next_page = None
        if 'next=' in r:
            next_page = r[r.find('next=')+5:].replace('/','')

        
        login_form = LoginForm(request.POST)
        register_form = RegisterForm(request.POST)

        if login_form.is_valid() and 'submit-login' in request.POST:
            user = authenticate(username=request.POST['email'],password=request.POST['password'])
            if user is not None:
                login(request,user)
                return redirect(next_page if  next_page else 'home')
            
            else:
                return render(request, 'ecommerce/login.html', {'login_form': login_form, 'register_form':register_form, 'message': 'invalid email/password'})
            
        if register_form.is_valid() and 'submit-register' in request.POST:
            user = User.objects.create_user(username=request.POST['email'],password=request.POST['password'])
            Customer.objects.create(user=user,name=request.POST['name'])
            return redirect(request.path_info)
    
    else:
        login_form = LoginForm()
        register_form = RegisterForm()

    return render(request, 'ecommerce/login.html', {'login_form': login_form, 'register_form':register_form, 'message': ''})


@login_required
def account(request):
    return render(request, 'ecommerce/account.html')


def shop(request):
    products = Product.objects.all()
    return render(request, 'ecommerce/shop.html', {'products': products})



def product(request,productSlug):
    product = Product.objects.get(slug=productSlug)

    if request.method == "POST":
        product_form = ProductForm(request.POST)

        if product_form.is_valid():
          customer = Customer.objects.get(user=request.user)
          order, val = Order.objects.get_or_create(customer=customer, complete=False)
          orderitem = OrderItem.objects.create(product=product,order=order,quantity=1,size=request.POST['size'])
          return redirect(request.path_info)
    
    else:
        product_form = ProductForm()

    return render(request, 'ecommerce/product.html', {'product': product, 'product_form': product_form})



def contact(request):
    message_list = [str(message) for message in list(messages.get_messages(request))]
    

    if request.method == "POST":
        contact_form = ContactForm(request.POST)
        contact_history_form = ContactHistoryForm(request.POST)

        if contact_form.is_valid():
          contact_form.save()
          messages.add_message(request, messages.INFO, 'Message Sent')
          return redirect(request.path_info)
        
        if contact_history_form.is_valid() and not any(key in ['subject','message', 'purpose'] for key in request.POST.keys()):
            messages.add_message(request, messages.INFO, request.POST['email'])
            messages.add_message(request, messages.INFO, request.POST['name'])
            return redirect('contact_history')
    
    else:
        contact_form = ContactForm()
        contact_history_form = ContactHistoryForm()
    
    return render(request, 'ecommerce/contact.html', {'contact_form': contact_form, 'contact_history_form': contact_history_form, 'message': message_list})



def contact_history(request):
    try:
        if request.META['HTTP_REFERER'] != 'http://127.0.0.1:8000/contact/':
            return redirect('contact')
    except:
        return redirect('contact')
    

    message_list = [str(message) for message in list(messages.get_messages(request))]
    try:
        email, name = message_list[0], message_list[1]
        messages.add_message(request, messages.INFO, 'eqwalton@gmail.com')
        messages.add_message(request, messages.INFO, 'Ethan Walton')
    except:
        messages.add_message(request, messages.ERROR, 'Session Expired')
        return redirect('contact')

    contact_requests = ContactRequest.objects.filter(email=email, name=name)

    return render(request, 'ecommerce/contact_history.html', {'contact_requests': contact_requests})


@login_required
def cart(request):
    customer = Customer.objects.get(user=request.user)
    order = Order.objects.get(customer=customer, complete=False)
    cart_items = OrderItem.objects.filter(order=order)
    len_items = sum([item.quantity for item in cart_items])
    order_total = round(sum([item.get_total for item in cart_items]),2)


    if request.method == "POST":
        if 'submit' in request.POST:
            product = request.POST['product']
            type = request.POST['submit']
            size = request.POST['size']
            item = [item for item in cart_items if item.product.name == product and item.size == size][0]

            if type == 'increment':
                item.quantity += 1
                item.save()
            elif type == 'decrement':
                item.quantity -= 1
                item.save()
                if item.quantity == 0:
                    item.delete()
            else:
                item.delete()
                

        return redirect('cart')

            

    return render(request, 'ecommerce/cart.html', {'cart_items': cart_items, 'len_items': len_items, 'order_total': order_total})


@login_required
def checkout(request):


    return render(request, 'ecommerce/checkout.html')
