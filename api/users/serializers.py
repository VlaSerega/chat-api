from djoser.serializers import UserCreatePasswordRetypeSerializer
from rest_framework import serializers

from api.models import User


class UserMeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'name', 'last_name', 'date_joined',)


class UserSmallSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'name', 'last_name')


class UserCreatePasswordSimpleRetypeSerializer(UserCreatePasswordRetypeSerializer):
    def validate(self, attrs):
        self.fields.pop("re_password", None)
        re_password = attrs.pop("re_password")
        if attrs["password"] == re_password:
            return attrs
        else:
            self.fail("password_mismatch")
