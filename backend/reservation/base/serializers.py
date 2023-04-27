from rest_framework import serializers
from .models import Sms, User
from rest_framework_simplejwt.tokens import RefreshToken



class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'

    def create(self,password, validated_data):
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        return user

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            if attr == 'password':
                instance.set_password(value)
            else:
                setattr(instance, attr, value)

        instance.save()
        return instance


class UserSerializerWithToken(UserSerializer): 
    token = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = User
        fields = ('id', 'full_name', 'phone', 'is_staff','token')

    def get_token(self, obj):
        token = RefreshToken.for_user(obj)
        
        return str(token.access_token)




class SmsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Sms
        fields = '__all__'
