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


# sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf8')


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

    # --------------------------------------------------------------------
    # openCard 搜索接口
    # 接口特点：各种聚合内容的搜索方式不同，基本上是基于 api 和基于网页实时爬取两种
    #          搜索结果只用于前端展示，提供给用户选择，所以入库，也不获取复杂的详细信息
    # --------------------------------------------------------------------

    def searchJueJinByGoogle(self, key):
        """
        通过 google 自定义搜索获取掘金账号信息(次数受限，每天仅100次）
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

    def searchGitHub(self, key):
        """
        通过 github 公开 api ，无访问限制
        :param key:
        :return:
        """
        result = []
        URL = 'https://api.github.com/search/users?q=' + key
        try:
            resp = requests.get(URL)
            respjson = json.loads(resp.text)
            result = respjson['items']
            return result
        except:
            return result

    def searchJianShuByH5(self, key):
        """
        通过实时爬取简书搜索用户页面获取信息，速度慢，但是为了不浪费一次爬虫数据，便尽可能多地获取有用数据
        （仅爬取一个页面）
        :param key:
        :return:
        """
        result = []
        URL = 'https://www.jianshu.com/search?page=1&type=user&q=' + key
        option = webdriver.ChromeOptions()
        option.add_argument('headless')
        option.add_argument('--headless')
        option.add_argument('--disable-gpu')
        driver = webdriver.Chrome(chrome_options=option, executable_path='/data/bin/chromedriver')
        driver.get(URL)
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        infos = soup.find_all('div', attrs={'class': 'info'})
        for info in infos:
            res = {}
            for child in info.children:
                if isinstance(child, bs4.element.Tag):
                    """ 由于简书阅读量的爬取速度慢，严重影响 api 质量，所以暂时先停止该数据的获取。后期改用异步爬取的方式优化
                    if child.attrs and 'href' in child.attrs:
                        res['uid'] = child.attrs['href'].split('/')[2]
                        res['totalViews'] = 0
                        for page in range(1, 100):
                            driver.get('https://www.jianshu.com/u/' + res['uid']+'?order_by=shared_at&page=' + str(page))
                            soup2 = BeautifulSoup(driver.page_source, 'html.parser')
                            tags = soup2.find('ul', attrs={'class': 'note-list'})
                            count = 0
                            for ch in tags:
                                if isinstance(ch, bs4.element.Tag):
                                    for chch in ch:
                                        if isinstance(chch, bs4.element.Tag):
                                            try:
                                                for chchch in chch.div.a:
                                                    if isinstance(chchch, bs4.element.NavigableString) and chchch.string.strip() != '':
                                                        res['totalViews'] += int(chchch.string.strip())
                                                        count += 1
                                            except:
                                                pass
                            if count < 9:
                                break
                    """
                    for ch in child.children:
                        if isinstance(ch, bs4.element.Tag):
                            for chch in ch.children:
                                if '粉丝' in chch.string:
                                    res['followers'] = chch.string.strip().split(' ')[-1]
                                if '文章' in chch.string:
                                    res['postedPosts'] = chch.string.strip().split(' ')[-1]
                                if '写了' in chch.string:
                                    res['totalCollections'] = chch.string.strip()
                        else:
                            if ch.string != ' ':
                                res['name'] = ch.string.strip()
            result.append(res)
        if driver:
            driver.close()
        return result

    # --------------------------------------------------------------------
    # openCard  详情数据获取接口
    # 接口特点：各种聚合内容的详情数据方式也不同，还是基于 api 和基于网页实时爬取两种
    #          详情数据目前有三种类型：
    #          1、可以实时获取的数据，该类接口先获取最新数据后，入库，后吐给客户端
    #          2、非实时获取的数据，直接从库中读出，返回客户端，数据的更新又后台定时进行
    #          3、第三方的 api 稳定、实时性好的详情数据，不入库保持，直接返回给客户端
    # --------------------------------------------------------------------
    def getJianShuInfoByH5(self, openid, uid):
        """
        （实时获取）简书详情信息，爬虫实现
        :param openid:
        :param uid:
        :return:
        """
        if OpenCards.objects.filter(openid=openid):
            query = OpenCards.objects.get(openid=openid)
            bskeys = model_to_dict(query)['bskeys']
            if bskeys and bskeys != 'xxx' and bskeys != 'null':
                bskeys = eval(bskeys)
            else:
                bskeys = {}
            bskeys['jianshu'] = {}
            option = webdriver.ChromeOptions()
            option.add_argument('headless')
            option.add_argument('--headless')
            option.add_argument('--disable-gpu')
            driver = webdriver.Chrome(chrome_options=option, executable_path='/data/bin/chromedriver')
            for page in range(1, 100):
                driver.get('https://www.jianshu.com/u/' + uid + '?order_by=shared_at&page=' + str(page))
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                # 获取用户信息
                if 'followers' not in bskeys['jianshu']:
                    title = soup.find('div', attrs={'class': 'title'})
                    bskeys['jianshu']['name'] = title.a.string.strip()
                    info = soup.find('div', attrs={'class': 'info'})
                    count = 0
                    for ch in info.children:
                        if isinstance(ch, bs4.element.Tag):
                            for chch in ch:
                                if isinstance(chch, bs4.element.Tag):
                                    if count == 1:
                                        bskeys['jianshu']['followers'] = chch.div.p.string.strip()
                                    if count == 2:
                                        bskeys['jianshu']['postedPosts'] = chch.div.p.string.strip()
                                    if count == 3:
                                        bskeys['jianshu']['totalCollections'] = '写了' + chch.div.p.string.strip() + '字,'
                                    if count == 4:
                                        bskeys['jianshu'][
                                            'totalCollections'] += '获得了' + chch.div.p.string.strip() + '个喜欢'
                                    count += 1
                else:
                    # 不再获取阅读量，故直接返回
                    break
                """ 由于简书阅读量的爬取速度慢，严重影响 api 质量，所以暂时先停止该数据的获取。后期改用异步爬取的方式优化
                tags = soup.find('ul', attrs={'class': 'note-list'})
                count = 0
                for ch in tags:
                    if isinstance(ch, bs4.element.Tag):
                        for chch in ch:
                            if isinstance(chch, bs4.element.Tag):
                                try:
                                    for chchch in chch.div.a:
                                        if isinstance(chchch,
                                                      bs4.element.NavigableString) and chchch.string.strip() != '':
                                            bskeys['jianshu']['totalViews'] += int(chchch.string.strip())
                                            count += 1
                                except:
                                    pass
                if count < 9:
                    break
                """
            bskeys['jianshu']['uid'] = uid
            OpenCards.objects.filter(openid=openid).update(bskeys=str(bskeys).strip())
            driver.close()
            return True
        return False

    def getGitHubInfo(self, openid, name):
        """
        (实时获取）获取具体的github用户信息，不入库
        :param uid:
        :return:
        """
        res = {}
        URL = 'https://api.github.com/users/' + name
        try:
            resp = requests.get(URL)
            respjson = json.loads(resp.text)
            res = respjson
            return res
        except:
            return res

    def getGitHubRepos(self, name):
        """
        (实时获取）获取具体的github用户的仓库列表
        :param name:
        :return:
        """
        res = {}
        URL = 'https://api.github.com/users/' + name + '/repos'
        try:
            resp = requests.get(URL)
            respjson = json.loads(resp.text)
            res = respjson
            return res
        except:
            return res

    def getAndSaveJueJinInfo(self, openid, uid):
        """
        实时获取具体的掘金用户信息（接口）
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

    # --------------------------------------------------------------------
    # openCard  保存用户选择接口
    # 接口特点: 只保存关键数据，与 openid 做好映射
    # --------------------------------------------------------------------
    def saveConnectInfo(self, openid, phone, email, name):
        """
         保存联系方式信息
        :param openid:
        :param phone:
        :param email:
        :param name:
        :return:
        """
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
        """
        保存用户简书信息
        :param openid:
        :param info:
        :return:
        """
        if OpenCards.objects.filter(openid=openid):
            query = OpenCards.objects.get(openid=openid)
            bskeys = model_to_dict(query)['bskeys']
            if bskeys and bskeys != 'xxx' and bskeys != 'null':
                bskeys = eval(bskeys)
            else:
                bskeys = {}
            bskeys['jianshu'] = {}
            bskeys['jianshu'] = eval(info)
            OpenCards.objects.filter(openid=openid).update(bskeys=str(bskeys).strip())
            return True
        else:
            return False

    def saveGitHubInfo(self, openid, id, name):
        """
        保存 github 用户信息
        :param openid:
        :param id:
        :param name:
        :return:
        """
        if OpenCards.objects.filter(openid=openid):
            query = OpenCards.objects.get(openid=openid)
            bskeys = model_to_dict(query)['bskeys']
            if bskeys and bskeys != 'xxx' and bskeys != 'null':
                bskeys = eval(bskeys)
            else:
                bskeys = {}
            bskeys['github'] = {}
            bskeys['github']['id'] = str(id)
            bskeys['github']['login'] = name
            OpenCards.objects.filter(openid=openid).update(bskeys=str(bskeys).strip())
            return True
        else:
            return False

    def get(self, request, format=None):
        """
        接口入口：待规范
        :param request:
        :param format:
        :return:
        """
        req = request.query_params
        # 通用参数检测
        if 'type' not in req:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
        # 微信用户鉴权
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
        # 搜索掘金
        elif req['type'] == 'search' and 'from' in req and req['from'] == 'juejin' and 'key' in req:
            res = self.searchJueJinByGoogle(req['key'])
            if res:
                return Response({"data": res}, status=status.HTTP_200_OK)
            else:
                return Response({}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        # 搜索简书
        elif req['type'] == 'search' and 'from' in req and req['from'] == 'jianshu' and 'key' in req:
            res = self.searchJianShuByH5(req['key'])
            if res:
                return Response({"data": res}, status=status.HTTP_200_OK)
            else:
                return Response({}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        # 搜索github
        elif req['type'] == 'search' and 'from' in req and req['from'] == 'github' and 'key' in req:
            res = self.searchGitHub(req['key'])
            if res:
                return Response({"data": res}, status=status.HTTP_200_OK)
            else:
                return Response({}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        # 保存github
        elif req['type'] == 'save' and 'from' in req and 'openid' in req and req['from'] == 'github':
            res = self.saveGitHubInfo(req['openid'], req['id'], req['login'])
            if res:
                return Response({"data": []}, status=status.HTTP_200_OK)
            else:
                return Response({}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        # 保存掘金
        elif req['type'] == 'save' and 'from' in req and 'openid' in req and req['from'] == 'juejin':
            res = self.getAndSaveJueJinInfo(req['openid'], req['uid'])
            if res:
                return Response({"data": []}, status=status.HTTP_200_OK)
            else:
                return Response({}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        # 保存简书
        elif req['type'] == 'save' and 'from' in req and 'openid' in req and req['from'] == 'jianshu':
            res = self.saveJianShuInfo(req['openid'], req['info'])
            if res:
                return Response({"data": []}, status=status.HTTP_200_OK)
            else:
                return Response({}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        # 保存联系方式
        elif req['type'] == 'save' and 'from' in req and 'openid' in req and req['from'] == 'connect':
            try:
                res = self.saveConnectInfo(req['openid'], req['phone'], req['email'], req['name'])
                if res:
                    return Response({"data": {}}, status=status.HTTP_200_OK)
                else:
                    return Response({'data': {}}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            except:
                return Response({'data': {}}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        # 获取掘金详情
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
        # 获取联系方式详情
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
        # 获取简书详情
        elif req['type'] == 'bskeys' and 'openid' in req and 'from' in req and req['from'] == 'jianshu':
            if OpenCards.objects.filter(openid=req['openid']):
                try:
                    query = OpenCards.objects.get(openid=req['openid'])
                    serializer = OpenCardsSerializer(query)
                    data = serializer.data
                    data['bskeys'] = eval(data['bskeys'])
                    self.getJianShuInfoByH5(req['openid'], data['bskeys']['jianshu']['uid'])
                    query = OpenCards.objects.get(openid=req['openid'])
                    serializer = OpenCardsSerializer(query)
                    data = serializer.data
                    data['bskeys'] = eval(data['bskeys'])
                    return Response({"data": data['bskeys']['jianshu']}, status=status.HTTP_200_OK)
                except:
                    return Response({"data": {}}, status=status.HTTP_200_OK)
            else:
                return Response({"data": {}}, status=status.HTTP_200_OK)
        # 获取github详情
        elif req['type'] == 'bskeys' and 'openid' in req and 'from' in req and req['from'] == 'github':
            if OpenCards.objects.filter(openid=req['openid']):
                try:
                    query = OpenCards.objects.get(openid=req['openid'])
                    serializer = OpenCardsSerializer(query)
                    data = serializer.data
                    data['bskeys'] = eval(data['bskeys'])
                    res = self.getGitHubInfo(req['openid'], data['bskeys']['github']['login'])
                    return Response({"data": res}, status=status.HTTP_200_OK)
                except:
                    return Response({"data": {}}, status=status.HTTP_200_OK)
            else:
                return Response({"data": {}}, status=status.HTTP_200_OK)
        elif req['type'] == 'repo' and 'from' in req and req['from'] == 'github':
            try:
                res = self.getGitHubRepos(req['login'])
                return Response({"data": res}, status=status.HTTP_200_OK)
            except:
                return Response({"data":{}}, status=status.HTTP_200_OK)
