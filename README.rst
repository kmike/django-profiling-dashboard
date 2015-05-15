==========================
django-profiling-dashboard
==========================

django-profiling-dashboard provides a dashboard with various profiling tools suitable
for use in live servers.

Requirements
============

* `yappi <http://code.google.com/p/yappi/>`_ for thread-aware live server profiling
  that can be enabled and disabled at run time;
* `Pympler <http://code.google.com/p/pympler/>`_ for memory debugging;
* `psutil <http://code.google.com/p/psutil/>`_ for system resource usage investigation;
* `django-query-exchange <https://github.com/daevaorn/django-query-exchange>`_.

Dashboard remplates are based on `Bootstrap <http://twitter.github.com/bootstrap/>`_ toolkit.

django-profiling-dashboard requires django >= 1.5 and python >= 2.6.

Installation
============

Make sure the requirements are installed::

    pip install yappi pympler psutil
    pip install git+https://github.com/daevaorn/django-query-exchange.git#egg=django-query-exchange

and install django-profiling-dashboard using pip::

    pip install django-profiling-dashboard

Usage
=====

1. Add ``'profiling_dashboard'`` and ``'query_exchange'`` to ``INSTALLED_APPS``::

       INSTALLED_APPS = (
           # ...
           'query_exchange',
           'profiling_dashboard',
           # ...
       )

2. include 'profiling_dashboard.urls' in your urls.py::

      urlpatterns = patterns('',
          # ...
          url(r'^profiling-dashboard/', include('profiling_dashboard.urls')),
          # ...
      )

3. visit /profiling-dashboard/

Screenshots
===========

TODO


Notes on CPU profiling in multi-process environment
===================================================

If there are several server processes then the profiler have to be started and stopped for each process,
and the profiling stats will be different for different processes.

In some deployment schemas (e.g. apache proxied by nginx) there is no way to make sure subsequent requests
will be handled by the same server process so take this in account while using django-profiling-dashboard.
