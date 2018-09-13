from rouboapi.serializers import DeviceReportSerializer
from rouboapi.serializers import Respage01Serializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rouboapi.models import Respage01Info
from datetime import datetime
import pandas as pd


class DeviceReport(APIView):
    """
    上报设备信息
    """
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
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


class Respage01(APIView):
    """
    获取respage01相关的数据
    """

    authentication_classes = []
    permission_classes = []

    def rangeTime(self, start_time, end_time):
        """
        获取时间区间
        :param start_time:
        :param end_time:
        :return:
        """
        print("------------")
        dateList = [datetime.strftime(x, "%Y_%m_%d")
                    for x in list(pd.date_range(start=start_time.replace('_',''), end=end_time.replace('_','')))]
        return dateList

    def get(self, request, format=None):
        req = request.query_params
        if 'type' not in req or 'start_time' not in req or 'end_time' not in req:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
        if req['type'] == 'location':
            dateList = self.rangeTime(start_time=req['start_time'], end_time=req['end_time'])
            queryset = Respage01Info.objects.filter(time__in=dateList)
            serializer = Respage01Serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
