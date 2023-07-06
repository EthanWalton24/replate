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



# @register.simple_tag
# def row(extra_classes=""):
#     return format_html('<div class="row {}">', extra_classes)
# @register.simple_tag
# def endrow():
#     return format_html("</div>")


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