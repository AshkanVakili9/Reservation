from rest_framework import serializers
from ..user.models import Sms, User




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



class SmsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Sms
        fields = '__all__'
