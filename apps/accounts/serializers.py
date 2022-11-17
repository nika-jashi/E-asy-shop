from rest_framework import serializers
from django.utils.translation import gettext_lazy as _

from apps.accounts.models import CustomAccount


class AccountRegistrationSerializer(serializers.ModelSerializer):
    """A serializer for creating new users. Includes all the required
       fields and validations, plus a repeated password. """

    password = serializers.CharField(max_length=255, write_only=True)
    confirm_password = serializers.CharField(max_length=255, write_only=True)
    email = serializers.EmailField()

    class Meta:
        model = CustomAccount
        fields = ['email', 'first_name', 'last_name', 'password', 'confirm_password']

    def validate(self, data):
        if data.get('password') != data.get('confirm_password'):
            raise serializers.ValidationError({"confirm_password": _("Those Passwords Don't Match.")})

        del data['confirm_password']  # deleting confirm_password because we don't use it after validation

        return data

    def create(self, validated_data):
        instance = CustomAccount.objects.create_user(**validated_data)
        return instance
