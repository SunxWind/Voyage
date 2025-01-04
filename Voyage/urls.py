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

from viewer.views import (
    IndexView, TripDetailsView, TripCreateView, TripPurchaseView, CustomLoginView, RegisterView, ProfileView, logout_page
)

from django.contrib.auth import views
import Voyage.settings as settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path(r'^chaining/', include('smart_selects.urls',)),
    path('', IndexView.as_view(), name='index'),
    path('trip/details', TripDetailsView.as_view(), name='trip_details'),
    path('trip_purchase', TripPurchaseView.as_view(), name='trip_purchase'),
    # path('some_page', SomePageView.as_view(), name='some_page'),
    path('trip_add', TripCreateView.as_view(), name='trip_add'),

    path('accounts/login', CustomLoginView.as_view(), name='login'),
    path('logout_page', logout_page, name='logout_page'),  # Does not work properly. Redirects to django default logout page, insted of user template loggedout.html.
    path('accounts', include('django.contrib.auth.urls')),
    path('register', RegisterView.as_view(), name='register'),
    path('profile', ProfileView.as_view(), name='profile'),
]

if settings.DEBUG:  # new
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
