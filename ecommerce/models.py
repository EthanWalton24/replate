from django.db import models
from django.conf import settings
from django.template.defaultfilters import slugify
from decimal import Decimal



class ShippingAddress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True)
    name = models.CharField(max_length=200,null=True)
    phone = models.CharField(max_length=10,null=True)
    address_line_1 = models.CharField(max_length=300,null=True)
    address_line_2 = models.CharField(max_length=300,null=True)
    city = models.CharField(max_length=200,null=True)
    state = models.CharField(max_length=200,null=True)
    zipcode = models.CharField(max_length=200,null=True)


    def __str__(self):
        return str(self.id)



class Product(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=200,null=True)
    artist = models.CharField(max_length=200,null=True,blank=True)
    image = models.ImageField(null=True, blank=True)
    price = models.DecimalField(max_digits=8,decimal_places=2)
    category = models.CharField(max_length=19,choices=[
                                                        ('Hip-Hop/Rap','Hip-Hop/Rap'),
                                                        ('R&B/Soul','R&B/Soul'),
                                                        ('Pop','Pop'),
                                                        ('Dance','Dance')
                                                        ],default='Hip-Hop/Rap')
    available = models.BooleanField(default=True,blank=False)
    slug = models.SlugField(blank=True)
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.id:
            # Newly created object, so set slug
            self.slug = slugify(self.name)

        super(Product, self).save(*args, **kwargs)
    


class Order(models.Model):
    order_number = models.CharField(max_length=300, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    shipping_address = models.ForeignKey(ShippingAddress, on_delete=models.CASCADE, null=True, blank=True)
    shipping_method = models.CharField(max_length=30 ,choices=[('Ground','Ground'),('Priority','Priority'),('Express','Express')],default='Ground')
    complete = models.BooleanField(default=False, null=True, blank=False)
    completed_total = models.CharField(max_length=20, null=True, blank=True)
    status = models.CharField(max_length=30 ,choices=[('Processing','Processing'),('Shipped','Shipped'),('Delivered','Delivered')],default='Processing')
    tracking = models.TextField(null=True, blank=True)
    code = models.CharField(max_length=19,choices=[
                                                    ('none',0),
                                                    ('WPFKPXNX',5),
                                                    ('20OFF',20)
                                                ],default='none')
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)
    
    def get_total(self):
        items = OrderItem.objects.filter(order=self)
        return sum([item.get_total for item in items])
    
    def get_items(self):
        return OrderItem.objects.filter(order=self)
    


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL,blank=True,null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL,blank=True,null=True)
    quantity = models.IntegerField(default=1, null=True,blank=True)
    size = models.CharField(max_length=30 ,choices=[('M','M   (17.7"/12.6")'),('L','L   (26.6"/18.9")'),('XL','XL   (35.4"/25.2")')])
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        size_price = float(f"{((self.product.price * 1 - Decimal(.01)) if self.size == 'M' else (self.product.price * 2 - Decimal(.01)) if self.size == 'L' else (self.product.price * 3 - Decimal(.01))):.2f}")
        return round(size_price * self.quantity,2)
    



class ContactRequest(models.Model):
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    purpose = models.CharField(max_length=30,choices=[
                                                    ('Support','Support'),
                                                    ('Request Custom Poster','Request Custom Poster'),
                                                    ('Returns','Returns')
                                                    ],default='Support')
    subject = models.CharField(max_length=200, null=True)
    message = models.TextField()
    status = models.CharField(max_length=15,choices=[
                                                    ('Open','Open'),
                                                    ('Complete','Complete')
                                                    ],default='Open')
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return str(self.id)