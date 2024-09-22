from django.shortcuts import render
from rest_framework.views import APIView 
from rest_framework.response import Response 
from rest_framework import status
from.models import User


class RegisterView(APIView):
    def post(self, request):

        phone_number=request.data.get('phone_number')
        if not phone_number:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        
        try:
            user = User.objects.get(phone_number=phone_number)
            return Response({'detail': 'User already registered!'}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            user =User.objects.create_user(phone_number=phone_number)
        #     User.objects.get_or_create(phone_number=phone_number)
            
        # if not created:
        #     return Response({'detail': 'User already registered!'}, status=status.HTTP_400_BAD_REQUEST)

