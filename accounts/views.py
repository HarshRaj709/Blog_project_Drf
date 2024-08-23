from .serializers import Registerserializer,StudentAuthenticate1,StudentAuthenticate2
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from django.contrib.auth import authenticate,login
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework_simplejwt.authentication import JWTAuthentication


# Create your views here.
class StudentRegister(APIView):
    def post(self,request):
        try:
            data = request.data
            serializer = Registerserializer(data=data)

            if serializer.is_valid():
                serializer.save()       #this is used to save data
                response_data={'data':serializer.data,'message':'User Registerd successfully'}
                return Response(response_data,status = status.HTTP_201_CREATED)
            
            else:
                response_data={'data':serializer.errors}
                return Response(response_data,status = status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            return Response({'data':str(e)},status = status.HTTP_400_BAD_REQUEST)
        
@method_decorator(csrf_exempt,name='dispatch')
class StudentLogin(APIView):
    def post(self,request):
        data = request.data
        try:
            serializer = StudentAuthenticate1(data=data)
            if serializer.is_valid():
                username = serializer.validated_data['username']
                password = serializer.validated_data['password']
                user = authenticate(username=username,password=password)
                if user is not None:
                    login(request,user)
                    response_data = {'confirm':'Login done successfull'}
                    return Response(response_data,status = status.HTTP_200_OK)
                else:
                    response_data = {'error':'Invaid credentials'}
                    return Response(response_data,status = status.HTTP_406_NOT_ACCEPTABLE)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'data':str(e)},status = status.HTTP_400_BAD_REQUEST)

#login using Token
class Studentloginusingtoken(APIView):
    def post(self,request):
        data = request.data
        try:
            serializer = StudentAuthenticate2(data = data)
            if serializer.is_valid():
                response = serializer.get_jwt_token(serializer.data)
                return Response(response,status=status.HTTP_202_ACCEPTED)
            else:
                response_data = {'error':serializer.errors,'message':'something went wrong'}
                return Response(response_data,status = status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            return Response({'data':str(e)},status = status.HTTP_400_BAD_REQUEST)