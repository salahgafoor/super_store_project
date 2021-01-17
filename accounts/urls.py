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
from django.urls import path, re_path, include

app_name = 'accounts'

from rest_framework.routers import DefaultRouter

from accounts import views
from rest_framework.authtoken import views as rest_auth_views
from django.contrib.auth import views as auth_views
router = DefaultRouter()
router.register('profile',views.UserProfileViewSet) 

urlpatterns = [
    path('',include(router.urls)),
    # templates
    re_path(r'^index/$',views.dashboardView.as_view(),name='dashboardView'),
    re_path(r'login/$', auth_views.LoginView.as_view(template_name="accounts/login.html"),name="login"),
    re_path(r'logout/$', auth_views.LogoutView.as_view(), name="logout"),    
    re_path(r'signup/$', views.SignUp.as_view(), name="signup"),
    path('login/', views.UserLoginApiView.as_view()),
    path('api-token-auth/', rest_auth_views.obtain_auth_token, name='api-tokn-auth'), 
    
    path('product/<pk>/', views.ProductView.as_view(), name='product'),
    # API
    re_path(r'^api/products/$', views.ProductListAPIView.as_view(), name='products'),
    re_path(r'^api/products/(?P<pk>\d+)/$', views.ProductRetrieveAPIView.as_view(), name='product_detail'),    
    re_path(r'^api/orders/$', views.OrderListAPIView.as_view(), name='orders_api'),
    re_path(r'^api/orders/(?P<pk>\d+)/$', views.OrderRetrieveAPIView.as_view(), name='order_detail_api'),
]
