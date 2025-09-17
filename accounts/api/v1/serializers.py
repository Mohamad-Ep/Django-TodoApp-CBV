from rest_framework import serializers
from ...models import CustomUser
import re
from rest_framework.authtoken.serializers import AuthTokenSerializer
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
# ________________________________________________

class RegisterationApiSerializer(serializers.ModelSerializer):
    re_password = serializers.CharField(write_only=True)
    
    class Meta:
        model = CustomUser
        fields = ['email','password','re_password']
        
    def validate(self, attrs):
        password = attrs.get('password')
        re_password = attrs.get('re_password')
        
        if password != re_password:
            raise serializers.ValidationError('The password is not the same as the re_password')
        
        if len(password)<8:
            raise serializers.ValidationError('The password should not be less than 8 characters')
                
        if not re.findall(r'[a-z]',password):
            raise serializers.ValidationError('The password must have at least one small letter')

        if not re.findall(r'[A-Z]',password):
            raise serializers.ValidationError('The password must have at least one capital letter')
        
        if not re.findall(r'[@#$%!^&*]',password):
            raise serializers.ValidationError('Password must have at least one specific character (@#$%!^&*)')
        
        return super().validate(attrs)
    
    def create(self, validated_data):
        validated_data.pop('re_password')        
        return CustomUser.objects.create_user(**validated_data)
# ________________________________________________

class CustomAuthTokenSerializer(serializers.Serializer):
    email = serializers.CharField(
        label=_("Email"),
        write_only=True
    )
    password = serializers.CharField(
        label=_("Password"),
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )
    token = serializers.CharField(
        label=_("Token"),
        read_only=True
    )
    
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'),
                                username=email, password=password)

            # The authenticate call simply returns None for is_active=False
            # users. (Assuming the default ModelBackend authentication
            # backend.)
            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
            
            if not user.is_verficated:
                msg = _('User in not Verificated')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs
# ________________________________________________

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        data = super().validate(attrs)
        if not self.user.is_verficated:
            raise serializers.ValidationError({"details": "user is not Verficated"})
        data["email"] = self.user.email
        data["user_id"] = self.user.id
        return data

# ________________________________________________

class ResendActivationApiSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True)
# ________________________________________________

class ChangePasswordApiSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)
    re_password = serializers.CharField(write_only=True)
    
        
    def validate(self, attrs):
        password = attrs.get('new_password')
        re_password = attrs.get('re_password')
        
        if password != re_password:
            raise serializers.ValidationError('The password is not the same as the re_password')
        
        if len(password)<8:
            raise serializers.ValidationError('The password should not be less than 8 characters')
                
        if not re.findall(r'[a-z]',password):
            raise serializers.ValidationError('The password must have at least one small letter')

        if not re.findall(r'[A-Z]',password):
            raise serializers.ValidationError('The password must have at least one capital letter')
        
        if not re.findall(r'[@#$%!^&*]',password):
            raise serializers.ValidationError('Password must have at least one specific character (@#$%!^&*)')
        
        return super().validate(attrs)
    
# ________________________________________________

class ResetPasswordApiSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True)
        
    def validate(self, attrs):
        email = attrs.get('email')
        try:
            user = CustomUser.objects.get(email=email)
            attrs['user'] = user
        
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError('کاربری با این مشخصات یافت نشد')
        
        return super().validate(attrs)
# ________________________________________________

class ResetPasswordConfirmSerializer(serializers.Serializer):
    new_password = serializers.CharField(write_only=True)
    re_password = serializers.CharField(write_only=True)
            
    def validate(self, attrs):
        password = attrs.get('new_password')
        re_password = attrs.get('re_password')
        
        if password != re_password:
            raise serializers.ValidationError('The password is not the same as the re_password')
        
        if len(password)<8:
            raise serializers.ValidationError('The password should not be less than 8 characters')
                
        if not re.findall(r'[a-z]',password):
            raise serializers.ValidationError('The password must have at least one small letter')

        if not re.findall(r'[A-Z]',password):
            raise serializers.ValidationError('The password must have at least one capital letter')
        
        if not re.findall(r'[@#$%!^&*]',password):
            raise serializers.ValidationError('Password must have at least one specific character (@#$%!^&*)')
        
        return super().validate(attrs)
# ________________________________________________