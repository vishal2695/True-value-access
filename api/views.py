from pickle import TRUE
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import decorators, permissions,  status
from rest_framework.views import APIView
from .serializers import *
from librarian.models import Borrowbook, User
from cherrypicker import CherryPicker
import jwt

# from django.contrib.auth import get_user_model
# Create your views here.

# User = get_user_model


def token(b):
    k = b.index(" ")
    k = b[k+1:]  # remove berar
    return k
    

def errors(b):
    picker = CherryPicker(b).flatten().get()
    error = {}
    for i, j in picker.items():
        td = i.count("_")
        if td > 1:
            b = i.index("_")
            c = i.index("_", b+1)
            error[i[:c]] = j
        else:
            b = i.index("_")
            error[i[:b]] = j
    return error


@decorators.api_view(["POST"])
@decorators.permission_classes([permissions.AllowAny])
def signup(request):
    register_user = UserRegisterSerializer(data=request.data)
    if register_user.is_valid():
        register_user.save()
    return Response({'message': 'Success', 'result': register_user.data}, status=status.HTTP_200_OK)



@decorators.api_view(["GET"])
@decorators.permission_classes([permissions.AllowAny])
def memberlist(request):
    kl = request.META['HTTP_AUTHORIZATION']  # token
    user = token(kl)  # id
    try:
        decoded = jwt.decode(user, settings.SECRET_KEY, ['HS256'])
        gk = decoded['user_id']
    except:
        return Response({"result": {"errors": "Unauthenticated"}}, status=status.HTTP_401_UNAUTHORIZED)
    if User.objects.filter(id=gk, user_role="LIBRARIAN"):
        user_objs = User.objects.filter(user_role='MEMBER')  
        register_user = Userserializer(user_objs, many=True)
        return Response({'message': 'Success', 'result': register_user.data}, status=status.HTTP_200_OK)
    return Response({"message": "data invalid"}, status=status.HTTP_400_BAD_REQUEST)


@decorators.api_view(["POST"])
@decorators.permission_classes([permissions.AllowAny])
def addmember(request):
    kl = request.META['HTTP_AUTHORIZATION']  # token
    user = token(kl)  # id
    try:
        decoded = jwt.decode(user, settings.SECRET_KEY, ['HS256'])
        gk = decoded['user_id']
    except:
        return Response({"result": {"errors": "Unauthenticated"}}, status=status.HTTP_401_UNAUTHORIZED)
    if User.objects.filter(id=gk, user_role="LIBRARIAN"):
        serializer = MemberRegisterSerializer(data=request.data)
        if serializer.is_valid():
            obj = serializer.save()
            instance = Userserializer(obj)
            return Response({'message': 'Success', 'result': instance.data}, status=status.HTTP_200_OK)
        error_list = errors(serializer.errors)
        return Response({"message": "data invalid", "result": {"errors": error_list}}, status=status.HTTP_400_BAD_REQUEST)
    return Response({"message": "data invalid"}, status=status.HTTP_400_BAD_REQUEST)


@decorators.api_view(["PATCH"])
@decorators.permission_classes([permissions.AllowAny])
def updatemember(request):
    kl = request.META['HTTP_AUTHORIZATION']  # token
    user = token(kl)  # id
    try:
        decoded = jwt.decode(user, settings.SECRET_KEY, ['HS256'])
        gk = decoded['user_id']
    except:
        return Response({"result": {"errors": "Unauthenticated"}}, status=status.HTTP_401_UNAUTHORIZED)
    if User.objects.filter(id=gk, user_role="LIBRARIAN"):
        obj = User.objects.get(id=request.data['uid'])
        serializer = MemberRegisterSerializer(obj, data=request.data, partial=True)
        serializer.context['id'] = obj.id
        if serializer.is_valid():   
            obj = serializer.save()
            password = request.data['password']
            obj.set_password(password)
            obj.save()
            instance = Userserializer(obj)
            return Response({'message': 'Success', 'result': instance.data}, status=status.HTTP_200_OK)
        error_list = errors(serializer.errors)
        return Response({"message": "data invalid", "result": {"errors": error_list}}, status=status.HTTP_400_BAD_REQUEST)
    return Response({"message": "Invalid Request"}, status=status.HTTP_400_BAD_REQUEST)



@decorators.api_view(["GET"])
@decorators.permission_classes([permissions.AllowAny])
def memberdetail(request):
    kl = request.META['HTTP_AUTHORIZATION']  # token
    user = token(kl)  # id
    try:
        decoded = jwt.decode(user, settings.SECRET_KEY, ['HS256'])
        gk = decoded['user_id']
    except:
        return Response({"result": {"errors": "Unauthenticated"}}, status=status.HTTP_401_UNAUTHORIZED)
    id = request.query_params['id']
    user_objs = User.objects.get(id=id)  
    if user_objs.user_role == 'MEMBER':
        register_user = Userserializer(user_objs)
        return Response({'message': 'Success', 'result': register_user.data}, status=status.HTTP_200_OK)
    return Response({"message": "Invalid Request"}, status=status.HTTP_400_BAD_REQUEST)



@decorators.api_view(["DELETE"])
@decorators.permission_classes([permissions.AllowAny])
def removemember(request):
    kl = request.META['HTTP_AUTHORIZATION']  # token
    user = token(kl)  # id
    try:
        decoded = jwt.decode(user, settings.SECRET_KEY, ['HS256'])
        gk = decoded['user_id']
    except:
        return Response({"result": {"errors": "Unauthenticated"}}, status=status.HTTP_401_UNAUTHORIZED)
    id = request.query_params['id']
    try:
        user_objs = User.objects.get(id=id)  
        if user_objs.user_role == 'MEMBER':
            user_objs.delete()
            return Response({'message': 'Success', 'result': {'data':'Remove Successfully'}}, status=status.HTTP_200_OK)
    except:
        return Response({"message": "Invalid Data Request"}, status=status.HTTP_400_BAD_REQUEST)



@decorators.api_view(["POST"])
@decorators.permission_classes([permissions.AllowAny])
def addbook(request):
    kl = request.META['HTTP_AUTHORIZATION']  # token
    user = token(kl)  # id
    try:
        decoded = jwt.decode(user, settings.SECRET_KEY, ['HS256'])
        gk = decoded['user_id']
    except:
        return Response({"result": {"errors": "Unauthenticated"}}, status=status.HTTP_401_UNAUTHORIZED)
    serializer = BookSerializer(data=request.data)
    if serializer.is_valid():
        obj = serializer.save()
        instance = BookdetailSerializer(obj)
        return Response({'message': 'Success', 'result': instance.data}, status=status.HTTP_200_OK)
    error_list = errors(serializer.errors)
    return Response({"message": "data invalid", "result": {"errors": error_list}}, status=status.HTTP_400_BAD_REQUEST)



@decorators.api_view(["PATCH"])
@decorators.permission_classes([permissions.AllowAny])
def updatebook(request):
    kl = request.META['HTTP_AUTHORIZATION']  # token
    user = token(kl)  # id
    try:
        decoded = jwt.decode(user, settings.SECRET_KEY, ['HS256'])
        gk = decoded['user_id']
    except:
        return Response({"result": {"errors": "Unauthenticated"}}, status=status.HTTP_401_UNAUTHORIZED)
    if User.objects.filter(id=gk, user_role="LIBRARIAN"):
        obj = Book.objects.get(id=request.data['book_id'])
        serializer = BookdetailSerializer(obj, data=request.data, partial=True)
        if serializer.is_valid():   
            obj = serializer.save()
            instance = BookdetailSerializer(obj)
            return Response({'message': 'Success', 'result': instance.data}, status=status.HTTP_200_OK)
        error_list = errors(serializer.errors)
        return Response({"message": "data invalid", "result": {"errors": error_list}}, status=status.HTTP_400_BAD_REQUEST)
    return Response({"message": "Invalid Request"}, status=status.HTTP_400_BAD_REQUEST)



@decorators.api_view(["DELETE"])
@decorators.permission_classes([permissions.AllowAny])
def removebook(request):
    kl = request.META['HTTP_AUTHORIZATION']  # token
    user = token(kl)  # id
    try:
        decoded = jwt.decode(user, settings.SECRET_KEY, ['HS256'])
        gk = decoded['user_id']
    except:
        return Response({"result": {"errors": "Unauthenticated"}}, status=status.HTTP_401_UNAUTHORIZED)
    if User.objects.get(id=gk, user_role='LIBRARIAN'):
        id = request.query_params['book_id']
        book_objs = Book.objects.get(id=id)  
        book_objs.delete()
        return Response({'message': 'Success', 'result': 'Remove Successfully'}, status=status.HTTP_200_OK)
    return Response({"message": "Invalid Request"}, status=status.HTTP_400_BAD_REQUEST)





# for member






@decorators.api_view(["GET"])
@decorators.permission_classes([permissions.AllowAny])
def booklistformember(request):
    kl = request.META['HTTP_AUTHORIZATION']  # token
    user = token(kl)  # id
    try:
        decoded = jwt.decode(user, settings.SECRET_KEY, ['HS256'])
        gk = decoded['user_id']
    except:
        return Response({"result": {"errors": "Unauthenticated"}}, status=status.HTTP_401_UNAUTHORIZED)
    obj = User.objects.get(id=gk)
    if obj.user_role == 'MEMBER':
        book_objs = Book.objects.all()
        serializer = BookdetailSerializer(book_objs, many=True)
        return Response({'message': 'Success', 'result': serializer.data}, status=status.HTTP_200_OK)
    return Response({"message": "Invalid Request"}, status=status.HTTP_400_BAD_REQUEST)



@decorators.api_view(["POST"])
@decorators.permission_classes([permissions.AllowAny])
def borrowbook(request):
    kl = request.META['HTTP_AUTHORIZATION']  # token
    user = token(kl)  # id
    try:
        decoded = jwt.decode(user, settings.SECRET_KEY, ['HS256'])
        gk = decoded['user_id']
    except:
        return Response({"result": {"errors": "Unauthenticated"}}, status=status.HTTP_401_UNAUTHORIZED)
    uobj = User.objects.get(id=gk)
    if uobj.user_role=="MEMBER":
        obj = Book.objects.get(id=request.data['book_id'])
        if obj.status == 'AVAILABLE':   
            obj.status = 'BORROWED'
            obj.save()
            userbooked = Borrowbook()
            userbooked.user_id = User.objects.get(id=gk)
            userbooked.book_id = obj
            userbooked.status = 'BORROWED'
            userbooked.save()
            return Response({'message': 'Success', 'result': {'status':'Borrowed Successfully', 'username':uobj.username, 'book_name':obj.name, 'book_status':obj.status}}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Success', 'result': {'status':'Book Not Available'}}, status=status.HTTP_400_BAD_REQUEST)
    return Response({"message": "Invalid Request"}, status=status.HTTP_400_BAD_REQUEST)




@decorators.api_view(["POST"])
@decorators.permission_classes([permissions.AllowAny])
def returnbook(request):
    kl = request.META['HTTP_AUTHORIZATION']  # token
    user = token(kl)  # id
    try:
        decoded = jwt.decode(user, settings.SECRET_KEY, ['HS256'])
        gk = decoded['user_id']
    except:
        return Response({"result": {"errors": "Unauthenticated"}}, status=status.HTTP_401_UNAUTHORIZED)
    uobj = User.objects.get(id=gk)
    if uobj.user_role=="MEMBER":
        obj = Borrowbook.objects.get(id=request.data['borrow_id'])
        if obj.status == 'BORROWED':   
            obj.status = 'RETURNED'
            obj.book_id.status = 'AVAILABLE'
            obj.save()
            return Response({'message': 'Success', 'result': {'status':'Return Successfully', 'username':uobj.username, 'book_name':obj.book_id.name, 'book_status':obj.book_id.status}}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Success', 'result': {'status':'Book Not Available'}}, status=status.HTTP_400_BAD_REQUEST)
    return Response({"message": "Invalid Request"}, status=status.HTTP_400_BAD_REQUEST)




@decorators.api_view(["DELETE"])
@decorators.permission_classes([permissions.AllowAny])
def removeaccount(request):
    kl = request.META['HTTP_AUTHORIZATION']  # token
    user = token(kl)  # id
    try:
        decoded = jwt.decode(user, settings.SECRET_KEY, ['HS256'])
        gk = decoded['user_id']
    except:
        return Response({"result": {"errors": "Unauthenticated"}}, status=status.HTTP_401_UNAUTHORIZED)
    uobj = User.objects.get(id=gk)
    if uobj.user_role=="MEMBER":
        uobj.delete()
        return Response({'message': 'Success', 'result': {'status':'Remove Account Successfully'}}, status=status.HTTP_200_OK)
    return Response({"message": "Invalid Request"}, status=status.HTTP_400_BAD_REQUEST)







