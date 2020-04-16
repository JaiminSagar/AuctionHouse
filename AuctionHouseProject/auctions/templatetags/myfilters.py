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

# @register.filter(name='first')
# def first(value,arg):
#     if arg == "firstname":
#         return value[0].first_name
#     if arg == "lastname":
#         return value[0].last_name
#     if arg == "user_bid_amount":
#         return value[0].user_bid_amount
#     if arg == "bid_time":
#         return value[0].bid_time
#     return value
