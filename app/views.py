from unittest import loader
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import login, logout, authenticate
from app.models import CustomUser
from django.views.generic import ListView
from .models import Collection
from django.shortcuts import render, redirect
from django.views.generic import CreateView
from .forms import CollectionForm
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth.hashers import check_password  # パスワード検証用
from .forms import AdminLoginForm
from .models import AdminUser
from .forms import AphorismForm
from .models import Aphorism


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
@login_required
def signout(request):
    logout(request)
    messages.success(request, 'ログアウトしました')
    return HttpResponseRedirect('/')

def home(request):
    template = loader.get_template("app/home.html")
    return HttpResponse(template.render({}, request))



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
