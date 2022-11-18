from django.core.cache import cache
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinLengthValidator

from apps.accounts.models import CustomAccount

from apps.utils.custom_validators import (not_contains_symbols,
                                          not_contains_whitespace,
                                          contains_uppercase,
                                          contains_digits,
                                          contains_lowercase)


class AccountRegistrationSerializer(serializers.ModelSerializer):
    """A serializer for creating new users. Includes all the required
       fields and validations, plus a repeated password. """

    password = serializers.CharField(max_length=255, write_only=True, validators=[not_contains_whitespace,
                                                                                  contains_uppercase,
                                                                                  contains_digits,
                                                                                  contains_lowercase,
                                                                                  MinLengthValidator(8)])
    confirm_password = serializers.CharField(max_length=255, write_only=True)
    email = serializers.EmailField()
    first_name = serializers.CharField(max_length=56, validators=[not_contains_symbols])
    last_name = serializers.CharField(max_length=56, validators=[not_contains_symbols])

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


class AccountChangePasswordSerializer(serializers.Serializer):  # noqa
    """A serializer for user to change password when authenticated. Includes all the required
       fields and validations, plus a repeated password. """
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True, validators=[not_contains_whitespace,
                                                                                     contains_uppercase,
                                                                                     contains_digits,
                                                                                     contains_lowercase,
                                                                                     MinLengthValidator(8)])
    confirm_password = serializers.CharField(required=True, write_only=True)

    def validate(self, data):
        user = self.context.get('request').user
        if not user.check_password(data.get("old_password")):
            raise serializers.ValidationError({"old_password": "Old password is not correct"})

        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError({"new_password": "Password fields didn't match."})

        return data

    def update(self, instance, validated_data):
        instance.set_password(validated_data['new_password'])
        instance.save()

        return instance


class PasswordResetRequestEmailSerializer(serializers.Serializer):  # noqa
    """A serializer for user to request password reset when is not authenticated.
     Includes email field for sending otp and all required validations. """
    email = serializers.EmailField(required=True)

    def validate(self, data):
        data = super().validate(data)
        if not CustomAccount.objects.get_queryset().filter(email=data.get('email')):
            raise serializers.ValidationError({'detail': _('user with this email is not registered')})
        return data


class OTPValidationSerializer(serializers.Serializer):  # noqa
    """A serializer for user to verify sent otp includes all required verifications. """
    OTP = serializers.CharField(write_only=True,
                                required=True,
                                help_text="Please input your otp code")
    email = serializers.CharField(read_only=True)

    def validate(self, data):
        data = super().validate(data)
        email = cache.get(data.get('OTP'))
        if not email:
            raise serializers.ValidationError({'detail': _('otp is wrong or expired')})

        data["email"] = email
        return data


class PasswordResetConfirmSerializer(serializers.Serializer):  # noqa
    """A serializer for user to confirm new password and obtain full access of account
     includes all password, plus a repeated password. """
    new_password = serializers.CharField(required=True, write_only=True, validators=[not_contains_whitespace,
                                                                                     contains_uppercase,
                                                                                     contains_digits,
                                                                                     contains_lowercase,
                                                                                     MinLengthValidator(8)])
    new_password_confirm = serializers.CharField(required=True, write_only=True)

    def validate(self, data):
        data = super().validate(data)
        new_password = data.get("new_password")
        new_password_confirm = data.get("new_password_confirm")

        if new_password != new_password_confirm:
            raise serializers.ValidationError({"new_password_confirm": _("Passwords are not matched.")})

        return data

    def update(self, instance, validated_data):
        instance.set_password(validated_data.get('new_password'))
        instance.save()
        return instance
