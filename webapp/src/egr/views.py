import datetime
from datetime import timedelta
from django.views.generic import TemplateView

from . import utils, forms

one_day_delta = datetime.timedelta(days=1)


class Home(TemplateView):
    template_name = "egr/home.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["date_form"] = forms.EgrDateSelectForm()
        return context
    

class Result(TemplateView):
    template_name = "egr/result.html"

    def get_context_data(self, **kwargs):
        period = self.request.GET.get("period", 1)
        date = self.request.GET.get("date")
        start_date = None
        stop_date = None
        if date:
            try:
                start_date = datetime.datetime.strptime(date, "%d.%m.%Y").date()
                stop_date = start_date
            except:
                pass

        elif period:

            try:
                period = int(period)
            except:
                period = 1
            if period not in [1, 2]:
                period = 1
            if period == 1:
                yesterday = datetime.datetime.now().date() - one_day_delta
                start_date = yesterday
                stop_date = yesterday
        if not start_date and not stop_date:
            prev_week_day = datetime.datetime.now().date() - timedelta(days=7)
            start_date = prev_week_day - timedelta(days=prev_week_day.weekday())
            stop_date = prev_week_day + timedelta(days=6)
        # a_list = []
        a_list = utils.data_combiner(start_date, stop_date)
        context = super().get_context_data(**kwargs)
        context["a_list"] = a_list
        context["start_date"] = start_date
        context["stop_date"] = stop_date
        context["date_form"] = forms.EgrDateSelectForm()
        return context
