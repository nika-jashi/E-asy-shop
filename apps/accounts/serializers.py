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


class AccountChangePasswordSerializer(serializers.Serializer):  # noqa
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True)
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
    email = serializers.EmailField(required=True)

    def validate(self, data):
        data = super().validate(data)
        if not CustomAccount.objects.get_queryset().filter(email=data.get('email')):
            raise serializers.ValidationError({'detail': _('user with this email is not registered')})
        return data
