# -*- coding: utf-8 -*-
from __future__ import absolute_import
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.yappi_stats, name='profiling_yappi_stats'),
    url(r'^do$', views.yappi_manage, name='profiling_yappi_manage'),
    url(r'^memory-usage$', views.memory_usage, name='profiling_memory_usage'),
    url(r'^top/$', views.web_top, name='profiling_web_top'),
    url(r'^top/(?P<pid>\d+)$', views.process_info, name='profiling_process_info')
]
