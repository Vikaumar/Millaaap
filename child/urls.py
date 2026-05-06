from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls import url
from django.contrib.auth.views import (
    LoginView, LogoutView
    )
from . import views
from django.conf.urls.static import static
urlpatterns=[
    path('',views.home,name="home"),
    path('login/',LoginView.as_view(template_name='child/login.html')),
    path('addmember/',views.addmember),
    path('aboutus/',views.aboutus,name="aboutus"),
    path('howitworks/',views.howitworks,name="howitworks"),
    path('dashboard/',views.dashboard),
    path('logout/',LogoutView.as_view(template_name='child/logout.html')),
    path('register/',views.register),
    path('allmembers/',views.allmembers,name='child/allmembers'),
    path('laststep/',views.laststep),
    path('congrats/',views.congrats),
    path('search/',views.searchmember),
    path('searchresult/',views.searchresult),
    path('addtolost/<int:id>',views.addtolost,name='child/addtolost'),
    path('deletefromlost/<int:id>',views.deletefromlost,name='child/deletefromlost'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/(?P<year>[0-9]{1,10})/$',views.activate, name='activate'),
    path('childdetails/',views.childdetails),
]
