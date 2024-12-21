"""
URL configuration for Voyage project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path, include
from django.contrib.auth import views
import smart_selects

from viewer.views import IndexView, TripCreateView, CustomLoginView

urlpatterns = [
    path('admin/', admin.site.urls),
    path(r'^chaining/', include('smart_selects.urls',)),
    path('', IndexView.as_view(), name='index'),
    path('trip_add', TripCreateView.as_view(), name='trip_add'),

    path('login', CustomLoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
]
