from django.shortcuts import render
import datetime
from django.shortcuts import redirect
from django.views import generic
from . import mixins
from .forms import BS4ScheduleForm
import calendar
from .models import Schedule

class MyCalendar(mixins.BaseCalendarMixin, mixins.WeekWithScheduleMixin, generic.CreateView):
    """月間カレンダー、週間カレンダー、スケジュール登録画面のある欲張りビュー"""
    template_name = 'app/mycalendar.html'
    model = Schedule
    date_field = 'date'
    form_class = BS4ScheduleForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        week_calendar_context = self.get_week_calendar()
        month_calendar_context = self.get_month_calendar()

        # year と month をコンテキストに追加
        context['year'] = self.kwargs.get('year', datetime.date.today().year)
        context['month'] = self.kwargs.get('month', datetime.date.today().month)

        context.update(week_calendar_context)
        context.update(month_calendar_context)
        return context


    def form_valid(self, form):
        month = self.kwargs.get('month')
        year = self.kwargs.get('year')
        day = self.kwargs.get('day')
        if month and year and day:
            date = datetime.date(year=int(year), month=int(month), day=int(day))
        else:
            date = datetime.date.today()
        schedule = form.save(commit=False)
        schedule.date = date
        schedule.save()
        return redirect('app:mycalendar', year=date.year, month=date.month, day=date.day)

    def get_month_calendar(self):
        """月間カレンダーを取得するメソッド"""
        today = datetime.date.today()
        month_days = calendar.monthcalendar(today.year, today.month)

        # 各日のスケジュールを取得する処理を追加することができます
        month_schedule_data = self.get_schedules_for_month(today.year, today.month)

        return {
            'month_days': month_days,
            'month_schedule_data': month_schedule_data,
        }

    def get_schedules_for_month(self, year, month):
        """指定した月のスケジュールを取得する（ダミー関数）"""
        # 実際のスケジュールデータを取得する処理を実装
        return {}