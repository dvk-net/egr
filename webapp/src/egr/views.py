import datetime
from datetime import timedelta
from django.views.generic import TemplateView
from . import utils

one_day_delta = datetime.timedelta(days=1)
class Home(TemplateView):
    template_name="egr/home.html"
    
class Result(TemplateView):
    template_name="egr/result.html"

    def get_context_data(self, **kwargs):
        period = self.request.GET.get('period', 1)
        try:
            period = int(period)
        except:
            period = 1
        if period not in [1, 2]:
            period = 1
        print(period) 
        if period == 1:
            yesterday = datetime.datetime.now().date() - one_day_delta
            start_date = yesterday
            stop_date = yesterday
        else:
            prev_week_day = datetime.datetime.now().date() - timedelta(days=7)
            start_date = prev_week_day - timedelta(days=prev_week_day.weekday())
            stop_date = prev_week_day + timedelta(days=6)

        print(start_date, stop_date)
        a_list = utils.data_combiner(start_date, stop_date)
        # a_list = [
        #     {
        #     'ngrn': 1,
        #     'vnuzp': 3,
        #     'vnaim': 4,
        #     'vtels': 5,
        # },
        # {
        #     'ngrn': 2,
        #     'vnuzp': 6,
        #     'vnaim':7,
        #     'vtels': 8,
        # }
        # ]
        context = super().get_context_data(**kwargs)
        context['a_list'] = a_list
        context['start_date'] = start_date
        context['stop_date'] = stop_date
        return context


