from rest_framework import  serializers
from librarian.models import User, Book
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.authtoken.models import Token
from django.core.validators import validate_email
from django.conf import settings
from rest_framework.response import Response
from library.settings import SIMPLE_JWT  
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import datetime, timedelta
from rest_framework import status
# from django.contrib.auth import get_user_model

# User = get_user_model



SUPERUSER_LIFETIME = timedelta(days=15)


class Userserializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username','user_role']



class UserRegisterSerializer(serializers.ModelSerializer):           
    class Meta:
        model = User
        fields = ['password','username','user_role']
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data): 
        password = validated_data["password"]
        username = validated_data["username"]
        user_role = validated_data["user_role"]
        user = User(email='', password=password, username=username, user_role=user_role)
        user.set_password(password)
        user.save()
        return user
 




class LoginUser(TokenObtainPairSerializer):
    def validate(self, attrs):
        credentials = {
        'username': '',
        'password': attrs.get("password"),
        }
        try:
            user_obj = User.objects.filter(username=attrs.get("username")).first()

            credentials['username'] = user_obj.username
            refresh = RefreshToken.for_user(user_obj)
            res = {
                "refresh": str(refresh),
                "access": str(refresh.access_token)
            }
            if user_obj.check_password(credentials['password']):
                uobj = Userserializer(user_obj)
                return  ({'status':status.HTTP_200_OK,'message':'success','result':{'user':uobj.data,'token':res}})
            else:
                return ({'status':status.HTTP_400_BAD_REQUEST,'message':'Invalid Credentials','error':{'password':'Incorrect password'}})
        except:
            return  ({'status':status.HTTP_400_BAD_REQUEST,'message':'Invalid Credentials','error':{'username':"Username does not exist."}})




class TokenRefreshSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    access = serializers.ReadOnlyField()

    def validate(self, attrs):
        try:
            refresh = RefreshToken(attrs['refresh'])
            data = {'access': str(refresh.access_token)}
            refresh.set_jti()
            refresh.set_exp(lifetime=SUPERUSER_LIFETIME)
            data['refresh'] = str(refresh)
            return  ({'status':status.HTTP_200_OK,'message':'Success!','result':data})
        except:
            return ({"status":status.HTTP_401_UNAUTHORIZED,"result":{"errors":"Refresh token is expired"}})



class MemberRegisterSerializer(serializers.ModelSerializer):           
    class Meta:
        model = User
        fields = ['password','username']
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data): 
        password = validated_data["password"]
        username = validated_data["username"]
        user = User(password=password, username=username, user_role='MEMBER')
        user.set_password(password)
        user.save()
        return user


    def validate_username(self, value):
        gg = '''~!@#$%^&*()_+|?><,./';'''
        if value == "":
            raise serializers.ValidationError({'username': 'Please enter your username.'})
        if User.objects.filter(username=value).exclude(id = self.context['id']):
            raise serializers.ValidationError({'username':'Username already taken.'})
        return value



class MemberUpdateSerializer(serializers.ModelSerializer):           
    class Meta:
        model = User
        fields = ['id','password','username']
        extra_kwargs = {"password": {"write_only": True}}

    

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['name', 'status']


class BookdetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'name', 'status']


        


