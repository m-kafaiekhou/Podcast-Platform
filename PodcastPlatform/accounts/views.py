from django.conf import settings
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, resolve_url
from rest_framework.response import Response
from .utils import (
        cache_refresh_token,
        validate_cached_token,
        decode_token,
        delete_cache,
        get_otp, check_cache,
        gen_confirmation_link
        )
from rest_framework.exceptions import AuthenticationFailed
from .authentications import JWTAuthentication
from .serializers import (
        ChangePasswordSerializer,
        RegisterSerializer,
        LoginSerializer,
        ForgotPasswordSerializer,
        ResetPasswordSerializer
        )
from .backends import EmailOrUsernameModelBackend
from rest_framework import generics, status, permissions, views
from .producer import publish
from django.core.mail import send_mail
from .models import CustomUser
from django.core.cache import cache
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.tokens import default_token_generator



User = get_user_model()


class RegisterView(generics.CreateAPIView):
    """
        Authenticates the user using username & password
        and creates the access & refresh token for the user
        and puts user in the whitelist in our cache based database

        args:
            request => request that the user sent

        return:
            HTTPResponse => JSON(API)
    """

    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer

    def perform_create(self, serializer):
        instance = serializer.save()

        conf_view_url = resolve_url('accounts:confirm-email')
        full_url = self.request.build_absolute_uri(conf_view_url)
        conf_link = gen_confirmation_link(full_url, instance)

        send_mail(
                'email confirmation',
                f' here is your confirmation link: {conf_link}',
                settings.EMAIL_HOST_USER,
                [instance.email],
                fail_silently=False,
                )
        publish('registery', {'user': instance.id}, 'auth-notification')
        return instance




class LoginView(views.APIView):
    """
        Authenticates the user using username & password
        and creates the access & refresh token for the user
        and puts user in the whitelist in our cache based database

        args:
            request => request that the user sent

        return:
            HTTPResponse => JSON(API)
    """
    permission_classes = (permissions.AllowAny, )
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get('username')
        password = serializer.validated_data.get('password')

        backend = EmailOrUsernameModelBackend()
        user = backend.authenticate(request, username=username, password=password)

        if user is None:
            return Response({'message': _('Invalid credentials')}, status=status.HTTP_400_BAD_REQUEST)

        access_token, refresh_token = JWTAuthentication.create_jwt(user.id)

        cache_refresh_token(decode_token(refresh_token))

        data = {
            "access": access_token,
            "refresh": refresh_token,
        }

        publish('login', {'user': user.id}, 'auth-notification')

        return Response(data, status=status.HTTP_201_CREATED)


class RefreshTokenView(views.APIView):
    """
    generates new access token for the user and set it in the whitelist and header(or body)
    if the refresh token is not expired and the user is in whitelist

    args:
        request => request that the user sent

    return:
        HTTPResponse => JSON(API)
    """
    def post(self, request):
        try:
            JWTAuthentication().authenticate(request)
        except AuthenticationFailed:
            pass
        else:
            return Response(data={"message": _("user already authenticated")}, status=status.HTTP_302_FOUND)

        refresh_token = request.data.get('refresh_token')

        refresh_token = decode_token(refresh_token)

        if not validate_cached_token(refresh_token):
            return Response(data={"message": _("invalid refresh token")}, status=status.HTTP_400_BAD_REQUEST)

        user_id = refresh_token.get('user_identifier')
        old_jti = refresh_token.get('jti')

        access_token, refresh_token = JWTAuthentication.create_jwt(user_id)

        cache_refresh_token(decode_token(refresh_token))

        data = {
            "access": access_token,
            "refresh": refresh_token,
        }

        delete_cache(old_jti)

        publish('refreshtoken', {'user': user_id}, 'auth-notification')

        return Response(data, status=status.HTTP_201_CREATED)


class LogoutView(views.APIView):
    """
    Removes the user from whitelist

    args:
        request => request that the user sent

    return:
        HTTPResponse => JSON(API)
    """
    def post(self, request):
        access_token = request.data.get('access_token')
        if not access_token:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        jti = decode_token(access_token).get('jti')
        delete_cache(jti)
        return Response(status=status.HTTP_204_NO_CONTENT)


class AuthenticatedView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (JWTAuthentication, )

    def get(self, request):
        return Response(data={"message": _("you are authenticated")}, status=status.HTTP_200_OK)
    

class ForgotPasswordView(views.APIView):
    serializer_class = ForgotPasswordSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data
        print(data['email'], data)
        if CustomUser.objects.filter(email=data['email']).exists():
            otp = get_otp()
            cache.set(key=f'{data["email"]}', value=f'{otp}', timeout=120)
            send_mail(
                _('Password reset request'),
                _(f'your otp code is {otp}.'),
                settings.EMAIL_HOST_USER,
                [data['email']],
                fail_silently=False,
                )
            message = {'detail': _('Success')}
            return Response(message, status=status.HTTP_200_OK)
        
        else:
            message = {'detail': _('Error')}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordView(views.APIView):
    serializer_class = ResetPasswordSerializer

    def put(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data
        user = get_object_or_404(CustomUser, email=data['email'])

        if user.is_active:
            print(data['otp'], check_cache(data['email']))
            otp = check_cache(data['email'])
            if otp and otp == data['otp']:
                user.set_password(data['password'])
                user.save()
                return Response(_('password reset successfully. '), status=status.HTTP_201_CREATED)
            
            else:
                message = {'detail': _('OTP did not matched')}
                return Response(message, status=status.HTTP_400_BAD_REQUEST)
        else:
            message = {'detail': _('User not active')}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(views.APIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (JWTAuthentication, )

    def put(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data
        user = request.user

        if user.check_password(data['old_password']):
            user.set_password(data['password'])
            user.save()
            return Response(_('password reset successfully. '), status=status.HTTP_201_CREATED)
        
        else:
            message = {'detail': _('OTP did not matched')}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
        

class ConfirmEmail(views.APIView):
    model = CustomUser

    def get(self, request, *args, **kwargs):
        user_id = request.query_params.get('user_id', '')
        confirmation_token = request.query_params.get('conf_token', '')

        user = get_object_or_404(self.model, pk=user_id)

        if not default_token_generator.check_token(user, confirmation_token):
            return Response('Token is invalid or expired. Please request another confirmation email by signing in.', status=status.HTTP_400_BAD_REQUEST)
        user.is_active = True
        user.save()
        return Response('Email successfully confirmed', status=status.HTTP_204_NO_CONTENT)
