from django import template

register = template.Library()

@register.filter(name='multiply')
def multiply(value, arg):
   if isinstance(value, str) and isinstance(arg, int):
       return str(value) * arg
   else:
       raise ValueError(f'Нельзя умножить {type(value)} на {type(arg)}')

STOP_LIST = [
       "mat1",
       "mat2",
       "mat3",
   ]
@register.filter(name='censor')
def censor(value):
    for word in STOP_LIST:
        if word in value:
            return str("***")
        else:
            return str(value)

