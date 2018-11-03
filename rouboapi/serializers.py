from rest_framework import serializers
from rouboapi.models import DeviceReport
from rouboapi.models import Respage01Info
from rouboapi.models import Respage01Gone
from rouboapi.models import Respage01New
from rouboapi.models import Respage01Union

from rouboapi.models import Respage02Info
from rouboapi.models import ProductHuntDayTop
from rouboapi.models import ProductHuntMonthTop


class DeviceReportSerializer(serializers.HyperlinkedModelSerializer):
    """
    序列化上报接口数据
    """

    class Meta:
        model = DeviceReport
        fields = ('report_type', 'report_time', 'device_id', 'ip_address')


class Respage01Serializer(serializers.HyperlinkedModelSerializer):
    """
    序列化Respage01相关的数据
    """

    class Meta:
        model = Respage01Info
        fields = ('time', 'lat', 'lng', 'name', 'address', 'detail_url', 'rate')


class Respage01GoneSerializer(serializers.HyperlinkedModelSerializer):
    """
    序列化Respage01Gone相关的数据
    """

    class Meta:
        model = Respage01Gone
        fields = ('time', 'lat', 'lng', 'name', 'address', 'detail_url', 'rate')


class Respage01NewSerializer(serializers.HyperlinkedModelSerializer):
    """
    序列化Respage01New相关的数据
    """

    class Meta:
        model = Respage01New
        fields = ('time', 'lat', 'lng', 'name', 'address', 'detail_url', 'rate')


class Respage01UnionSerializer(serializers.HyperlinkedModelSerializer):
    """
    序列化Respage01相关的数据
    """

    class Meta:
        model = Respage01Union
        fields = ('time', 'lat', 'lng', 'name', 'address', 'detail_url', 'rate')


class Respage01CountSerializer(serializers.HyperlinkedModelSerializer):
    """
    序列化计数数据
    """
    time = serializers.StringRelatedField()
    count = serializers.IntegerField()

    class Meta:
        model = Respage01Info
        fields = ('time', 'count')


class Respage02Serializer(serializers.HyperlinkedModelSerializer):
    """
    序列化Respage02相关的数据
    """

    class Meta:
        model = Respage02Info
        fields = ('time', 'lat', 'lng', 'bikeid', 'type', 'day')


class ProductHuntMonthTopSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ProductHuntMonthTop
        fields = (
            'comments_count', 'day', 'phid', 'name', 'tagline', 'slug', 'votes_count', 'category_id', 'created_at',
            'discussion_url', 'image_url', 'user_id', 'user_name', 'user_twitter_username', 'user_website_url',
            'profile_url', 'month')


class ProductHuntDayTopSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ProductHuntDayTop
        fields = (
            'comments_count', 'day', 'phid', 'name', 'tagline', 'slug', 'votes_count', 'category_id', 'created_at',
            'discussion_url', 'image_url', 'user_id', 'user_name', 'user_twitter_username', 'user_website_url',
            'profile_url', 'days')