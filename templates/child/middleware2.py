import re
from django.conf import settings
from django.urls import reverse
from django.shortcuts import redirect,render
from django.http import HttpResponseRedirect
#from django.contrib.flatpages.views import flatpage
from django.contrib.auth import logout
EXEMPT_URLS=[re.compile(settings.LOGIN_URL.lstrip('/'))]
if hasattr(settings,'LOGIN_EXEMPT_URLS'):
	EXEMPT_URLS+=[re.compile(url) for url in settings.LOGIN_EXEMPT_URLS]
class LoginRequiredMiddleware:
	def __init__(self,get_response):
		self.get_response = get_response
	def __call__(self,request):
		response = self.get_response(request)
		return response
	def process_view(self,request,view_func,view_args,view_kwargs):
		flag=0
		assert hasattr(request,'user')
		path=request.path_info.lstrip('/')
		if not request.user.is_authenticated:
			if not any(url.match(path) for url in EXEMPT_URLS):
				print("Hello Keshav")
				return redirect(settings.LOGIN_URL)
		url_is_exempt=any(url.match(path) for url in EXEMPT_URLS)
		if path=='/childfinder/logout':
			logout(request)
		if flag==0:
			if request.user.is_authenticated and url_is_exempt:
				flag=1
				return HttpResponseRedirect('/childfinder/dashboard')
			elif request.user.is_authenticated or url_is_exempt:
				print("Hello Keshav2")
				return None
			else:
				print("Hello Keshav3")
				return redirect(settings.LOGIN_URL)

