from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, get_user_model, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages

from website_shop.settings import LOGIN_REDIRECT_URL
from .forms import UserRegistrationForm, ChangePasswordForm, UserProfileForm

User = get_user_model()


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            context = {
                'title': 'Успешная регистрация',
                'new_user': new_user,
            }
            return render(request, template_name='users/register_done.html', context=context)
    user_form = UserRegistrationForm()
    context = {
        'register_form': user_form,
        'current_page': 'users:register',
    }
    return render(request, template_name='users/register.html', context=context)


def log_in(request):
    form = AuthenticationForm(request, request.POST)
    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            url = request.GET.get('next', LOGIN_REDIRECT_URL)
            return redirect(url)
    context = {'form': form, 'current_page': 'users:login'}
    return render(request, template_name='users/login.html', context=context)


@login_required
def log_out(request):
    logout(request)
    return redirect('shop:products')

@login_required
def user_detail(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.user != user:
        raise PermissionDenied()
    context = {
        'user': user,
        'title': 'Информация о профиле',
    }
    return render(request, template_name='users/profile.html', context=context)


@login_required
def change_password(request):
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            old_password = form.cleaned_data['old_password']
            new_password = form.cleaned_data['new_password']

            # Проверка правильности старого пароля
            if not request.user.check_password(old_password):
                form.add_error('old_password', 'Старый пароль неверен.')
            else:
                # Изменение пароля
                request.user.set_password(new_password)
                request.user.save()
                update_session_auth_hash(request, request.user)  # Сохраняем сессию пользователя
                messages.success(request, 'Пароль успешно изменен.')
                return redirect('some_view')  # Замените на нужный вам URL

    else:
        form = ChangePasswordForm()

    return render(request, 'users/change_password.html', {'form': form})


@login_required
def change_profile(request):
    user = request.user
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user)
        if form.is_valid():
            user = form.save(commit=False)
            form.save()
            context = {
                'user': user,
                'title': 'Успешное изменение профиля',
            }
            return render(request, template_name='users/change_done.html', context=context)
    else:
        form = UserProfileForm(instance=user)

    context = {
        'form': form,
        'title': 'Изменение профиля',
    }

    return render(request, 'users/change_profile.html', context=context)