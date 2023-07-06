from django.shortcuts import redirect, render, get_object_or_404
from django.utils import timezone
from ecommerce.models import *
from ecommerce.forms import *
import logging

logger = logging.getLogger(__name__)



def home(request):

    return render(request, 'ecommerce/home.html')



def shop(request):
    products = Product.objects.all()
    return render(request, 'ecommerce/shop.html', {'products': products})



def product(request,productSlug):
    product = Product.objects.get(slug=productSlug)

    return render(request, 'ecommerce/product.html')



def contact(request):

    return render(request, 'ecommerce/contact.html')



def cart(request):

    return render(request, 'ecommerce/cart.html')
