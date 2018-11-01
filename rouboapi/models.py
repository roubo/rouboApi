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


class Respage02Info(models.Model):
    """
    respage 02 相关的数据
    """
    time = models.CharField(max_length=100)
    bikeid = models.CharField(max_length=200)
    lat = models.FloatField()
    lng = models.FloatField()
    type = models.CharField(max_length=100)

    class Meta:
        db_table = "respage02"


class ProductHuntMonthTop(models.Model):
    """
    PH月数据
    """
    comments_count = models.CharField(max_length=200)
    day = models.CharField(max_length=200)
    phid = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    tagline = models.CharField(max_length=200)
    slug = models.CharField(max_length=200)
    votes_count = models.CharField(max_length=200)
    category_id = models.CharField(max_length=200)
    created_at = models.CharField(max_length=200)
    discussion_url = models.CharField(max_length=200)
    image_url = models.CharField(max_length=200)
    user_id = models.CharField(max_length=200)
    user_name = models.CharField(max_length=200)
    user_twitter_username = models.CharField(max_length=200)
    user_website_url = models.CharField(max_length=200)
    profile_url = models.CharField(max_length=200)
    month = models.CharField(max_length=200)

    class Meta:
        db_table = "ph_month_top"


class ProductHuntDayTop(models.Model):
    """
    PH日数据
    """
    comments_count = models.CharField(max_length=200)
    day = models.CharField(max_length=200)
    phid = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    tagline = models.CharField(max_length=200)
    slug = models.CharField(max_length=200)
    votes_count = models.CharField(max_length=200)
    category_id = models.CharField(max_length=200)
    created_at = models.CharField(max_length=200)
    discussion_url = models.CharField(max_length=200)
    image_url = models.CharField(max_length=200)
    user_id = models.CharField(max_length=200)
    user_name = models.CharField(max_length=200)
    user_twitter_username = models.CharField(max_length=200)
    user_website_url = models.CharField(max_length=200)
    profile_url = models.CharField(max_length=200)
    days = models.CharField(max_length=200)

    class Meta:
        db_table = "ph_day_top"
