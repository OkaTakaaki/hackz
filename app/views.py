from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password  # パスワード検証用
from .forms import AdminLoginForm
from .models import AdminUser
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import AphorismForm
from .models import Aphorism
from django.contrib.auth import logout


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
