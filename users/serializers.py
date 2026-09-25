from rest_framework import serializers
from .models import CustomUser
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate




class RegisterSerializer(serializers.ModelSerializer):
    conf_password = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'last_name', 'username','role','phone_number', 'address', 'photo', 'password', 'conf_password']
        read_only_fields = ['id']

    def create(self, validated_data):
        validated_data.pop('conf_password')
        return CustomUser.objects.create_user(**validated_data)

    def to_representation(self, instance):
        data = super().to_representation(instance)

        return data

    

class LoginSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    role = serializers.CharField(read_only=True)
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    token = serializers.CharField(read_only=True)

    def validate(self, attrs):
        user = authenticate(username=attrs['username'], password=attrs['password'])
        if not user:
            raise serializers.ValidationError("Username yoki parol noto'g'ri")
        token, created = Token.objects.get_or_create(user=user)

        attrs['token'] = token.key
        attrs['id'] = user.id
        attrs['role'] = user.role
        return attrs


class ProfileSerializer(serializers.ModelSerializer):
    role = serializers.CharField(read_only=True)
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'username','role', 'phone_number', 'address', 'photo']

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.username = validated_data.get('username', instance.username)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.address = validated_data.get('address', instance.address)
        instance.photo = validated_data.get('photo', instance.photo)

        instance.save()
        return instance




