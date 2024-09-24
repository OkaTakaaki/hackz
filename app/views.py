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
    
from django.shortcuts import render
import io
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import base64
from django.contrib.auth.decorators import login_required
from app.models import Goal
import calendar

def create_graph(x_list, y_list):
    plt.cla()
    plt.plot(y_list, x_list, label="達成度")
    plt.ylim(0, 100)  # y軸の範囲を0から100に固定
    plt.yticks(range(0, 101, 10))  # 0から100まで10刻みで目盛りを表示
    plt.xlabel('日付')
    plt.ylabel('達成度')
    plt.xticks(rotation=45)  # 日付を回転して見やすくする

def get_image():
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()
    return graph

@login_required
def plot(request):
    # 現在ログインしているユーザーの目標を取得し、作成日順にソート
    goals = Goal.objects.filter(user=request.user).order_by('created_at')
    
    # 月ごとにデータをグループ化するための辞書
    monthly_goals = {}
    
    for goal in goals:
        # 年と月ごとにグループ化
        year_month = goal.created_at.strftime('%Y-%m')
        if year_month not in monthly_goals:
            monthly_goals[year_month] = []
        monthly_goals[year_month].append(goal)

    # 各月ごとのグラフを作成
    graphs = {}
    for year_month, goals_in_month in monthly_goals.items():
        # 達成度と日付のリストを作成
        x_list = [goal.achievement for goal in goals_in_month]
        y_list = [goal.created_at.strftime('%m/%d') for goal in goals_in_month]  # 日付をフォーマット

        # グラフを作成
        create_graph(x_list, y_list)
        graph = get_image()

        # 年月ごとにグラフを保存
        graphs[year_month] = graph

    # テンプレートに月ごとのグラフを渡す
    return render(request, 'app/plot.html', {'graphs': graphs})
