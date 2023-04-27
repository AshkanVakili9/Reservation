from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from reservation.base.models import User, Sms
from reservation.base.serializers import UserSerializer, UserSerializerWithToken, SmsSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.auth.hashers import make_password
from rest_framework import status
import random
import requests
import json
# Create your views here.

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView




class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        serializer = UserSerializerWithToken(self.user).data

        for k, v in serializer.items():
            data[k] = v

        return data


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer



@api_view(['POST'])
def registerUser(request):
    data = request.data
     
    user = User.objects.create(
        full_name=data['full_name'],
        phone=data['phone'],
        password=make_password(data['password'])
    )
    serializer = UserSerializerWithToken(user, many=False)
    
    # unique_id = str(random.randint(10000, 99999))
    # url = 'https://api.sms.ir/v1/send/verify'
    # headers = {
    #     'X-API-KEY': 'xLaqtCB7xkF6N4HB3OBSHbfPxZlMd8VXbpSOAuv3vFU5EPaTZcPqVMLhZw0lIvEW',
    #     'ACCEPT': 'application/json',
    #     'Content-Type': 'application/json'}
    # sms_data = {"mobile": request.data["phone"], "templateId": 245789,
    #             "parameters": [{"name": "CODE", "value": unique_id}]}
    # requset_sms = requests.post(
    #     url=url, headers=headers, data=json.dumps(sms_data), params=request.POST)
    # sms_data = {"phone": data["phone"], "sms": unique_id}
    # sms_data_ser = SmsSerializer(data=sms_data)
    # if sms_data_ser.is_valid():
    #     sms_data_ser.save()
    
    return Response({'detail':'User created and Sms sent.', 'payload':serializer.data}, status=status.HTTP_201_CREATED)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def sendSms(request):
    user = request.user
    unique_id = str(random.randint(10000, 99999))
    url = 'https://api.sms.ir/v1/send/verify'
    headers = {
        'X-API-KEY': 'xLaqtCB7xkF6N4HB3OBSHbfPxZlMd8VXbpSOAuv3vFU5EPaTZcPqVMLhZw0lIvEW',
        'ACCEPT': 'application/json',
        'Content-Type': 'application/json'
    }
    sms_data = {
        "mobile": user.phone, "templateId": 245789,
        "parameters": [
            {
                "name": "CODE",
                "value": unique_id
            }
        ]
    }
    requset_sms = requests.post(
        url=url, headers=headers, data=json.dumps(sms_data), params=request.POST)
    sms_data = {"phone": user.phone, "sms": unique_id}
    sms_data_ser = SmsSerializer(data=sms_data)
    if sms_data_ser.is_valid():
        sms_data_ser.save()
        return Response("Sms has been Sent", status=status.HTTP_201_CREATED)
    return Response("Sms has been NoT Sent", status=status.HTTP_201_CREATED)



        
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def verifyCode(request):
    user = request.user
    code = request.data['code']
    user_sms = Sms.objects.filter(phone=user.phone).latest('sentDate')
    if user_sms is not None:
        if user_sms.sms == code:
            user.is_verifed = True
            user.save()
            return Response("sms is true", status=status.HTTP_200_OK)
        return Response("sms is Not true", status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response("phone Number in Not true", status=status.HTTP_404_NOT_FOUND)



@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateUserProfile(request):
    user = request.user
    serializer = UserSerializerWithToken(user, many=False)
    
    data = request.data
    
    user.full_name = data['full_name']
    
    if data['password'] != '':
        user.password = make_password(data['password'])
        
    user.save()
    return Response(serializer.data)




@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUserProfile(request):
    user = request.user
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def getUsers(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)



@api_view(['GET'])
@permission_classes([IsAdminUser])
def getUserById(request, pk):
    user = User.objects.get(id=pk)
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAdminUser])
def updateUser(request, pk):
    user = User.objects.get(id=pk)
    
    data = request.data
    
    user.full_name = data['full_name']
    user.phone = data['phone']
    
    if data['is_staff'] != '':
        user.is_staff = data['is_staff']
    
    user.save()
    
    serializer = UserSerializer(user, many=False)
    
    return Response(serializer.data)



@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def deleteUser(request, pk):
    try:
        userForDeletion = User.objects.get(id=pk)
        if userForDeletion:
            userForDeletion.delete()
            return Response('User deleted successfully', status=status.HTTP_200_OK)
    except Exception:
        return Response('User not found.', status=status.HTTP_404_NOT_FOUND)
