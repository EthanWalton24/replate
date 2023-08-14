from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages
from allauth.utils import generate_unique_username
from ecommerce.models import *
from ecommerce.forms import *
import logging, uuid

logger = logging.getLogger(__name__)




def sign_in(request):

    if request.method == "POST":
        r = request.build_absolute_uri()
        next_page = None
        if 'next=' in r:
            next_page = r[r.find('next=')+5:].replace('/','')

        
        login_form = LoginForm(request.POST)
        register_form = RegisterForm(request.POST)

        if login_form.is_valid() and 'submit-login' in request.POST:
            try:
                users = User.objects.filter(email=request.POST['email'])
                user=None
                for u in users:
                    if u.check_password(request.POST['password']):
                        user = u
                        break
            except:
                user = None

            if user is not None:
                login(request,user,backend='django.contrib.auth.backends.ModelBackend')
                return redirect(next_page if  next_page else 'shop')
            else:
                return render(request, 'ecommerce/login.html', {'login_form': login_form, 'register_form':register_form, 'message': 'invalid email/password'})
            
        if register_form.is_valid() and 'submit-register' in request.POST:
            user, val = User.objects.get_or_create(username=request.COOKIES['device'])
            user.email = request.POST['email']
            user.set_password(request.POST['password'])
            user.first_name = request.POST['name'].split()[0]
            user.last_name = request.POST['name'].split()[-1]
            login(request,user,backend='django.contrib.auth.backends.ModelBackend')
            return redirect(request.path_info)
    
    else:
        login_form = LoginForm()
        register_form = RegisterForm()

    return render(request, 'ecommerce/login.html', {'login_form': login_form, 'register_form':register_form, 'message': ''})


@login_required
def account(request):

    if request.method == "POST":

        if request.POST['which'] == 'profile':
            #redirect to GET request if form is invalid
            if any(field == '' for field in [request.POST['first_name'],request.POST['last_name'],request.POST['email']]):
                return redirect(request.path_info)
            
            user = request.user
            user.first_name = request.POST['first_name']
            user.last_name = request.POST['last_name']
            user.email = request.POST['email']
            if request.POST['password'] != '':
                user.set_password(request.POST['password'])
            user.save()

        elif request.POST['which'] == 'add-shipping':
            #redirect to GET request if form is invalid
            if any(field == '' for field in [request.POST['first_name'],request.POST['last_name'],request.POST['phone'],request.POST['address'],request.POST['apt'],request.POST['city'],request.POST['state'],request.POST['zip']]):
                return redirect(request.path_info)
            
            address,val = ShippingAddress.objects.get_or_create(
                                                            user=request.user,
                                                            name=f"{request.POST['first_name']} {request.POST['last_name']}",
                                                            phone=request.POST['phone'],
                                                            address_line_1=request.POST['address'],
                                                            address_line_2=request.POST['apt'],
                                                            city=request.POST['city'],
                                                            state=request.POST['state'],
                                                            zipcode=request.POST['zip']
                                                        )

        elif request.POST['which'] == 'delete-shipping':
            address = ShippingAddress.objects.get(pk=request.POST['address'])
            address.delete()
        # elif request.POST['which'] == 'add-payment':

        # elif request.POST['which'] == 'delete-payment':

        else:
            return redirect(request.path_info)


    shipping_addresses = ShippingAddress.objects.filter(user=request.user)
    orders = Order.objects.filter(user=request.user,complete=True)
    return render(request, 'ecommerce/account.html', {'shipping_addresses': shipping_addresses, 'orders': orders})


def shop(request):
    products = Product.objects.all()
    return render(request, 'ecommerce/shop.html', {'products': products})



def product(request,productSlug):
    product = Product.objects.get(slug=productSlug)

    if request.method == "POST":
        product_form = ProductForm(request.POST)

        if not request.user.is_authenticated:
            user, val = User.objects.get_or_create(username=request.COOKIES['device'])
        else:
            user = request.user


        if product_form.is_valid():
            if len(Order.objects.filter(user=user, complete=False)) == 0:
                order = Order.objects.create(order_number=str(uuid.uuid4().int>>64).replace('-','')[:10],user=user,complete=False)
            else:
                order = Order.objects.filter(user=user, complete=False)[0]

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
    user = request.user
    try:
        order = Order.objects.get(user=user, complete=False)
        len_items = sum([item.quantity for item in order.get_items()])
    except:
        order = None
        len_items = 0

    codes = dict(Order._meta.get_field('code').choices[1:])

    

    if request.method == "POST":

        if 'which' in request.POST:
            if len(ShippingAddress.objects.filter(user=request.user,name=f"{request.POST['first_name']} {request.POST['last_name']}",phone=request.POST['phone'],address_line_1=request.POST['address'],address_line_2=request.POST['apt'],city=request.POST['city'],state=request.POST['state'],zipcode=request.POST['zip'])) > 0:
                address = ShippingAddress.objects.filter(user=request.user,name=f"{request.POST['first_name']} {request.POST['last_name']}",phone=request.POST['phone'],address_line_1=request.POST['address'],address_line_2=request.POST['apt'],city=request.POST['city'],state=request.POST['state'],zipcode=request.POST['zip'])
            else:
                address = ShippingAddress.objects.create(user=request.user,name=f"{request.POST['first_name']} {request.POST['last_name']}",phone=request.POST['phone'],address_line_1=request.POST['address'],address_line_2=request.POST['apt'],city=request.POST['city'],state=request.POST['state'],zipcode=request.POST['zip'])
            address.save()
            order.shipping_address = address
            order.shipping_method = request.POST['shipping-method']
            order.complete = True
            order.completed_total = request.POST['completed-total']
            order.tracking = 'https://tools.usps.com/go/TrackConfirmAction_input'
            if 'code' in request.POST:
                order.code = request.POST['code']
            order.save()

            return redirect(f'/order/{order.order_number}')


        else:
            product = request.POST['product']
            type = request.POST['submit']
            size = request.POST['size']
            item = [item for item in order.get_items() if item.product.name == product and item.size == size][0]

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
                
        if len(OrderItem.objects.filter(order=order)) == 0:
            order.delete()
            

        return redirect('cart')

    return render(request, 'ecommerce/cart.html', {'order': order, 'len_items': len_items, 'codes': codes})



@login_required
def order(request,order_number):
    order = Order.objects.get(order_number=order_number)

    return render(request, 'ecommerce/order.html', {'order': order})
