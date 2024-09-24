from unittest import loader
from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import login, logout, authenticate
from app.models import CustomUser, Goal
from django.contrib.auth.decorators import login_required
from .forms import GoalForm
import datetime
from django.views import generic
from . import mixins
from .forms import BS4ScheduleForm
import calendar
from .models import Schedule

def index(request):
    context = {'user': request.user}
    return render(request, 'index.html', context)

def signup(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        new_user = CustomUser(first_name=first_name, last_name=last_name, username=username, email=email)
        new_user.set_password(password)  # パスワードのハッシュ化
        new_user.save()
        
        # signup_success.htmlでアラートを表示し、リダイレクトさせる
        return render(request, 'signup_success.html', {'message': 'ユーザーの作成に成功しました'})
    else:
        return render(request, 'signup.html')

def signin(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return render(request, 'signin.html', {'error_message': 'ユーザーが存在しません。'})

        user = authenticate(request, username=user.username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/home')
        else:
            return render(request, 'signin.html', {'error_message': 'パスワードが正しくありません。'})
    else:
        return render(request, 'signin.html')

def signout(request):
    logout(request)
    return HttpResponseRedirect('/')

def home(request):
    goals = Goal.objects.all()
    context = {'goals': goals}
    return render(request, "app/home.html", context)
    # template = loader.get_template("app/home.html")
    # return HttpResponse(template.render({}, request))

@login_required  # ログインが必要
def goal(request):
    if request.method == 'POST':
        form = GoalForm(request.POST)
        if form.is_valid():
            goal = form.save(commit=False)  # フォームからオブジェクトを作成するが、まだ保存しない
            goal.user = request.user  # 現在ログインしているユーザーをセット
            goal.save()  # データベースに保存
            return HttpResponseRedirect('/home')
    else:
        form = GoalForm()  # 空のフォームを表示

    return render(request, 'app/goal.html', {'form': form})

def detail_day(request, year, month, day):
    goal_all = Goal.objects.all()
    selectday = str(year) + "-" + str(month) + "-" + str(day)
    try:
        filter_goal = Goal.objects.get(created_at__date=selectday)
    except:
        filter_goal = None

    context = {'filter_goal': filter_goal}
    print("-------------------------" , goal_all[0].created_at.day , "-------------------------")
    print("filter-------------------------" , filter_goal , "-------------------------")
    return render(request, "app/input_goal.html", context)

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
        context['day'] = self.kwargs.get('day', datetime.date.today().day)
        print("###############", context['day'], "###############")
        detail_day(self.request, context['year'], context['month'], context['day'])

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
        month_schedule_data = self.get_schedules_for_month(today.year, today.month, today.day)

        return {
            'month_days': month_days,
            'month_schedule_data': month_schedule_data,
        }

    def get_schedules_for_month(self, year, month, day):
        """指定した月のスケジュールを取得する（ダミー関数）"""
        # 実際のスケジュールデータを取得する処理を実装
        goal_all = Goal.objects.all()
        today = datetime.date.today()
        filter_goal = Goal.objects.get(created_at__date=today)
        print("-------------------------" , day , "-------------------------")
        print("-------------------------" , goal_all[0].created_at.day , "-------------------------")
        print("filter-------------------------" , filter_goal , "-------------------------")
        return{}
    
    