from django.contrib.auth import authenticate
from drf_spectacular.utils import extend_schema
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from concurrency.users.models import BaseUser, UserTypes


class InPutLoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField(required=True)
    password = serializers.CharField(required=True)


class OutPutLoginSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField("get_token")

    class Meta:
        model = BaseUser
        fields = ('token',)

    def get_token(self, user):
        data = dict()
        token_class = RefreshToken

        refresh = token_class.for_user(user)

        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)

        return data


def authenticate_user(request, user_type):
    serializer = InPutLoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    phone_number = serializer.validated_data.get('phone_number')
    password = serializer.validated_data.get('password')
    user = authenticate(request=request, phone_number=phone_number, password=password)
    if not user:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

    if not user.user_type == user_type:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    if not user.phone_verified:
        return Response({"error": "varify your phone_number first"} , status = status.HTTP_400_BAD_REQUEST)
    if user.user_type == UserTypes.SELLER and not user.verified :
        return Response({"error": "Wait until admin verify your account"}, status= status.HTTP_401_UNAUTHORIZED)

    return user


class CustomerLoginApi(APIView):

    @extend_schema(request=InPutLoginSerializer, responses=OutPutLoginSerializer)
    def post(self, request):
        try:
            user = authenticate_user(self.request, user_type=UserTypes.CUSTOMER)
            if isinstance(user , Response):
                return user
        except Exception as ex:
            return Response(
                f"Error {ex}",
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(OutPutLoginSerializer(user, context={'request': request}).data, status=status.HTTP_200_OK)


class SellerLoginApi(APIView):

    @extend_schema(request=InPutLoginSerializer, responses=OutPutLoginSerializer)
    def post(self, request):
        try:
            user = authenticate_user(self.request, user_type=UserTypes.SELLER)
            if isinstance(user , Response):
                return user
        except Exception as ex:
            return Response(
                f"Error {ex}",
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(OutPutLoginSerializer(user, context={'request': request}).data, status=status.HTTP_200_OK)


