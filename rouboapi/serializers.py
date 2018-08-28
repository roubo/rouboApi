from rest_framework import serializers
from rouboapi.models import DeviceReport


class DeviceReportSerializer(serializers.HyperlinkedModelSerializer):

    """
    序列化上报接口数据
    """
    class Meta:
        model = DeviceReport
        fields = ('report_type', 'report_time', 'device_id', 'ip_address')

