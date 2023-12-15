from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status
from concurrency.api.mixins import ApiAuthMixin
from django.core.validators import MinLengthValidator
from drf_spectacular.utils import extend_schema
from rest_framework_simplejwt.tokens import RefreshToken
from .services import (
        create_user,
        generate_otp,
        confirm_phone,
        update_user,
        change_password,
    )
from .selectors import (
        get_user,
        verify_phone_otp,
        verify_password_otp,
        )
from .models import (
        BaseUser,
        UserTypes,
        VerifyType,
        )
from .validators import (
        number_validator,
        letter_validator,
        phone_number_validator,
        special_char_validator,
        )
class UserApi(ApiAuthMixin , APIView):
    class UserOutPutSerializer(serializers.ModelSerializer):
        class Meta:
            model = BaseUser
            fields = ("firstname" , "lastname" , "account_balance" , "created_at" , "updated_at")


    class UserInputSerializer(serializers.Serializer):
        firstname = serializers.CharField(max_length=50)
        lastname  = serializers.CharField(max_length=50)

    @extend_schema(request= UserInputSerializer , responses= UserOutPutSerializer)
    def put(self , request):
        serializer = self.UserInputSerializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        try:
            update_user(user= request.user,
                        firstname = serializer.validated_data.get("firstname"),
                        lastname = serializer.validated_data.get("lastname"))
            return Response(self.UserOutPutSerializer(request.user).data ,status = status.HTTP_200_OK)
        except Exception as ex:
            return Response({"error": f"{ex}"} , status= status.HTTP_400_BAD_REQUEST)


    @extend_schema(responses = UserOutPutSerializer)
    def get(self , request):
        info = self.UserOutPutSerializer(request.user).data
        return Response(info , status= status.HTTP_200_OK)

class UserRegisterApi(APIView):
    class InputRegisterSerializer(serializers.Serializer):
        # TODO: add validator for phonenumber
        phone_number = serializers.CharField(max_length=13)
        firstname = serializers.CharField(max_length=255)
        lastname = serializers.CharField(max_length=255)
        password = serializers.CharField(
            validators=[
                number_validator,
                letter_validator,
                special_char_validator,
                MinLengthValidator(limit_value=8)
            ]
        )
        confirm_password = serializers.CharField(max_length=255)
        user_type = serializers.ChoiceField(required =True,
                                            choices = UserTypes.choices())
        def validate_phone_number(self, phone_number):
            if BaseUser.objects.filter(phone_number=phone_number).exists():
                raise serializers.ValidationError("phone_number Already Taken")
            return phone_number

        def validate(self, data):
            if not data.get("password") or not data.get("confirm_password"):
                raise serializers.ValidationError("Please fill password and confirm password")

            if data.get("password") != data.get("confirm_password"):
                raise serializers.ValidationError("confirm password is not equal to password")
            return data
    class OutPutRegisterSerializer(serializers.ModelSerializer):

        token = serializers.SerializerMethodField("get_token")

        class Meta:
            model = BaseUser
            fields = ("firstname", "lastname", "phone_number", "created_at", "updated_at" , "token")

        def get_token(self, user):
            data = dict()
            token_class = RefreshToken

            refresh = token_class.for_user(user)

            data["refresh"] = str(refresh)
            data["access"] = str(refresh.access_token)

            return data

    @extend_schema(request=InputRegisterSerializer, responses=OutPutRegisterSerializer)
    def post(self, request):
        serializer = self.InputRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user = create_user(
                firstname=serializer.validated_data.get('firstname'),
                lastname=serializer.validated_data.get('lastname'),
                phone_number=serializer.validated_data.get('phone_number'),
                password=serializer.validated_data.get('password'),
                user_type=serializer.validated_data.get("user_type"),
            )
        except Exception as ex:
            return Response(
                f"Database Error {ex}",
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(self.OutPutRegisterSerializer(user, context={"request": request}).data)


class VerifyPhoneRequestApi(APIView):
    class InputPhoneOtpSerializer(serializers.Serializer):
        # TODO: add validate your phone number
        phone_number = serializers.CharField(max_length=11, required=True)

    @extend_schema(request=InputPhoneOtpSerializer)
    def post(self, request):
        serializer = self.InputPhoneOtpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user = get_user(phone_number=serializer.validated_data.get('phone_number'))
            if not user:
                return Response({"error": "user is doesn't exists"})
            otp = generate_otp(user=user, verify_type=VerifyType.PHONENUMBER)
            # TODO: send otp via sms
            return Response({f"message': 'otp sent successfuly {otp=}"}, status=status.HTTP_200_OK)
        except Exception as ex:
            return Response(f"Database error {ex}", status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordRequestApi(APIView):
    class InputPasswordOtpSerializer(serializers.Serializer):
        phone_number = serializers.CharField(max_length=11, required=True)

    @extend_schema(request=InputPasswordOtpSerializer)
    def post(self, request):
        serializer = self.InputPasswordOtpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user = get_user(phone_number=serializer.validated_data.get('phone_number'))

            otp = generate_otp(user=user, verify_type=VerifyType.PASSWORD)
            print(otp)
            return Response({f"message": f"sms sent successfully{otp=}"}, status=status.HTTP_200_OK)

        except Exception as ex:
            return Response(f"user not found {ex}", status=status.HTTP_400_BAD_REQUEST)

class VerifyPhoneApi(APIView):
    class VerifyPhoneSerializer(serializers.Serializer):
        phone_number = serializers.CharField(required= True , max_length=13)
        otp = serializers.IntegerField(required=True,)


    @extend_schema(request= VerifyPhoneSerializer)
    def post(self , request):
        serializer = self.VerifyPhoneSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        try:
            if not verify_phone_otp(
                phone_number = serializer.validated_data.get("phone_number"),
                otp = serializer.validated_data.get("otp"),
                ):
                return Response({"message": "input data is not valid"} , status = status.HTTP_400_BAD_REQUEST)
            confirm_phone(phone_number = serializer.validated_data.get("phone_number"))
            return Response({"message": "your phone_number verified successfully"} ,status=status.HTTP_200_OK)
        except Exception as ex:
            return Response({"error": f"{ex}"} , status= status.HTTP_400_BAD_REQUEST)

class ChangePasswordApi(APIView):
    class InputChangePasswordSerializer(serializers.Serializer):
        otp = serializers.IntegerField(required=True)
        new_password = serializers.CharField(
            validators=[
                number_validator,
                letter_validator,
                special_char_validator,
                MinLengthValidator(limit_value=8)
            ]
        )
        confirm_new_password = serializers.CharField(max_length=255)
        phone_number= serializers.CharField(max_length=11)
        def validate(self, data):
            if not data.get("new_password") or not data.get("confirm_new_password"):
                raise serializers.ValidationError("Please fill password and confirm password")
            if data.get("new_password") != data.get("confirm_new_password"):
                raise serializers.ValidationError("confirm password is not equal to password")
            return data

    @extend_schema(request=InputChangePasswordSerializer)
    def post(self, request):
        serializer = self.InputChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            if not verify_password_otp(phone_number=serializer.validated_data.get('phone_number'),
                                       otp=serializer.validated_data.get('otp')):
                return Response('input data is not correct', status=status.HTTP_400_BAD_REQUEST)
            user = get_user(phone_number=serializer.validated_data.get('phone_number'))
            change_password(user=user, password=serializer.validated_data.get('new_password'))
            return Response({'message': 'password changed successfully'}, status=status.HTTP_200_OK)
        except Exception as ex:
            return Response({"error": f"{ex}"} ,status= status.HTTP_400_BAD_REQUEST)
