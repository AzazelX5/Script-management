# encoding:utf-8
from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^get_script/$', views.get_script),  # 获取全本脚本
    url(r'^get_script/(?P<script_id>[0-9a-f]{1,8}-?'
        r'([0-9a-f]{0,4}-){0,3}[0-9a-f]{0,12})$', views.get_script),  # 获取单个脚本
    url(r'^save_script/$', views.save_script),  # 保存脚本
    url(r'^del_script/$', views.del_script),  # 删除脚本
]
