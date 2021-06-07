import re

from rest_framework_jwt.settings import api_settings
from django.contrib.auth import get_user_model
from rest_framework import serializers

from accounts.models import SystemSetting
from rbac.serializers import GroupSerializer, RoleSerializer

User = get_user_model()


class LoginSerializer(serializers.ModelSerializer):
    """
    自定义用户登录Serializer，允许使用邮箱或者用户名进行登录
    """
    username = serializers.CharField()

    class Meta:
        model = User
        fields = ['username', 'password']

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if re.match('^.+@.+$', username):  # 邮箱登录正则
            user = User.objects.filter(email=username).first()
        else:  # 用户名登录
            user = User.objects.filter(username=username).first()
        if user and user.check_password(password):
            # 密码验证通过，生成token
            jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
            jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

            payload = jwt_payload_handler(user)
            token = jwt_encode_handler(payload)

            #  token是要在视图类种使用,现在我们在序列化类中
            # 视图类和序列化类之间通过context这个字典来传递数据
            self.context['token'] = token
            self.context['user'] = user
            return attrs
        else:
            raise serializers.ValidationError('账号或密码错误')


class UserSerializer(serializers.ModelSerializer):
    ammic_group = GroupSerializer()
    ammic_role = RoleSerializer(many=True)

    class Meta:
        model = User
        fields = ('id', 'last_login', 'is_superuser', 'username', 'is_staff', 'is_active', 'name', 'email', 'avatar',
                  'slmsname', 'fmaildays', 'ammic_group', 'ammic_role')


class MyGroupUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "name", "username", "avatar", "email")


class SystemSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = SystemSetting
        fields = "__all__"
