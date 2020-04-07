from django  import template
import math
register=template.Library()

@register.filter(name='cut')       #This line will wrap our function as filter    You can also visit decorater in python level 2
def cut(value):
    if 'p.m.' in value:
        args='p.m.'
    if 'a.m.' in value:
        args='a.m.'
    return value.replace(args,'')

@register.filter(name='multiply')
def multiply(value,arg):
    return math.ceil(float(value)*float(arg))