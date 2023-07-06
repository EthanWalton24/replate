from django.shortcuts import redirect, render, get_object_or_404
from django.utils import timezone
from ecommerce.models import *
from ecommerce.forms import *
import logging

logger = logging.getLogger(__name__)



def home(request):

    return render(request, 'ecommerce/home.html')



def shop(request):

    return render(request, 'ecommerce/shop.html')



def contact(request):

    return render(request, 'ecommerce/contact.html')



def cart(request):

    return render(request, 'ecommerce/cart.html')
