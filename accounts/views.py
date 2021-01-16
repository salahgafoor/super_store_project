from rest_framework import status
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework import filters
import django_filters.rest_framework
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework import generics
from .serializer import *
from django.shortcuts import render
from accounts import serializer, models, permissions
from .permissions import IsOwnerAndAuth

class UserProfileViewSet(viewsets.ModelViewSet):
    """Handle creating and updating profiles"""
    serializer_class = serializer.UserProfileSerializer
    queryset = models.UserProfileInfo.objects.all()
    
    # enable authentication; one user can modify only his details
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateOwnProfile,) #trigger has_object_permission function inside permissions.py file
    
    #searching of users
    filter_backends = (filters.SearchFilter,) 
    search_fields = ('name','email',)

class UserLoginApiView(ObtainAuthToken):
    """Handle creating user authentcation tokens"""
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

class ProductListAPIView(generics.ListAPIView):
    #permission_classes = [IsAuthenticated]
    queryset = models.Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [
                    filters.SearchFilter, 
                    filters.OrderingFilter, 
                    django_filters.rest_framework.DjangoFilterBackend,
                    ]
    search_fields = ["title", "description"]
    ordering_fields  = ["title", "id"]
    #filter_class = ProductFilter
    #pagination_class = ProductPagination


class ProductRetrieveAPIView(generics.RetrieveAPIView):
    queryset = models.Product.objects.all()
    serializer_class = ProductDetailSerializer


class OrderRetrieveAPIView(generics.RetrieveAPIView):
    authentication_classes = [SessionAuthentication]
    #permission_classes = [IsOwnerAndAuth]
    model = models.Order
    queryset = models.Order.objects.all()
    serializer_class = OrderDetailSerializer

    def get_queryset(self, *args, **kwargs):
        return models.Order.objects.all() #filter(user__user=self.request.user)


class OrderListAPIView(generics.ListAPIView):
    authentication_classes = [SessionAuthentication]
    #permission_classes = [IsOwnerAndAuth]
    model = models.Order
    queryset = models.Order.objects.all()
    serializer_class = OrderDetailSerializer

    def get_queryset(self, *args, **kwargs):
        print("Errrororo jhshdwewe")
        print(self.request)
        return models.Order.objects.all() #filter(user__user=self.request.userprofileinfo)

    def post(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
        
"""
class Login(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'accounts/login.html'

    def get(self, request):
        queryset = models.UserProfileInfo.objects.all()
        return Response({'profiles': queryset})
"""