from django.contrib.auth.models import User, Group
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):

    """
    用户信息的序列化器（根据前端需要的数据信息来组织结构）
    """
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):

    """
    组信息的序列化器
    """
    class Meta:
        model = Group
        fields = ('url', 'name')