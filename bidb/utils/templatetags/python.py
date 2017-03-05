import operator

from django import template

register = template.Library()


for fn in (
    operator.getitem,
):
    register.filter(fn.__name__, lambda x, y: fn(x, y))
