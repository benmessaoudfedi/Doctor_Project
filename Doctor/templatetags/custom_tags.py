from django import template

register = template.Library()

@register.filter(name='copy_name')
def copy_name(name):
   return str(name)[max(index for index, item in enumerate(str(name)) if item == '/') + 1:]
