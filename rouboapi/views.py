from rouboapi.serializers import DeviceReportSerializer
from rouboapi.serializers import Respage01Serializer
from rouboapi.serializers import Respage02Serializer
from rouboapi.serializers import Respage01CountSerializer
from rouboapi.serializers import Respage01GoneSerializer
from rouboapi.serializers import Respage01NewSerializer
from rouboapi.serializers import Respage01UnionSerializer
from rouboapi.serializers import ProductHuntDayTopSerializer
from rouboapi.serializers import ProductHuntMonthTopSerializer
from rouboapi.serializers import OpenCardsSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rouboapi.models import Respage01Info
from rouboapi.models import Respage01New
from rouboapi.models import Respage01Gone
from rouboapi.models import Respage01Union
from rouboapi.models import Respage02Info
from rouboapi.models import ProductHuntMonthTop
from rouboapi.models import ProductHuntDayTop
from rouboapi.models import OpenCards
from django.db.models import Count
from datetime import datetime, timedelta
import pandas as pd
import requests
import json
from django.http import QueryDict


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
        print(request.query_params)
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
        dateList = [datetime.strftime(x, "%Y_%m_%d")
                    for x in list(pd.date_range(start=start_time.replace('_', ''), end=end_time.replace('_', '')))]
        return dateList

    def get(self, request, format=None):
        req = request.query_params
        if 'type' not in req:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
        if req['type'] == 'location':
            dateList = self.rangeTime(start_time=req['start_time'], end_time=req['end_time'])
            queryset = Respage01Info.objects.filter(time__in=dateList)
            serializer = Respage01Serializer(queryset, many=True)
        elif req['type'] == 'count':
            dateList = self.rangeTime(start_time=req['start_time'], end_time=req['end_time'])
            queryset = Respage01Info.objects.filter(time__in=dateList).values('time').annotate(count=Count('id'))
            serializer = Respage01CountSerializer(queryset, many=True)
        elif req['type'] == 'stat':
            querysetNew = Respage01New.objects.all()
            serializerNew = Respage01NewSerializer(querysetNew, many=True)
            querysetGone = Respage01Gone.objects.all()
            serializerGone = Respage01GoneSerializer(querysetGone, many=True)
            querysetUnion = Respage01Union.objects.all()
            serializerUnion = Respage01UnionSerializer(querysetUnion, many=True)
            return Response({
                'new': serializerNew.data,
                'gone': serializerGone.data,
                'union': serializerUnion.data
            }, status=status.HTTP_200_OK)
        return Response(serializer.data, status=status.HTTP_200_OK)


class Respage02(APIView):
    """
    获取respage02相关的数据
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
        res = []
        start = datetime.strptime(start_time, '%Y_%m_%d_%H')
        end = datetime.strptime(end_time, '%Y_%m_%d_%H')
        step = timedelta(hours=1)

        while start <= end:
            res.append(start.strftime('%Y_%m_%d_%H'))
            start += step
        return res

    def get(self, request, format=None):
        req = request.query_params
        if 'type' not in req:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
        if req['type'] == 'now':
            if 'day' not in req:
                return Response({}, status=status.HTTP_400_BAD_REQUEST)
            timelist = Respage02Info.objects.distinct().values("time").filter(day=req['day']).order_by('-time').all()
            now = timelist[0]['time']
            queryset = Respage02Info.objects.filter(day=req['day']).filter(time=now)
            serializer = Respage02Serializer(queryset, many=True)
        if req['type'] == 'timelist':
            if 'day' not in req:
                return Response({}, status=status.HTTP_400_BAD_REQUEST)
            timelist = Respage02Info.objects.distinct().values("time").filter(day=req['day']).order_by('time').all()
            return Response(timelist, status=status.HTTP_200_OK)
        if req['type'] == 'location':
            if 'day' not in req or 'time' not in req:
                return Response({}, status=status.HTTP_400_BAD_REQUEST)
            queryset = Respage02Info.objects.filter(day=req['day']).filter(time=req['time'])
            serializer = Respage02Serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProductHuntTop(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        req = request.query_params
        if 'type' not in req:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
        if req['type'] == 'month':
            queryset = ProductHuntMonthTop.objects.filter(month=req['index'])
            serializer = ProductHuntMonthTopSerializer(queryset, many=True)
        if req['type'] == 'day':
            queryset = ProductHuntDayTop.objects.filter(days=req['index'])
            serializer = ProductHuntDayTopSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class OpenCard(APIView):
    """
    OpenCards
    """
    authentication_classes = []
    permission_classes = []

    def wxCode2Session(self, code):
        """
        微信 code2Session 实现
        :param code:
        :return:
        """
        # 非真实
        AppId = 'wx17dddea5d4fa8dceer'
        AppSecret = 'd5fe0741bc02f11820f459274d2299beer'
        try:
            URL = 'https://api.weixin.qq.com/sns/jscode2session?appid=' + AppId + \
                  "&secret=" + AppSecret + \
                  "&js_code=" + code + \
                  "&grant_type=authorization_code"
            resp = requests.get(URL)
            return json.loads(resp.text)
        except:
            return None

    def get(self, request, format=None):
        req = request.query_params
        if 'type' not in req:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
        if req['type'] == 'login' and 'wxcode' in req:
            res = self.wxCode2Session(req['wxcode'])
            if not res or 'openid' not in res:
                return Response({"data":""}, status=status.HTTP_200_OK)
            else:
                openid = res['openid']
                session_key = res['session_key']
                if OpenCards.objects.filter(openid=openid):
                    OpenCards.objects.filter(openid=openid).update(session_key=session_key)
                else:
                    data = "openid="+openid+"&userinfo=null&backup=null&bskeys=null&session_key=" + session_key
                    serializer = OpenCardsSerializer(data=QueryDict(data))
                    if serializer.is_valid():
                        serializer.save()
                return Response({"data": {"openid": openid}}, status=status.HTTP_200_OK)
