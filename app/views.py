from unittest import loader
from django.shortcuts import render, redirect
from django.views import View
from calendar import monthrange
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import login, logout, authenticate
from app.models import CustomUser, Goal
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from .forms import AdminLoginForm, AphorismForm, GoalForm, BS4ScheduleForm
import datetime
from datetime import datetime, date, timedelta
from django.views import generic
from django.views.generic import ListView
from . import mixins
from django.utils import timezone
import calendar
from .models import AdminUser, Aphorism, Collection, Schedule
import io
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import base64
from app.models import Goal
import calendar


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
            return HttpResponseRedirect('/mycalendar/2024/9/')
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
    selectday = timezone.datetime(year, month, day).date()
    filter_goal = Goal.objects.filter(created_at__date=selectday).first()

    if filter_goal:
        context = {'filter_goal': filter_goal}
        return render(request, "app/input_goal.html", context)
    else:
        message = "{}に目標が設定されていません。".format(selectday.strftime("%Y/%m/%d"))
        
        # 現在の年と月を取得してコンテキストに追加
        current_year = timezone.now().year
        current_month = timezone.now().month
        
        return render(request, "app/input_goal_error.html", {
            "message": message,
            "current_year": current_year,
            "current_month": current_month,
        })
         
class MyCalendar(mixins.BaseCalendarMixin, mixins.WeekWithScheduleMixin, generic.CreateView):
    template_name = 'app/mycalendar.html'
    model = Schedule
    date_field = 'date'
    form_class = BS4ScheduleForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        week_calendar_context = self.get_week_calendar()
        month_calendar_context = self.get_month_calendar()

        # year と month をコンテキストに追加
        context['year'] = self.kwargs.get('year', timezone.now().year)
        context['month'] = self.kwargs.get('month', timezone.now().month)
        context['day'] = self.kwargs.get('day', timezone.now().day)

        # detail_dayからfilter_goalを取得
        selectday = date(context['year'], context['month'], context['day'])
        filter_goal = Goal.objects.filter(created_at__date=selectday).first()
        context['filter_goal'] = filter_goal

        context.update(week_calendar_context)
        context.update(month_calendar_context)
        return context    

    def form_valid(self, form):
        month = self.kwargs.get('month')
        year = self.kwargs.get('year')
        day = self.kwargs.get('day')
        
        if month and year and day:
            date_obj = date(year=int(year), month=int(month), day=int(day))  # 修正
        else:
            date_obj = date.today()

        schedule = form.save(commit=False)
        schedule.date = date_obj  # 修正
        schedule.save()

        return redirect('app:mycalendar', year=date_obj.year, month=date_obj.month)

    def get_month_calendar(self):
        """月間カレンダーを取得するメソッド"""
        year = self.kwargs.get('year', date.today().year)
        month = self.kwargs.get('month', date.today().month)

        # 月の最初の日と最後の日を取得
        first_day = date(year, month, 1)
        last_day = (first_day + timedelta(days=31)).replace(day=1) - timedelta(days=1)
        
        # 月の初めの日から最後の日までのすべての日を取得
        month_days = []
        week = []
        
        # カレンダーを埋めるための空のセルを追加
        for _ in range(first_day.weekday()):
            week.append(0)  # 空白のセル

        for day in range(1, last_day.day + 1):
            week.append(day)
            if len(week) == 7:  # 1週間分のセルが埋まったら
                month_days.append(week)
                week = []  # 新しい週を開始

        # 月が終了した後の空白セルを追加
        while len(week) < 7:
            week.append(0)  # 空白のセル

        if week:  # もし残りの週があれば追加
            month_days.append(week)

        # スケジュールデータを取得
        month_schedule_data = self.get_schedules_for_month(year, month)

        return {
            'month_days': month_days,
            'month_schedule_data': month_schedule_data,
        }

    def get_schedules_for_month(self, year, month):
        """指定した月のスケジュールを取得する（ダミー関数）"""
        # 実際のスケジュールデータを取得する処理を実装
        return {date(year, month, day): [] for day in range(1, calendar.monthrange(year, month)[1] + 1)}

class MyCalendar(View):
    def get(self, request, year, month):
        # 月の日数を取得
        num_days = monthrange(year, month)[1]
        
        # カレンダーの構造を作成
        month_days = []
        week = []
        for day in range(1, num_days + 1):
            week.append(day)
            if len(week) == 7:  # 1週間分の配列が揃ったら
                month_days.append(week)
                week = []
        if week:  # 残りの曜日を追加
            month_days.append(week)

        # 前月と次月の情報
        previous_month = month - 1 if month > 1 else 12
        previous_year = year if month > 1 else year - 1
        next_month = month + 1 if month < 12 else 1
        next_year = year if month < 12 else year + 1

        context = {
            'year': year,
            'month': month,
            'month_days': month_days,
            'previous_year': previous_year,
            'previous_month': previous_month,
            'next_year': next_year,
            'next_month': next_month,
        }
        return render(request, 'app/mycalendar.html', context)


class MyCalendarWithDate(View):
    def get(self, request, year, month, day):
        goal = Goal.objects.filter(user=request.user, created_at__year=year, created_at__month=month, created_at__day=day).first()
        goal_form = GoalForm(instance=goal) if goal else GoalForm()

        context = {
            'year': year,
            'month': month,
            'day': day,
            'goal': goal,
            'goal_form': goal_form,
        }
        return render(request, 'app/mycalendar_with_date.html', context)

    def post(self, request, year, month, day):
        goal = Goal.objects.filter(user=request.user, created_at__year=year, created_at__month=month, created_at__day=day).first()

        # 新規目標のフォームを作成
        if goal:
            form = GoalForm(request.POST, instance=goal)  # 既存の目標を更新
        else:
            form = GoalForm(request.POST)  # 新しい目標のフォームを作成

        if form.is_valid():
            # 既存の目標を更新または新しい目標を作成
            goal = form.save(commit=False)
            goal.user = request.user
            if not goal.created_at:
                goal.created_at = timezone.now()  # 新しい場合は日時を設定
            goal.save()
            return redirect('app:mycalendar', year=year, month=month)

        # バリデーションエラーがある場合、再度フォームを表示
        context = {
            'year': year,
            'month': month,
            'day': day,
            'goal': goal,
            'goal_form': form,
        }
        return render(request, 'app/mycalendar_with_date.html', context)

def create_graph(x_list, y_list):
    plt.cla()
    plt.plot(y_list, x_list, label="モチベーション")
    plt.ylim(0, 10)  # y軸の範囲を0から100に固定
    plt.yticks(range(0, 11, 1))  # 0から10まで1刻みで目盛りを表示
    plt.xlabel('日付')
    plt.ylabel('モチベーション')
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
def plot(request, year, month):
    # 現在ログインしているユーザーの目標を取得し、作成日順にソート
    goals = Goal.objects.filter(user=request.user, created_at__year=year, created_at__month=month).order_by('created_at')

    # 達成度と日付のリストを作成
    x_list = [goal.motivation for goal in goals]
    y_list = [goal.created_at.strftime('%m/%d') for goal in goals]  # 日付をフォーマット

    # グラフを作成
    create_graph(x_list, y_list)
    graph = get_image()

    # 現在の月
    current_date = datetime(year, month, 1)

    # 先月と次月の計算
    previous_month = current_date - timedelta(days=1)
    next_month = current_date + timedelta(days=calendar.monthrange(year, month)[1])

    # テンプレートに渡すコンテキスト
    context = {
        'graph': graph,
        'year': year,
        'month': month,
        'previous_year': previous_month.year,
        'previous_month': previous_month.month,
        'next_year': next_month.year,
        'next_month': next_month.month,
    }

    return render(request, 'app/plot.html', context)

class ViewCollectionList(ListView):
    model = Collection
    template_name = 'collection_list.html'  # テンプレート名
    context_object_name = 'collections'  # テンプレート内で使うオブジェクト名

    def get_queryset(self):
        # ユーザーのコレクションを取得
        queryset = Collection.objects.filter(user=self.request.user)

        # フィルタリング条件を取得
        author = self.request.GET.get('author')
        acquision_date = self.request.GET.get('acquision_date')
        rarity = self.request.GET.get('rarity')

        # 各フィールドが指定されていた場合、絞り込みを適用
        if author:
            queryset = queryset.filter(author__icontains=author)
        if acquision_date:
            queryset = queryset.filter(acquision_date__date=acquision_date)
        if rarity:
            queryset = queryset.filter(rarity=rarity)

        return queryset.order_by('rarity')

def admin_login(request):
    if request.method == 'POST':
        form = AdminLoginForm(request.POST)
        if form.is_valid():
            adminname = form.cleaned_data.get('adminname')
            passAphorism = form.cleaned_data.get('password')
            
            # AdminUserを探す
            try:
                admin_user = AdminUser.objects.get(adminname=adminname)
                
                # パスワードが一致するか確認
                if check_password(passAphorism, admin_user.password):
                    request.session['admin_user_id'] = admin_user.id  # セッションにログイン情報を保存
                    messages.success(request, 'ログインに成功しました！')
                    return redirect('app:admin_dashboard')  # ダッシュボードにリダイレクト
                else:
                    messages.error(request, 'パスワードが間違っています。')
            except AdminUser.DoesNotExist:
                messages.error(request, '管理者ユーザーが見つかりません。')
    else:
        form = AdminLoginForm()
    
    return render(request, 'admin_login.html', {'form': form})



@login_required
def admin_logout(request):
    logout(request)
    messages.success(request, 'ログアウトしました。')
    return redirect('app:admin_login')  # ログアウト後にログインページにリダイレクト



@login_required
def admin_dashboard(request):
    aphorisms = Aphorism.objects.all()
    if request.method == 'POST':
        form = AphorismForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('app:admin_dashboard')  # 適切なURLにリダイレクト
    else:
        form = AphorismForm()

    return render(request, 'admin_dashboard.html', {'form': form, 'aphorisms': aphorisms})
from django.shortcuts import get_object_or_404

@login_required
def edit_aphorism(request, pk):
    aphorism = get_object_or_404(Aphorism, pk=pk)
    if request.method == 'POST':
        form = AphorismForm(request.POST, request.FILES, instance=aphorism)
        if form.is_valid():
            form.save()
            messages.success(request, '名言が更新されました！')
            return redirect('app:admin_dashboard')
    else:
        form = AphorismForm(instance=aphorism)

    return render(request, 'edit_aphorism.html', {'form': form})


@login_required
def delete_aphorism(request, pk):
    aphorism = get_object_or_404(Aphorism, pk=pk)
    if request.method == 'POST':
        aphorism.delete()
        messages.success(request, '名言が削除されました！')
        return redirect('app:admin_dashboard')
    
    return render(request, 'confirm_delete.html', {'aphorism': aphorism})