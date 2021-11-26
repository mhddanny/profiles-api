from django.shortcuts import render
from rest_framework.serializers import Serializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from  . import  serializers

# Create your views here.


class HelloApiView(APIView):
    """Test Api View"""
    
    serializer_class = serializers.HelloSerializer
    

    def get(self, request,  format=None):
        """Returns a list of APIView feature"""
        an_apiview = [
            'Uses HTTP methods as function (get, post, pacth, put, delete)',
            'It is  similiar to a tradisional Django',
            'Gives you the most control over your logic',
            'Is mapped manually to URLs'
        ]
        
        return Response({'message': 'Hello', 'an_apiview': an_apiview})
    
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