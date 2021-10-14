from rest_framework import serializers
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken,TokenError
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from .models import Otheruser

class OtheruserRegisterSerializer(serializers.ModelSerializer):
    Otheruser_pass = serializers.CharField(
        max_length=68, min_length=6, write_only=True)
    # email=serializers.CharField(max_length=68,min_length=6,write_only=True)    

    default_error_messages = {
        'Otheruser_email': 'The email should  be valid'}

    class Meta:
        model = Otheruser
        fields = ['Otheruser_name','Otheruser_email','Otheruser_add','Otheruser_mobile','Type','Is_delete','Is_edit','Is_views','Otheruser_pass']

    # def validate(self, attrs):
    #     Otheruser_email = attrs.get('Otheruser_email', '')
    #     # username = attrs.get('username', '')

    #     if Otheruser_email.isalnum():
    #         raise serializers.ValidationError(
    #             self.default_error_messages)
    #     return attrs

    def create(self, validated_data):
        return Otheruser.objects.create(**validated_data)


class OtheruserEmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)

    class Meta:
        model = Otheruser
        fields = ['token']


class Otheruserloginserializer(serializers.ModelSerializer):
  
    Otheruser_email = serializers.EmailField(max_length=255, min_length=3)
    Otheruser_pass = serializers.CharField(
        max_length=68, min_length=6, write_only=True)
    # username = serializers.CharField(
        # max_length=255, min_length=3, read_only=True)
    # tokens = serializers.SerializerMethodField()

    class Meta:
        model = Otheruser
        fields = ['Otheruser_email', 'Otheruser_pass','tokens']

    def validate(self, attrs):
        Otheruser_email = attrs.get('Otheruser_email', '')
        Otheruser_pass = attrs.get('Otheruser_pass', '')

        user =Otheruser.objects.get(Otheruser_email=Otheruser_email,Otheruser_pass=Otheruser_pass)
        if not user:
            raise AuthenticationFailed('Invalid credentials, try again')
        if not user.is_active:
            raise AuthenticationFailed('Account disabled, contact admin')    
        if not user.is_verified:
            raise AuthenticationFailed('Email is not verified')

        return {
            'Otheruser_email': user.Otheruser_email,
            # 'username': user.username,
            'tokens': user.tokens
        }

        return super().validate(attrs)


class admingetotheruserdataserializer(serializers.ModelSerializer):
    class Meta:
        model = Otheruser
        fields = ['Otheruser_name', 'Otheruser_email', 'Otheruser_add',
                  'Otheruser_mobile', 'Type', 'Is_delete', 'Is_edit', 'Is_views']
                  
                  

