from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import  TokenAuthentication
from rest_framework import filters
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.permissions import IsAuthenticated

from . import serializers
from . import models
from . import permissions

# Create your views here.


class HelloApiView(APIView):
    """Test Api View"""
    
    serializer_class = serializers.HelloSerializer
    

    def get(self, request,  format=None):
        """Returns a list of APIView feature"""
        a_viewset = [
            'Uses HTTP methods as function (get, post, pacth, put, delete)',
            'It is  similiar to a tradisional Django',
            'Gives you the most control over your logic',
            'Is mapped manually to URLs'
        ]
        
        return Response({'message': 'Hello', 'a_viewset': a_viewset})
    
    def post(self, request):
        """"Create a hallo message with our name"""
        
        serializer = serializers.HelloSerializer(data=request.data)
        
        if serializer.is_valid():
            name =  serializer.data.get('name')
            message = 'hello {0}'.format(name)
            return Response({'message': message})
        else:
            return Response(
                serializer.errors,  status=status.HTTP_400_BAD_REQUEST
            )
            
    def put(self, request, pk=None):
        """"Handle updating on object"""
        return Response({'method':  'put'})
    
    def patch(self, request, pk=None):
        """Patch request, only updates field provided in the request."""
        return Response({'method': 'patch'})
    
    
    def delete(self, request, pk=None):
        """Delete and object."""
        return Response({'method': 'delete'})
    
    
class  HelloViewSet(viewsets. ViewSet):
    """Test Api ViewSet"""
    
    serializer_class = serializers.HelloSerializer
    
    def list(self, request):
        """return a hellp message"""
        
        a_viewset = [
            'Uses actions (list, retriewe, update, partial_update)',
            'Automatically  map to URL using Routers',
            'Provided more functionality  with less code'
        ]
        
        return Response({'message': 'hello', 'a_viewset': a_viewset})
    
    def create(self, request):
        """Create a new hello  message"""
        
        serializer = serializers.HelloSerializer(data=request.data)
        
        if serializer.is_valid():
            name = serializer.data.get('name')
            message = 'Hello {0}'.format(name)
            return Response({'message': message})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def retriever(self, rerquest, pk=None):
        """Handle geting an object by its ID"""
        return Response ({'http_method': 'GET'})
    
    def update(self, request, pk=None):
        """Handles updating  part of an object"""
        return Response({'http_method', 'PUT'})
    
    def partial_update(self, request,  pk=None):
        """Handles updating part of an object"""
        return Response({'http_method': 'PATCh'})
    
    def  destroy(self, request, pk=None):
        """Handles removing an object"""
        return Response({'http_method': 'DELETE'})


class UserProfileViewSet(viewsets.ModelViewSet):
    """Handles crating and updating profiles."""
    
    serializer_class = serializers.UserProfileSerializer
    queryset = models.UserProfile.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateOwnProfile,)
    filter_backends = (filters.SearchFilter,)
    search_fields =  ('name', 'email',)
    
class LoginViewSet(viewsets.ViewSet,):
    """checks email and passwword and returns an auth token."""
    
    serializer_class = AuthTokenSerializer
    
    def create(self, request):
        """Use the ObthainAuthToken APIView to valide and create too token."""
        
        # return ObtainAuthToken().post(request)
        return ObtainAuthToken().as_view()(request=request._request)
    
class UserProfileFeedViewSet(viewsets.ModelViewSet):
    """Handles creating, reading anf updating profile"""
    
    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.ProfileFeedItemSerializer
    queryset = models.ProfileFeedItem.objects.all()
    permission_classes = (permissions.PostOwnStatus, IsAuthenticated)
    
    def perform_create(self, serializer):
        """Setts the user profile to  the logged in  user."""
        
        serializer.save(user_profile=self.request.user)