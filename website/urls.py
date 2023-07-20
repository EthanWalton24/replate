"""
URL configuration for website project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
import ecommerce.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', ecommerce.views.home, name='home'),
    path('login/', ecommerce.views.sign_in, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('account/', ecommerce.views.account, name='account'),
    path('shop/', ecommerce.views.shop, name='shop'),
    path('product/<productSlug>/', ecommerce.views.product, name='product'),
    path('contact/', ecommerce.views.contact, name='contact'),
    path('contact-history/', ecommerce.views.contact_history, name='contact_history'),
    path('cart/', ecommerce.views.cart, name='cart'),
    path('checkout/', ecommerce.views.checkout, name='checkout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)