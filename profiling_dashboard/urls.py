# -*- coding: utf-8 -*-
from __future__ import absolute_import
from django.conf.urls.defaults import *

urlpatterns = patterns('profiling_dashboard.views',
    url(r'^do$', 'yappi_manage', name='profiling_yappi_manage'),
    url(r'^memory-usage$', 'memory_usage', name='profiling_memory_usage'),
    url(r'^top/$', 'web_top', name='profiling_web_top'),
    url(r'^top/(?P<pid>\d+)$', 'process_info', name='profiling_process_info'),
    url(r'^$', 'yappi_stats', name='profiling_yappi_stats')
)
