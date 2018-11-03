from django.conf.urls import url
from . import views
from rest_framework.documentation import include_docs_urls
API_TITLE = 'Roubo Api documentation'
API_DESCRIPTION = '一些用于业余研究的自维护 api，如有疑问请联系我：daijunjian11@gmail.com'

urlpatterns = [
    url(r'docs/', include_docs_urls(title=API_TITLE, description=API_DESCRIPTION, authentication_classes=[], permission_classes=[])),
    url(r'v1/report/$', views.DeviceReport.as_view(), name='DeviceReport'),
    url(r'v1/respage01/$', views.Respage01.as_view(), name='Respage01'),
    url(r'v1/respage02/$', views.Respage02.as_view(), name='Respage02'),
    url(r'v1/producthunt/top$', views.ProductHuntTop.as_view(), name='ProductHuntTop'),
]