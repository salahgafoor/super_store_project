"""

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
from django.urls import path, re_path, include

app_name = 'accounts'

from rest_framework.routers import DefaultRouter

from accounts import views

router = DefaultRouter()
#router.register('hello-viewset',views.HelloViewSet,base_name='hello-viewset')#name of url
router.register('profile',views.UserProfileViewSet) #no need of base_name since there is a queryset
#router.register('feed',views.UserProfileFeedViewSet)

urlpatterns = [
    path('',include(router.urls)),
    path('login/', views.UserLoginApiView.as_view()),

]
