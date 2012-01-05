# -*- coding: utf-8 -*-
from __future__ import absolute_import
from pympler import muppy, summary
from pympler.muppy import get_size
from django import forms
import yappi
from profiling_dashboard.stats import get_top_info
from .stats import get_full_yappi_stats, get_other_yappi_stats

class YappiManageForm(forms.Form):
    ACTIONS = (
        ('start', 'start'),
        ('start_with_builtins', 'start_with_builtins'),
        ('stop', 'stop'),
        ('reset', 'reset'),
    )

    action = forms.ChoiceField(ACTIONS)

    def do_action(self):
        action = self.cleaned_data['action']
        if action == 'start':
            yappi.start()
        elif action == 'start_with_builtins':
            yappi.start(builtins=True)
        elif action == 'stop':
            yappi.stop()
        elif action == 'reset':
            yappi.clear_stats()
        return action


class YappiFilterForm(forms.Form):
    SORT_ORDER = (
        (yappi.SORTORDER_ASCENDING, 'asc'),
        (yappi.SORTORDER_DESCENDING, 'desc'),
    )

    SORT_TYPE = (
        (yappi.SORTTYPE_NAME, 'name of the function being profiled'),
        (yappi.SORTTYPE_NCALL, 'total call count of the function'),
        (yappi.SORTTYPE_TAVG, 'average total time'),
        (yappi.SORTTYPE_TSUB, 'total time spent in the function excluding sub-calls'),
        (yappi.SORTTYPE_TTOTAL, 'total time spent in the function'),
    )

    sort_order = forms.TypedChoiceField(choices=SORT_ORDER, initial=yappi.SORTORDER_DESCENDING, coerce=int, widget=forms.HiddenInput())
    sort_type = forms.TypedChoiceField(choices=SORT_TYPE, initial=yappi.SORTTYPE_TTOTAL, coerce=int, widget=forms.HiddenInput())
    limit = forms.IntegerField(initial=20, help_text='-1 means no limit')

    def get_stats(self):
        try:
            return get_full_yappi_stats(
                sorttype=self.cleaned_data['sort_type'],
                sortorder=self.cleaned_data['sort_order'],
                limit=self.cleaned_data['limit'],
            )
        except Exception as e:
            return ['Stats are not available.\n Reason: %s' % e]

    def get_other_stats(self):
        return get_other_yappi_stats()


class MuppyFilterForm(forms.Form):
    limit = forms.IntegerField(initial=20)
    sort_by = forms.IntegerField(initial=2, widget=forms.HiddenInput())

    def get_report(self):
        all_objects = muppy.get_objects()
        size = get_size(all_objects)
        report = summary.summarize(all_objects)

        sort_index = self.cleaned_data['sort_by']
        limit = self.cleaned_data['limit']

        report.sort(key=lambda item: item[sort_index], reverse=True)
        if limit:
            report = report[:limit]

        return size, report

class TopFilterForm(forms.Form):
    limit = forms.IntegerField(initial=100)
    sort_by = forms.CharField(initial='RSS', widget=forms.HiddenInput())
    only_ready = forms.BooleanField(initial=True, required=False)

    def get_processes(self):
        processes = get_top_info()

        sort_index = self.cleaned_data['sort_by']
        limit = self.cleaned_data['limit']

        if self.cleaned_data['only_ready']:
            processes = filter(lambda proc: proc._READY, processes)

        processes.sort(key = lambda proc: getattr(proc, sort_index, None), reverse=True)
        if limit:
            processes = processes[:limit]

        return processes
