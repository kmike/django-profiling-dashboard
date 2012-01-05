# -*- coding: utf-8 -*-
from __future__ import absolute_import
from collections import namedtuple
from contextlib import contextmanager
import datetime
from time import strftime
import psutil
import yappi

YappiStat = namedtuple('YappiStat', 'name ncall ttotal tsub tavg')

def _get_all_yappi_stats():
    res = []
    def handle(data):
        avg = data[2]/data[1]
        stat = YappiStat(*(data+(avg,)))
        res.append(stat)
    yappi.enum_stats(handle)
    return res

def get_full_yappi_stats(sorttype=yappi.SORTTYPE_NCALL, sortorder=yappi.SORTORDER_DESCENDING, limit=yappi.SHOW_ALL):
    """
    Like yappi.get_stats, but returns a list of namedtuples with the full information for function profiling data.
    """

    stats = _get_all_yappi_stats()
    stats.sort(key=lambda stat: stat[sorttype], reverse=sortorder)

    if limit != yappi.SHOW_ALL:
        stats = stats[:limit]

    return stats

def get_other_yappi_stats():
    stats = yappi.get_stats(limit=0)
    THREAD_HEADER = '\n\nname           tid    fname                                scnt     ttot'
    thread_index = stats.index(THREAD_HEADER)
    stats[thread_index] = stats[thread_index].strip()
    return stats[thread_index:]

def get_yappi_status():
    try:
        other_stats = get_other_yappi_stats()
        last_line = other_stats[-1]
        return last_line.split()[0]
    except Exception as e:
        return str(e)

@contextmanager
def _ignore_AccessDenied():
    try:
        yield
    except psutil.AccessDenied:
        pass
    except AttributeError:
        pass

def proc_annotate_with_short_info(p):
    p._READY = False
    with _ignore_AccessDenied():
        p.PID = p.pid
        p.USERNAME = p.username
        p.CMDLINE = ' '.join(p.cmdline)
        p.NAME = p.name
        p.RSS, p.VMS = p.get_memory_info()
        p.MEMPERCENT = p.get_memory_percent()
        p.CPUPERCENT = p.get_cpu_percent(interval=0)
        p.CPU_USER, p.CPU_SYSTEM = p.get_cpu_times()
        p._READY = True
    return p

def proc_annotate_with_full_info(p):

    with _ignore_AccessDenied():
        p.CREATE_TIMESTAMP = p.create_time
        p.CREATE_TIME = datetime.datetime.fromtimestamp(p.CREATE_TIMESTAMP)
        p.NOW = datetime.datetime.now()

    with _ignore_AccessDenied():
        p.CPUPERCENT = p.get_cpu_percent(interval=1)

    with _ignore_AccessDenied():
        p.IO_COUNTERS = p.get_io_counters()

    with _ignore_AccessDenied():
        p.THREADS = p.get_threads()

    with _ignore_AccessDenied():
        p.OPEN_FILES = p.get_open_files()

    with _ignore_AccessDenied():
        p.CONNECTIONS = p.get_connections()

def get_top_info():
    processes = psutil.get_process_list()

    for p in processes:
        try:
            proc_annotate_with_short_info(p)
        except psutil.NoSuchProcess:
            processes.remove(p)

    return processes