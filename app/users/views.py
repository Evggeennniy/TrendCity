from django.views.generic import TemplateView
from catalog.views import PanelView
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.contrib.auth import logout as auth_logout
from django.views.decorators.csrf import csrf_protect
from catalog import models as catalog_models


class FavoriteView(PanelView, TemplateView):
    template_name = "favorite.html"


class BasketView(PanelView, TemplateView):
    template_name = "basket.html"


User = get_user_model()


@csrf_protect
def register(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone_code = request.POST.get('phone_code')
        phone_number = request.POST.get('phone_number')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Ел. пошта вже використовується.')
            request.session['regerror'] = True  # Установка ошибки
            return redirect(request.path_info)

        # Создание нового пользователя
        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        user.save()
        auth_login(request, user)
        messages.success(request, 'Реєстрація пройшла успішно.')
        request.session['regerror'] = False  # Сброс ошибки (если необходимо оставить флаг False)

        # Очистка значения после его использования
        if 'regerror' in request.session:
            del request.session['regerror']  # Удаление ключа из сессии

        return redirect(request.path_info)  # Перенаправление после успешной регистрации
    else:
        return redirect('index')  # Регистрация обрабатывается только через POST


@csrf_protect
def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)

        if user is not None:
            auth_login(request, user)
            messages.success(request, 'Ви успішно увійшли.')
            request.session['logerror'] = False  # Сброс ошибки (если необходимо оставить флаг False)
        else:
            messages.error(request, 'Невірна ел. пошта або пароль.')
            request.session['logerror'] = True  # Установка ошибки

        # Очистка значения после его использования
        if 'logerror' in request.session:
            del request.session['logerror']  # Удаление ключа из сессии

        return redirect(request.path_info)  # Перезагрузка текущей страницы
    else:
        return redirect('index')  # Логин обрабатывается только через POST


@csrf_protect
def logout(request):
    auth_logout(request)
    return redirect('index')
