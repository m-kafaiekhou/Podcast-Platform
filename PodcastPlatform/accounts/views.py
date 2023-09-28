from django.contrib.auth.models import User
from rest_framework.response import Response
from .utils import cache_refresh_token, validate_cached_token
from rest_framework.exceptions import AuthenticationFailed
from .authentications import JWTAuthentication
from .serializers import RegisterSerializer, LoginSerializer
from .backends import EmailOrUsernameModelBackend
from rest_framework import generics, status, permissions, views


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
            return Response({'message': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

        access_token, refresh_token = JWTAuthentication.create_jwt(user)

        cache_refresh_token(refresh_token)

        data = {
            "access": access_token,
            "refresh": refresh_token,
        }

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
            return Response(data={"message": "user already authenticated"}, status=status.HTTP_302_FOUND)

        refresh_token = request.data.get('refresh_token')

        if not validate_cached_token(refresh_token):
            return Response(data={"message": "invalid refresh token"}, status=status.HTTP_400_BAD_REQUEST)

        user_id = refresh_token.get('user_identifier')

        access_token, refresh_token = JWTAuthentication.create_jwt(user_id)

        cache_refresh_token(refresh_token)

        data = {
            "access": access_token,
            "refresh": refresh_token,
        }

        return Response(data, status=status.HTTP_201_CREATED)


def logout(request):
    """
    Removes the user from whitelist

    args:
        request => request that the user sent

    return:
        HTTPResponse => JSON(API)
    """
