"""groupformer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import include, path
urlpatterns = [
    path('setup_screen/', include('setup_screen.urls')),
    path('min_iteration2/', include('min_iteration2.urls')),
    path('response_screen/', include('response_screen.urls')),
    path('admin/', admin.site.urls),
    path('dbtools/', include('dbtools.urls')),
]
