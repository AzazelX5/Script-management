from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^get_script/$', views.get_script),
    url(r'^get_script/(?P<script_id>[0-9a-f]{1,8}-?([0-9a-f]{0,4}-){0,3}[0-9a-f]{0,12})$', views.get_script),
    url(r'^save_script/$', views.save_script),
]
