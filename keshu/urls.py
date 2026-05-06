# pyrefly: ignore [missing-import]
"""keshu URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# pyrefly: ignore [missing-import]
from django.contrib import admin
# pyrefly: ignore [missing-import]
from django.urls import path,include
# pyrefly: ignore [missing-import]
from django.conf.urls.static import static
# pyrefly: ignore [missing-import]
from django.conf import settings
# pyrefly: ignore [missing-import]
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('child/',include('child.urls')),
    path('', RedirectView.as_view(url='/child/', permanent=True)),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



    
 
