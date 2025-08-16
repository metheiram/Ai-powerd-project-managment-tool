# data/templatetags/custom_filters.py

from django import template

register = template.Library()

@register.filter(name='to')  # ✅ 'to' naam se register ho raha hai
def to(value, arg):
    try:
        return range(int(value), int(arg)+ 1)
    except:
        return []
