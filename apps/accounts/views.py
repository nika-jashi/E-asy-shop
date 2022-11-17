from django.core.cache import cache
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from drf_spectacular.utils import extend_schema

from apps.accounts.models import CustomAccount
from apps.accounts.serializers import (AccountRegistrationSerializer,
                                       AccountChangePasswordSerializer,
                                       PasswordResetRequestEmailSerializer, PasswordResetConfirmSerializer,
                                       OTPValidationSerializer)
from apps.utils.email_sender import SendEmail
from apps.utils.otp_generator import OTP_generator


@extend_schema(tags=["Auth"])
class AccountRegistrationView(APIView):
    """
     A view for creating new users. with POST request method and proper status codes
    """
    serializer_class = AccountRegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = request.data.get("email")
        user = CustomAccount.objects.filter(email=email).first()
        if user:
            return Response({"message": "User with this credentials already exists."},
                            status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@extend_schema(tags=["Auth"])
class AccountLoginView(TokenObtainPairView):
    """View for user to log in using JWT bearer Token"""
    serializer_class = TokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        user = CustomAccount.objects.filter(email=email).first()
        if not user:
            return Response(
                {"detail": "No active account found with the given credentials"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.validated_data, status=status.HTTP_200_OK)


@extend_schema(tags=["password_change"])
class AccountChangePasswordView(APIView):
    serializer_class = AccountChangePasswordSerializer
    model = CustomAccount
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        obj = self.request.user
        return obj

    def post(self, request):
        user = request.user
        serializer = self.serializer_class(instance=user, data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({"detail": "You successfully changed your password."}, status=status.HTTP_200_OK)


@extend_schema(tags=["password_reset"])
class PasswordResetRequestEmailView(APIView):
    serializer_class = PasswordResetRequestEmailSerializer

    def post(self, request):
        data = request.data
        otp = OTP_generator()

        cache.set(otp, data.get('email'))

        serializer = PasswordResetRequestEmailSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        SendEmail.send_email(subject="Es-Shop Password Reset for your account",
                             body=f"Your Password Reset Code Is: {otp} (Code is valid for 10 minutes)",
                             to=[serializer.data.get("email")])

        return Response({"detail": "We Have Sent You Message To your email"}, status=status.HTTP_200_OK)


@extend_schema(tags=["password_reset"])
class PasswordResetVerifyEmailView(APIView):
    serializer_class = OTPValidationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get("email")
        user = CustomAccount.objects.get_queryset().filter(email=email).first()

        if not user:
            return Response({"detail": "User does not exist."}, status=status.HTTP_400_BAD_REQUEST)

        refresh = RefreshToken.for_user(user=user)
        data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
        return Response(data, status=status.HTTP_200_OK)


@extend_schema(tags=["password_reset"])
class PasswordResetConfirmView(APIView):
    serializer_class = PasswordResetConfirmSerializer
    queryset = CustomAccount.objects.get_queryset().all()
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        user = request.user
        serializer = PasswordResetConfirmSerializer(instance=user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({"detail": "You successfully changed your password!"}, status=status.HTTP_200_OK)
