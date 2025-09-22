from rest_framework import generics
from rest_framework import permissions
from .serializers import (
    RegisterationApiSerializer,
    CustomAuthTokenSerializer,
    CustomTokenObtainPairSerializer,
    ResendActivationApiSerializer,
    ChangePasswordApiSerializer,
    ResetPasswordApiSerializer,
    ResetPasswordConfirmSerializer,
)
from ...models import CustomUser
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from mail_templated import EmailMessage
from rest_framework import status
from django.conf import settings
from rest_framework.views import APIView
import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.views import TokenObtainPairView
from .permissions import IsAnonymousUser

# ________________________________________________


class RegistrationApiView(generics.GenericAPIView):
    """Registeration User by Class Api"""

    permission_classes = [IsAnonymousUser]
    serializer_class = RegisterationApiSerializer

    def post(self, request, *args, **kwargs):
        ser_data = self.get_serializer(data=request.data)
        ser_data.is_valid(raise_exception=True)
        ser_data.save()

        email = ser_data.validated_data["email"]
        user = get_object_or_404(CustomUser, email=email)
        token = get_tokens_for_user(user)
        message = EmailMessage(
            "email/email_verify.tpl",
            {"token": token},
            "admin@gmail.com",
            to=[email],
        )
        message.send()
        data = {
            "email": email,
            "message": "registeration is successfully",
            "verification_email": "link verify send to your email; checkuot",
        }
        return Response(data=data, status=status.HTTP_201_CREATED)


# ________________________________________________


class ActivationApiView(APIView):
    """Activate User by Api class"""

    def get(self, request, token):
        try:
            token_obj = jwt.decode(
                jwt=token, key=settings.SECRET_KEY, algorithms=["HS256"]
            )
            user_id = token_obj.get("user_id")
            user = get_object_or_404(CustomUser, pk=user_id)
            if not user.is_verficated:
                user.is_verficated = True
                user.save()
                return Response(
                    data={
                        "details": "User activation has been successfully completed."
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    data={"details": "The user has already been confirmed"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        except ExpiredSignatureError:
            return Response({"details": "token is Expired"})

        except ExpiredSignatureError:
            return Response({"details": "token is not valid"})


# ________________________________________________


def get_tokens_for_user(user):
    """get jwt token for user by refresh token"""
    if not user.is_active:
        raise AuthenticationFailed("User is not active")

    refresh = RefreshToken.for_user(user)
    return str(refresh.access_token)


# ________________________________________________


class CustomAuthToken(ObtainAuthToken):
    """Custom Auth token by Api class"""

    serializer_class = CustomAuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'email': user.email, 'id': user.pk})


# ________________________________________________


class CustomDicardAthToken(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return Response(
            data={"Logout: Token is Removed"}, status=status.HTTP_204_NO_CONTENT
        )


# ________________________________________________


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


# ________________________________________________


class ResendActivationApiView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = ResendActivationApiSerializer

    def post(self, request, *args, **kwargs):
        ser_data = self.get_serializer(data=request.data)
        ser_data.is_valid(raise_exception=True)

        try:
            email = ser_data.validated_data['email']
            user = get_object_or_404(CustomUser, email=email)
            if not user.is_verficated:
                token = get_tokens_for_user(user)
                message = EmailMessage(
                    'email/email_verify.tpl',
                    {'token': token},
                    'admin@gmail.com',
                    to=[user.email],
                )
                message.send()
                return Response(
                    data={'details': 'Send Activation Link for Email; checkout'},
                    status=status.HTTP_200_OK,
                )
            return Response(
                data={'details': 'This user has already been confirmed.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        except CustomUser.DoesNotExist:
            return Response(
                data={"details": "User is Not Found"}, status=status.HTTP_404_NOT_FOUND
            )


# ________________________________________________


class ChangePasswordApiView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ChangePasswordApiSerializer

    def put(self, request, *args, **kwargs):
        user = get_object_or_404(CustomUser, id=request.user.id)
        ser_data = self.get_serializer(instance=user, data=request.data)
        ser_data.is_valid(raise_exception=True)

        if user.check_password(ser_data.validated_data['old_password']):
            user.set_password(ser_data.validated_data['new_password'])
            user.save()
            return Response(
                data={'details': 'The set new password is successfuly'},
                status=status.HTTP_200_OK,
            )
        return Response(
            data={'details': 'The Current password is Invalid'},
            status=status.HTTP_400_BAD_REQUEST,
        )


# ________________________________________________


class ResetPasswordApiView(generics.GenericAPIView):
    permission_classes = [IsAnonymousUser]
    serializer_class = ResetPasswordApiSerializer

    def post(self, request, *args, **kwargs):
        ser_data = self.get_serializer(data=request.data)
        ser_data.is_valid(raise_exception=True)
        user = ser_data.validated_data['user']
        email = ser_data.validated_data['email']

        token = get_tokens_for_user(user)

        message = EmailMessage(
            'email/reset_password.tpl', {'token': token}, 'admin@gmail.com', to=[email]
        )
        message.send()

        return Response(
            data={'details': 'Reset Password Link is send email; checkout'},
            status=status.HTTP_200_OK,
        )


# ________________________________________________


class ResetPasswordConfirmApiView(generics.GenericAPIView):
    permission_classes = [IsAnonymousUser]
    serializer_class = ResetPasswordConfirmSerializer

    def post(self, request, token):
        try:
            token_obj = jwt.decode(
                jwt=token, key=settings.SECRET_KEY, algorithms=["HS256"]
            )
            user_id = token_obj.get("user_id")
            user = get_object_or_404(CustomUser, pk=user_id)
            ser_data = self.get_serializer(data=request.data)
            ser_data.is_valid(raise_exception=True)
            password = ser_data.validated_data['new_password']
            if not user.check_password(password):
                user.set_password(password)
                user.save()
                return Response(
                    data={
                        'details': 'The user password has been successfully changed.'
                    },
                    status=status.HTTP_200_OK,
                )
            return Response(
                data={'details': 'This password has been used before.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        except ExpiredSignatureError:
            return Response({"details": "This link has expired to change the password"})

        except ExpiredSignatureError:
            return Response(
                {"details": "This link is not valid for changing the password."}
            )


# ________________________________________________
