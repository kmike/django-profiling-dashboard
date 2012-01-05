# -*- coding: utf-8 -*-
from __future__ import absolute_import
import os
import threading
import psutil
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from .forms import YappiManageForm, YappiFilterForm, MuppyFilterForm, TopFilterForm
from .stats import get_yappi_status, proc_annotate_with_short_info, proc_annotate_with_full_info

def _tid_safe():
    try:
        return threading.currentThread().ident
    except Exception as e:
        return str(e)


@staff_member_required
def yappi_manage(request):
    form = YappiManageForm(request.POST or None)
    if form.is_valid():
        pid = os.getpid()
        try:
            action = form.do_action()
            messages.success(request, "yappi %s is successful for process #%s" % (action, pid))
        except Exception as e:
            messages.info(request, "process #%s" % pid)
            messages.error(request, e)
    return redirect('profiling_yappi_stats')


@staff_member_required
def yappi_stats(request):
    form = YappiFilterForm(request.GET or None)
    stats, other_stats = [], []
    status = get_yappi_status()
    pid = os.getpid()
    if form.is_valid():
        try:
            stats = form.get_stats()
            other_stats = form.get_other_stats()
        except Exception as e:
            messages.info(request, "process #%s" % pid)
            messages.error(request, e)

    return TemplateResponse(request, 'profiling_dashboard/cpu.html', {
        'form': form,
        'stats': stats,
        'other_stats': other_stats,
        'status': status,
        'pid': pid,
        'tid': _tid_safe(),
    })


@staff_member_required
def memory_usage(request):
    pid = os.getpid()

    form = MuppyFilterForm(request.GET or None)
    size, report = None, None
    if form.is_valid():
        size, report = form.get_report()

    return TemplateResponse(request, 'profiling_dashboard/memory.html', {
        'form': form,
        'size': size,
        'report': report,
        'pid': pid,
        'tid': _tid_safe(),
    })

@staff_member_required
def web_top(request):
    pid = os.getpid()
    form = TopFilterForm(request.GET or None)

    processes = []
    if form.is_valid():
        processes = form.get_processes()

    return TemplateResponse(request, 'profiling_dashboard/web_top.html', {
        'pid': pid,
        'processes': processes,
        'form': form,
        'tid': _tid_safe(),
    })

@staff_member_required
def process_info(request, pid):
    try:
        proc = psutil.Process(int(pid))
    except Exception as e:
        messages.error(request, "process %s: %s" % (pid, e))
        return redirect('profiling_web_top')

    proc_annotate_with_short_info(proc)
    proc_annotate_with_full_info(proc)

    return TemplateResponse(request, 'profiling_dashboard/process_info.html', {
        'pid': os.getpid(),
        'tid': _tid_safe(),
        'proc': proc,
    })