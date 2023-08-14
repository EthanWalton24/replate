from django.contrib.auth import get_user_model
from django import template
from django.utils.html import escape, format_html
from django.utils.safestring import mark_safe
from ecommerce.models import *


register = template.Library()
user_model = get_user_model()

# @register.filter
# def author_details(author, current_user=None):
#   if not isinstance(author,user_model):
#     return ""
  
#   if author == current_user:
#     return mark_safe("<strong>me</strong>")

#   if author.first_name and author.last_name:
#     name = escape(f"{author.first_name} {author.last_name}")
#   else:
#     name = escape(f"{author.username}")


#   if author.email:
#     name = f'<a href="mailto:{escape(author.email)}">{name}</a>'


#   return mark_safe(name)


@register.filter
def math(val1, args):
    val2, type = args.split(',')
    if 'add' in type:
        return float(val1)+float(val2)
    if 'sub' in type:
        return float(val1)-float(val2)
    if 'mult' in type:
        return float(val1)*float(val2)
    else:
        return float(val1)/float(val2)




@register.simple_tag(takes_context=True)
def cart_count(context):
    if context['request'].user.is_authenticated:
        try:
            user = context['request'].user
            order = Order.objects.get(user=user,complete=False)
            orderitems = OrderItem.objects.filter(order=order)

            cart_count = sum([item.quantity for item in orderitems])
            return format_html('<span id="cart-count">{}</span>', cart_count)
        except:
            return mark_safe('<span id="cart-count">0</span>')
    else:
        return mark_safe('<span id="cart-count">0</span>')


# @register.simple_tag
# def col(extra_classes=""):
#     return format_html('<div class="col {}">', extra_classes)
# @register.simple_tag
# def endcol():
#     return format_html("</div>")


# @register.inclusion_tag("blog/post-list.html")
# def recent_posts(post):
#     posts = Post.objects.exclude(pk=post.pk)[:5]
#     return {"title": "Recent Posts", "posts": posts}