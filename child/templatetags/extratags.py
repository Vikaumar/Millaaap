from child.models import esehi
from django import template
register = template.Library()

@register.filter(name='filter')
def filter(t):
	return esehi.objects.filter(id=t).count()

#@register.filter(name='add1')
#def add1():
#	return esehi.objects.all().count()