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
from rest_framework.authtoken import views as auth_views
router = DefaultRouter()
#router.register('hello-viewset',views.HelloViewSet,base_name='hello-viewset')#name of url
router.register('profile',views.UserProfileViewSet) #no need of base_name since there is a queryset
#router.register('feed',views.UserProfileFeedViewSet)

urlpatterns = [
    path('',include(router.urls)),
    #re_path(r'^signin/$', views.LoginView.as_view(template_name='rest_framework/login.html'), name='login'),
    #path(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    #path(r'^login', login, template_name, name='login'),
    #url(r'^logout', logout, template_name, name='logout'),
    path('login/', views.UserLoginApiView.as_view()),
    #path('login2/', views.Login.as_view()),
    path('api-token-auth/', auth_views.obtain_auth_token, name='api-tokn-auth'), 
    
    re_path(r'^api/products/$', views.ProductListAPIView.as_view(), name='products'),
    re_path(r'^api/products/(?P<pk>\d+)/$', views.ProductRetrieveAPIView.as_view(), name='product_detail'),
    
    re_path(r'^api/orders/$', views.OrderListAPIView.as_view(), name='orders_api'),
    re_path(r'^api/orders/(?P<pk>\d+)/$', views.OrderRetrieveAPIView.as_view(), name='order_detail_api'),
]
