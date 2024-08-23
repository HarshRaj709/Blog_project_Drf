from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate,login


class Registerserializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=50,required = True, error_messages = {'required':'Please provide password'})
    username = serializers.CharField(max_length=50,required = True, error_messages = {'required':'Please provide username'})
    email = serializers.CharField(max_length=50,required = True, error_messages = {'required':'Please provide email'})

    class Meta:
        model = User
        fields = ['username','first_name','last_name','email','password']

    def validate(self,data):
        if User.objects.filter(username = data['username']).exists():
            raise serializers.ValidationError('Username already used, try with other username')
        return data
    
    def create(self,validated_data):
        user = User.objects.create(username=validated_data['username'],
                                   first_name=validated_data['first_name'],
                                   last_name=validated_data['last_name'],
                                   email = validated_data['email'])
        user.set_password(validated_data['password'])
        user.save()
        return validated_data
    

class StudentAuthenticate1(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    def validate(self,data):
        if not User.objects.filter(username = data['username']).exists():
            raise serializers.ValidationError('Invalid credential')
        return data
    

class StudentAuthenticate2(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    def validate(self,data):
        if not User.objects.filter(username = data['username']).exists():
            raise serializers.ValidationError('Invalid credential')
        return data
    
    def get_jwt_token(self,data):
        user = authenticate(username = data['username'],password=data['password'])
        if user is not None:
            refresh = RefreshToken.for_user(user)
            return {
                'message':'login Success',
                'data':{
                    'token':{
                        'refresh':str(refresh),
                        'access':str(refresh.access_token)
                    }
                }
            }
        
        else:
            return {'message':'Invalid Credentials'}