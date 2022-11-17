from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accounts.models import CustomAccount
from apps.accounts.serializers import AccountRegistrationSerializer


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
