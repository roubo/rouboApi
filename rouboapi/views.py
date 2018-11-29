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
import io
import sys
from django.forms.models import model_to_dict
from bs4 import BeautifulSoup
import bs4
from selenium import webdriver

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf8')


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
        AppId = 'wx17dddea5d4fa8dce'
        AppSecret = 'd5fe0741bc02f11820f459274d2299be'
        try:
            URL = 'https://api.weixin.qq.com/sns/jscode2session?appid=' + AppId + \
                  "&secret=" + AppSecret + \
                  "&js_code=" + code + \
                  "&grant_type=authorization_code"
            resp = requests.get(URL)
            return json.loads(resp.text)
        except:
            return None

    def searchJueJinByGoogle(self, key):
        """
        通过 google 自定义搜索获取掘金账号信息
        :param key:
        :return:
        """
        # 非真实，google 自定义搜索的 key 和 id
        APIKEY = 'AIzaSyAqxT53ptmvLDcKwLsh2YrWk6kTo'
        APICX = '010859235238722630878:8tuwg'
        result = []
        try:
            URL = 'https://www.googleapis.com/customsearch/v1?key=' + APIKEY + '&cx=' + APICX + "&q=" + key
            resp = requests.get(URL)
            respjson = json.loads(resp.text)
            skip = False
            for item in respjson['items']:
                if 'displayLink' in item and item['displayLink'] == 'juejin.im':
                    if 'pagemap' in item and 'person' in item['pagemap']:
                        for res in result:
                            if res['userid'] == item['pagemap']['person'][-1]['url'].split('/')[-1]:
                                skip = True
                        if not skip:
                            result.append({
                                'name': item['pagemap']['person'][-1]['name'],
                                'userid': item['pagemap']['person'][-1]['url'].split('/')[-1]
                            })
            return result
        except:
            return None

    def searchJianShu(self, key):
        """
        通过简书 API 获取简书搜索信息
        :param key:
        :return:
        """
        headers = {
            'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 8.0.0; MIX 2 MIUI/8.11.22) okhttp/3.3.0 haruki/4.1.0',
            'HOST': 's0.jianshuapi.com',
            'X-App-Name': 'haruki',
            'X-App-Version': '4.1.0',
            'X-Device-Guid': '869033024218829',
            'X-Timestamp': '1543483341',
            'X-Auth-1': '326b774a36f25bff4b536dd3296a9139',
            'X-NETWORK': '1',
            'Connection': 'Keep-Alive',
            'Accept-Encoding': 'gzip',
            'If-None-Match': 'W/"db59a468cf84fb228826f34cea88ae90"'
        }

        result = []
        try:
            URL = 'https://s0.jianshuapi.com/v3/search/all?q=' + key
            resp = requests.get(URL, headers=headers, verify=False)
            respjson = json.loads(resp.text)
            result = respjson['users']
            return result
        except:
            return result

    def searchJianShuByH5(self, key):
        result = []
        URL = 'https://www.jianshu.com/search?page=1&type=user&q=' + key
        option = webdriver.ChromeOptions()
        option.add_argument('headless')
        option.add_argument('--headless')
        option.add_argument('--disable-gpu')
        driver = webdriver.Chrome(chrome_options=option, executable_path='/Users/JunJian/Downloads/chromedriver')
        driver.get(URL)
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        infos = soup.find_all('div', attrs={'class': 'info'})
        for info in infos:
            res = {}
            for child in info.children:
                if isinstance(child, bs4.element.Tag):
                    if child.attrs and 'href' in child.attrs:
                        res['uid'] = child.attrs['href'].split('/')[2]
                    for ch in child.children:
                        if isinstance(ch, bs4.element.Tag):
                            for chch in ch.children:
                                if '关注' in chch.string:
                                    res['followers'] = chch.string.strip().split(' ')[-1]
                                if '文章' in chch.string:
                                    res['postedPosts'] = chch.string.strip().split(' ')[-1]
                                if '写了' in chch.string:
                                    res['totalCollections'] = chch.string.strip()
                        else:
                            if ch.string != ' ':
                                res['name'] = ch.string.strip()
            result.append(res)
        return result

    def getAndSaveJueJinInfo(self, openid, uid):
        """
        获取具体的掘金用户信息
        :param uid:
        :return:
        """
        URL = 'https://lccro-api-ms.juejin.im/v1/get_multi_user?cols=objectId%7Cusername%7Cavatar_large%7CavatarLarge%7Crole%7Ccompany%7CjobTitle%7Cself_description%7CselfDescription%7CblogAddress%7CisUnitedAuthor%7CisAuthor%7CauthData%7CtotalHotIndex%7CpostedEntriesCount%7CpostedPostsCount%7CcollectedEntriesCount%7CcollectionSetCount%7CsubscribedTagsCount%7CfolloweesCount%7CfollowersCount&src=ios&token=xxx&ids=' + uid
        resp = requests.get(URL)
        respjson = json.loads(resp.text)
        if respjson:
            if OpenCards.objects.filter(openid=openid):
                query = OpenCards.objects.get(openid=openid)
                bskeys = model_to_dict(query)['bskeys']
                if bskeys and bskeys != 'xxx' and bskeys != 'null':
                    bskeys = eval(bskeys)
                else:
                    bskeys = {}
                bskeys['juejin'] = {}
                bskeys['juejin']['followers'] = respjson['d'][uid]['followersCount']
                bskeys['juejin']['totalViews'] = respjson['d'][uid]['totalViewsCount']
                bskeys['juejin']['totalCollections'] = respjson['d'][uid]['totalCollectionsCount']
                bskeys['juejin']['postedPosts'] = respjson['d'][uid]['postedPostsCount']
                bskeys['juejin']['totalComments'] = respjson['d'][uid]['totalCommentsCount']
                bskeys['juejin']['name'] = respjson['d'][uid]['username']
                bskeys['juejin']['uid'] = uid
                OpenCards.objects.filter(openid=openid).update(bskeys=str(bskeys).strip())
                return True
            else:
                return False
        else:
            return False

    def saveConnectInfo(self, openid, phone, email, name):
        if OpenCards.objects.filter(openid=openid):
            query = OpenCards.objects.get(openid=openid)
            bskeys = model_to_dict(query)['bskeys']
            if bskeys and bskeys != 'xxx' and bskeys != 'null':
                bskeys = eval(bskeys)
            else:
                bskeys = {}
            bskeys['connect'] = {}
            bskeys['connect']['name'] = name
            bskeys['connect']['phone'] = phone
            bskeys['connect']['email'] = email
            OpenCards.objects.filter(openid=openid).update(bskeys=str(bskeys).strip())
            return True
        else:
            return False

    def saveJianShuInfo(self, openid, info):
        if OpenCards.objects.filter(openid=openid):
            query = OpenCards.objects.get(openid=openid)
            bskeys = model_to_dict(query)['bskeys']
            if bskeys and bskeys != 'xxx' and bskeys != 'null':
                bskeys = eval(bskeys)
            else:
                bskeys = {}
            bskeys['jianshu'] = {}
            bskeys['jianshu'] = info
            OpenCards.objects.filter(openid=openid).update(bskeys=str(bskeys).strip())
            return True
        else:
            return False

    def get(self, request, format=None):
        req = request.query_params
        if 'type' not in req:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
        if req['type'] == 'login' and 'wxcode' in req:
            res = self.wxCode2Session(req['wxcode'])
            if not res or 'openid' not in res:
                return Response({"data": ""}, status=status.HTTP_200_OK)
            else:
                openid = res['openid']
                session_key = res['session_key']
                if OpenCards.objects.filter(openid=openid):
                    OpenCards.objects.filter(openid=openid).update(session_key=session_key)
                else:
                    data = "openid=" + openid + "&userinfo=null&backup=null&bskeys=null&session_key=" + session_key
                    serializer = OpenCardsSerializer(data=QueryDict(data))
                    if serializer.is_valid():
                        serializer.save()
                return Response({"data": {"openid": openid}}, status=status.HTTP_200_OK)
        elif req['type'] == 'search' and 'from' in req and req['from'] == 'juejin' and 'key' in req:
            res = self.searchJueJinByGoogle(req['key'])
            if res:
                return Response({"data": res}, status=status.HTTP_200_OK)
            else:
                return Response({}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        elif req['type'] == 'search' and 'from' in req and req['from'] == 'jianshu' and 'key' in req:
            res = self.searchJianShuByH5(req['key'])
            if res:
                return Response({"data": res}, status=status.HTTP_200_OK)
            else:
                return Response({}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        elif req['type'] == 'save' and 'from' in req and 'openid' in req and req['from'] == 'juejin':
            res = self.getAndSaveJueJinInfo(req['openid'], req['uid'])
            if res:
                return Response({"data": []}, status=status.HTTP_200_OK)
            else:
                return Response({}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        elif req['type'] == 'save' and 'from' in req and 'openid' in req and req['from'] == 'jianshu':
            res = self.saveJianShuInfo(req['openid'], req['info'])
            if res:
                return Response({"data": []}, status=status.HTTP_200_OK)
            else:
                return Response({}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        elif req['type'] == 'save' and 'from' in req and 'openid' in req and req['from'] == 'connect':
            try:
                res = self.saveConnectInfo(req['openid'], req['phone'], req['email'], req['name'])
                if res:
                    return Response({"data": {}}, status=status.HTTP_200_OK)
                else:
                    return Response({'data': {}}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            except:
                return Response({'data': {}}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        elif req['type'] == 'bskeys' and 'openid' in req and 'from' in req and req['from'] == 'juejin':
            if OpenCards.objects.filter(openid=req['openid']):
                try:
                    query = OpenCards.objects.get(openid=req['openid'])
                    serializer = OpenCardsSerializer(query)
                    data = serializer.data
                    data['bskeys'] = eval(data['bskeys'])
                    self.getAndSaveJueJinInfo(req['openid'], data['bskeys']['juejin']['uid'])
                    query = OpenCards.objects.get(openid=req['openid'])
                    serializer = OpenCardsSerializer(query)
                    data = serializer.data
                    data['bskeys'] = eval(data['bskeys'])
                    return Response({"data": data['bskeys']['juejin']}, status=status.HTTP_200_OK)
                except:
                    return Response({"data": {}}, status=status.HTTP_200_OK)
            else:
                return Response({"data": {}}, status=status.HTTP_200_OK)
        elif req['type'] == 'bskeys' and 'openid' in req and 'from' in req and req['from'] == 'connect':
            if OpenCards.objects.filter(openid=req['openid']):
                try:
                    query = OpenCards.objects.get(openid=req['openid'])
                    serializer = OpenCardsSerializer(query)
                    data = serializer.data
                    data['bskeys'] = eval(data['bskeys'])
                    return Response({"data": data['bskeys']['connect']}, status=status.HTTP_200_OK)
                except:
                    return Response({"data": {}}, status=status.HTTP_200_OK)
            else:
                return Response({"data": {}}, status=status.HTTP_200_OK)
        elif req['type'] == 'bskeys' and 'openid' in req and 'from' in req and req['from'] == 'jianshu':
            if OpenCards.objects.filter(openid=req['openid']):
                try:
                    query = OpenCards.objects.get(openid=req['openid'])
                    serializer = OpenCardsSerializer(query)
                    data = serializer.data
                    data['bskeys'] = eval(data['bskeys'])
                    return Response({"data": data['bskeys']['jianshu']}, status=status.HTTP_200_OK)
                except:
                    return Response({"data": {}}, status=status.HTTP_200_OK)
            else:
                return Response({"data": {}}, status=status.HTTP_200_OK)
