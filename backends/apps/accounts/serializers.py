from django.contrib.auth import get_user_model
from rest_framework import serializers

from accounts.models import SystemSetting
from rbac.serializers import GroupSerializer, RoleSerializer

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    ammic_group = GroupSerializer()
    ammic_role = RoleSerializer(many=True)

    class Meta:
        model = User
        fields = ('id', 'last_login', 'is_superuser', 'username', 'is_staff', 'is_active', 'name', 'email', 'avatar',
                  'ammic_group', 'ammic_role')


class MyGroupUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "name", "username", "avatar")


class SystemSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = SystemSetting
        fields = "__all__"

