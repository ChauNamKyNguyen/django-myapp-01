from django import template

# My model
from jav.models import Actress

register = template.Library()

# Filter requires one or two arguments. 

@register.filter 
def cut(value, arg):
    """Removes all values of arg from the given string"""
    return value.replace(arg, '')    
    
@register.filter
def lower(value):
    return value.lower()
    
@register.inclusion_tag('jav/all_actress_tag.html')
def show_actress(selected):
    actresses = Actress.objects.all()
    return {'actresses' : actresses, 'selected_actress': selected}
    

