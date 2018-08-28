"""
View中，必然会看到model（操作数据库）和序列化器（组织response内容）
"""
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from quickstart.serializers import UserSerializer, GroupSerializer


class UserViewSet(viewsets.ModelViewSet):

    """
    处理查看、编辑用户的界面
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):

    """
    处理查看、编辑用户组的界面
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer