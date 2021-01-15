from rest_framework import status
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework import filters
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import TemplateHTMLRenderer

from django.shortcuts import render
from accounts import serializer, models, permissions




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

class Login(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'accounts/login.html'

    def get(self, request):
        queryset = models.UserProfileInfo.objects.all()
        return Response({'profiles': queryset})