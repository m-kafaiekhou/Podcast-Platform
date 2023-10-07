from django.contrib.auth import get_user_model
from rest_framework.response import Response
from .utils import cache_refresh_token, validate_cached_token, decode_token, delete_cache
from rest_framework.exceptions import AuthenticationFailed
from .authentications import JWTAuthentication
from .serializers import RegisterSerializer, LoginSerializer
from .backends import EmailOrUsernameModelBackend
from rest_framework import generics, status, permissions, views
from .producer import publish


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
        publish('registery', {'user': instance.id})
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
            return Response({'message': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

        access_token, refresh_token = JWTAuthentication.create_jwt(user.id)

        cache_refresh_token(decode_token(refresh_token))

        data = {
            "access": access_token,
            "refresh": refresh_token,
        }

        publish('login', {'user': user.id}) # rabbit

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

        refresh_token = decode_token(refresh_token)

        if not validate_cached_token(refresh_token):
            return Response(data={"message": "invalid refresh token"}, status=status.HTTP_400_BAD_REQUEST)

        user_id = refresh_token.get('user_identifier')

        access_token, refresh_token = JWTAuthentication.create_jwt(user_id)

        cache_refresh_token(decode_token(refresh_token))

        data = {
            "access": access_token,
            "refresh": refresh_token,
        }

        publish('login', {'user': user_id})

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
        return Response(data={"message": "you are authenticated"}, status=status.HTTP_200_OK)