from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from .forms import UserRegistrationForm, UserUpdateForm, ProfileUpdateForm, CustomAuthenticationForm

def register(request):
    """Регистрация нового пользователя"""
    if request.user.is_authenticated:
        messages.info(request, 'Вы уже авторизованы.')
        return redirect('main:home')
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save(commit=False)
                user.set_password(form.cleaned_data['password1'])
                user.save()
                
                # Автоматически входим в систему
                login(request, user)
                messages.success(request, f'Добро пожаловать, {user.username}! Регистрация прошла успешно.')
                return redirect('main:home')
            except IntegrityError:
                messages.error(request, 'Пользователь с таким именем уже существует.')
            except Exception as e:
                messages.error(request, 'Произошла ошибка при регистрации. Попробуйте еще раз.')
        else:
            # Показываем конкретные ошибки
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{form.fields[field].label}: {error}')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'auth_app/register.html', {'form': form})

def user_login(request):
    """Вход в систему"""
    if request.user.is_authenticated:
        messages.info(request, 'Вы уже авторизованы.')
        return redirect('main:home')
    
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            
            if user is not None:
                if user.is_active:
                    login(request, user)
                    messages.success(request, f'Добро пожаловать, {username}!')
                    
                    # Перенаправляем на страницу, с которой пришел пользователь
                    next_url = request.GET.get('next')
                    if next_url and next_url.startswith('/'):
                        return redirect(next_url)
                    return redirect('main:home')
                else:
                    messages.error(request, 'Ваш аккаунт заблокирован.')
            else:
                messages.error(request, 'Неверное имя пользователя или пароль.')
        else:
            messages.error(request, 'Неверное имя пользователя или пароль.')
    else:
        form = CustomAuthenticationForm()
    
    return render(request, 'auth_app/login.html', {'form': form})

@login_required
def profile(request):
    """Профиль пользователя"""
    try:
        if request.method == 'POST':
            u_form = UserUpdateForm(request.POST, instance=request.user)
            p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
            
            if u_form.is_valid() and p_form.is_valid():
                try:
                    u_form.save()
                    p_form.save()
                    messages.success(request, 'Профиль успешно обновлен!')
                    return redirect('auth:profile')
                except IntegrityError:
                    messages.error(request, 'Пользователь с таким именем уже существует.')
                except Exception as e:
                    messages.error(request, 'Произошла ошибка при обновлении профиля.')
            else:
                # Показываем ошибки форм
                for field, errors in u_form.errors.items():
                    for error in errors:
                        messages.error(request, f'{u_form.fields[field].label}: {error}')
                
                for field, errors in p_form.errors.items():
                    for error in errors:
                        messages.error(request, f'{p_form.fields[field].label}: {error}')
        else:
            u_form = UserUpdateForm(instance=request.user)
            p_form = ProfileUpdateForm(instance=request.user.profile)
        
        context = {
            'u_form': u_form,
            'p_form': p_form
        }
        
        return render(request, 'auth_app/profile.html', context)
    except Exception as e:
        messages.error(request, 'Произошла ошибка при загрузке профиля.')
        return redirect('main:home')

def user_logout(request):
    """Выход из системы"""
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, 'Вы успешно вышли из системы.')
    else:
        messages.info(request, 'Вы не были авторизованы.')
    
    return redirect('main:home')


