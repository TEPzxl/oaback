from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import  LoginSerializer
from rest_framework import serializers
from .authentications import generate_jwt

# Create your views here.
class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token = generate_jwt(user)
            print('===============', token)
            return Response({'token': token})
        else:
            raise serializers.ValidationError(serializer.errors)

