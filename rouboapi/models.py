from django.db import models


class DeviceReport(models.Model):
    """
    收集设备相关的统计数据
    report_id
        自增id作为主键
    report_type
        上报类型，比如启动上报：open
    report_time
        上报时间戳
    device_id
        可以描述设备的id
    ip_address
        公网ip地址
    """
    report_type = models.CharField(max_length=100)
    report_time = models.DateTimeField(auto_now_add=True)
    device_id = models.CharField(max_length=200)
    ip_address = models.CharField(max_length=50)



class Respage01Info(models.Model):
    """
    respage 01 相关的数据
    """
    time = models.CharField(max_length=100)
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=500)
    detail_url = models.URLField(max_length=500)
    rate = models.FloatField()
    lat = models.FloatField()
    lng = models.FloatField()

    class Meta:
        db_table = "respage01"



class Respage01Gone(models.Model):
    """
    respage 01 店面减少 相关的数据
    """
    time = models.CharField(max_length=100)
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=500)
    detail_url = models.URLField(max_length=500)
    rate = models.FloatField()
    lat = models.FloatField()
    lng = models.FloatField()

    class Meta:
        db_table = "respage01Gone"

class Respage01New(models.Model):
    """
    respage 01 店面增加 相关的数据
    """
    time = models.CharField(max_length=100)
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=500)
    detail_url = models.URLField(max_length=500)
    rate = models.FloatField()
    lat = models.FloatField()
    lng = models.FloatField()

    class Meta:
        db_table = "respage01New"


class Respage01Union(models.Model):
    """
    respage 01 店面集合 相关的数据
    """
    time = models.CharField(max_length=100)
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=500)
    detail_url = models.URLField(max_length=500)
    rate = models.FloatField()
    lat = models.FloatField()
    lng = models.FloatField()

    class Meta:
        db_table = "respage01Union"