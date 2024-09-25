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