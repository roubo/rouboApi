from rest_framework import serializers
from rouboapi.models import DeviceReport
from rouboapi.models import Respage01Info


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
