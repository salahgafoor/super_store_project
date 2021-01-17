from rest_framework import viewsets, filters, generics
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
import django_filters.rest_framework
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from django.urls import reverse_lazy
from accounts import serializer, models, permissions
from django.views.generic import CreateView, ListView, DetailView, View
from . import forms
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404,redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from . models import *

class dashboardView(ListView):
    model = Product
    template_name = "accounts/dashboard.html"

class ProductView(DetailView):
    model = Product
    template_name = "accounts/product.html"
    
class SignUp(CreateView):
    form_class = forms.UserCreateForm
    success_url = reverse_lazy("accounts:login")
    template_name = "accounts/signup.html"
    
class UserProfileViewSet(viewsets.ModelViewSet):
    """Handle creating and updating profiles"""
    serializer_class = serializer.UserProfileSerializer
    queryset = UserProfileInfo.objects.all()
    
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
    queryset = Product.objects.all()
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
    queryset = Product.objects.all()
    serializer_class = serializer.ProductDetailSerializer


class OrderRetrieveAPIView(generics.RetrieveAPIView):
    authentication_classes = [SessionAuthentication]
    #permission_classes = [IsOwnerAndAuth]
    model = Order
    queryset = Order.objects.all()
    serializer_class = serializer.OrderDetailSerializer

    def get_queryset(self, *args, **kwargs):
        return Order.objects.all() #filter(user__user=self.request.user)


class OrderListAPIView(generics.ListAPIView):
    authentication_classes = [SessionAuthentication]
    #permission_classes = [IsOwnerAndAuth]
    model = Order
    queryset = Order.objects.all()
    serializer_class = serializer.OrderDetailSerializer

    def get_queryset(self, *args, **kwargs):
        print("Errrororo jhshdwewe")
        print(self.request)
        return Order.objects.all() #filter(user__user=self.request.userprofileinfo)

    def post(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


# Cart Views
@login_required
def add_to_cart(request, pk):
    """ 
    adding products from product.html to cart (Flow: models.py->urls.py->views.py(this function))
    """
    product = get_object_or_404(Product, pk=pk )
    order_item, created = OrderItem.objects.get_or_create(
        product = product,
        user = request.user,
        ordered = False
    )
    order_qs = Order.objects.filter(userprofileinfo=request.user, ordered=False)

    if order_qs.exists():
        order = order_qs[0]
        order.products.add(order_item)
        return redirect("accounts:cart-items")
    else: 
        order = Order.objects.create(user=request.user)
        order.products.add(order_item)
        return redirect("accounts:cart-items")
    
class CartItemsView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):

        try:
            order = Order.objects.get(userprofileinfo=self.request.user, ordered=False)
            context = {
                'object': order
            }
            print(order)
            return render(self.request, 'accounts/cart_items.html', context)
        except ObjectDoesNotExist:
            print("You do not have an order")
            return redirect("/")