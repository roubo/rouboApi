from rouboapi.serializers import DeviceReportSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class DeviceReport(APIView):
    """
    上报设备信息
    """
    authentication_classes = []
    permission_classes = []

    def get (self, request, format=None):
        """
        :param  report_type: 上报类型，比如启动上报：open
        :param  report_time: 上报时间戳
        :param  device_id: 可以描述设备的id
        :param  ip_address: 公网ip地址
        """
        serializer = DeviceReportSerializer(data=request.query_params)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
