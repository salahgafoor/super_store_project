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

from accounts.views import *
from rest_framework.authtoken import views as rest_auth_views
from django.contrib.auth import views as auth_views
router = DefaultRouter()
router.register('profile', UserProfileViewSet) 

urlpatterns = [
    path('',include(router.urls)),
    # templates
    re_path(r'^index/$',dashboardView.as_view(),name='dashboardView'),
    re_path(r'login/$', auth_views.LoginView.as_view(template_name="accounts/login.html"),name="login"),
    re_path(r'logout/$', auth_views.LogoutView.as_view(), name="logout"),    
    re_path(r'signup/$', SignUp.as_view(), name="signup"),
    path('login/', UserLoginApiView.as_view()),
    path('api-token-auth/', rest_auth_views.obtain_auth_token, name='api-tokn-auth'), 
    
    path('product/<pk>/', ProductView.as_view(), name='product'),
    path('cart/<pk>/', add_to_cart, name='add-to-cart'),
    path('cart-items/', CartItemsView.as_view(), name='cart-items'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('place-order/', PlaceOrderView.as_view(), name='place-order'),
    # API
    re_path(r'^api/products/$', ProductListAPIView.as_view(), name='products'),
    re_path(r'^api/products/(?P<pk>\d+)/$', ProductRetrieveAPIView.as_view(), name='product_detail'),    
    re_path(r'^api/orders/$', OrderListAPIView.as_view(), name='orders_api'),
    re_path(r'^api/orders/(?P<pk>\d+)/$', OrderRetrieveAPIView.as_view(), name='order_detail_api'),
]
