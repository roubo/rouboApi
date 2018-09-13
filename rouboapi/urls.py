from django.conf.urls import url
from . import views
from rest_framework.documentation import include_docs_urls
API_TITLE = 'roubo api documentation'
API_DESCRIPTION = 'roubo api server for rouboinfo'

urlpatterns = [
    url(r'v1/report/$', views.DeviceReport.as_view(), name='DeviceReport'),
    url(r'docs/', include_docs_urls(title=API_TITLE, description=API_DESCRIPTION, authentication_classes=[], permission_classes=[])),
    url(r'v1/respage01/$', views.Respage01.as_view(), name='Respage01')
]