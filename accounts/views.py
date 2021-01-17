from rest_framework import viewsets, filters, generics
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
import django_filters.rest_framework
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from django.urls import reverse_lazy
from accounts import serializer, models, permissions
from django.views.generic import CreateView, ListView, DetailView
from . import forms

class dashboardView(ListView):
    model = models.Product
    template_name = "accounts/dashboard.html"

class ProductView(DetailView):
    model = models.Product
    template_name = "accounts/product.html"
    
class SignUp(CreateView):
    form_class = forms.UserCreateForm
    success_url = reverse_lazy("accounts:login")
    template_name = "accounts/signup.html"
    
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
    serializer_class = serializer.ProductSerializer
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
    serializer_class = serializer.ProductDetailSerializer


class OrderRetrieveAPIView(generics.RetrieveAPIView):
    authentication_classes = [SessionAuthentication]
    #permission_classes = [IsOwnerAndAuth]
    model = models.Order
    queryset = models.Order.objects.all()
    serializer_class = serializer.OrderDetailSerializer

    def get_queryset(self, *args, **kwargs):
        return models.Order.objects.all() #filter(user__user=self.request.user)


class OrderListAPIView(generics.ListAPIView):
    authentication_classes = [SessionAuthentication]
    #permission_classes = [IsOwnerAndAuth]
    model = models.Order
    queryset = models.Order.objects.all()
    serializer_class = serializer.OrderDetailSerializer

    def get_queryset(self, *args, **kwargs):
        print("Errrororo jhshdwewe")
        print(self.request)
        return models.Order.objects.all() #filter(user__user=self.request.userprofileinfo)

    def post(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
