import json
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from . import forms
from .models import Profile, Contact
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from actions.utils import create_action
from actions.models import Action


@login_required
def dashboard(request):
    # По умолчанию отображаем все действия.
    actions = Action.objects.exclude(user=request.user)
    following_ids = request.user.following.values_list('id', flat=True)
    if following_ids:
        # Если текущий пользователь подписался на кого-то,
        # отображаем только действия этих пользователей.
        actions = actions.filter(user_id__in=following_ids)
    actions = actions.select_related('user', 'user__profile').prefetch_related('target')[:10]
    context = {
        'section': 'dashboard',
        'actions': actions
    }
    return render(request, 'account/dashboard.html', context)


def register(request):
    """Регистрация пользователя"""
    if request.method == 'POST':
        user_form = forms.UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Создаем нового пользователя, но пока не сохраняем в базу данных
            new_user = user_form.save(commit=False)
            # Задаем пользователю зашифрованный пароль.
            new_user.set_password(user_form.cleaned_data['password'])
            # Сохраняем пользователя в базе данных.
            new_user.save()
            # Создание профиля пользователя.
            Profile.objects.create(user=new_user)
            create_action(new_user, 'has created an account')
            return render(request, 'account/register_done.html', {'new_user': new_user})
    else:
        user_form = forms.UserRegistrationForm()
    return render(request, 'account/register.html', {'user_form': user_form})


@login_required
def edit(request):
    """Редактирования Profile, User"""
    if request.method == 'POST':
        user_form = forms.UserEditForm(instance=request.user, data=request.POST)
        profile_form = forms.ProfileEditForm(instance=request.user.profile,
                                             data=request.POST,
                                             files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request, 'Error updating your profile')
    else:
        user_form = forms.UserEditForm(instance=request.user)
        profile_form = forms.ProfileEditForm(instance=request.user.profile)
    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    return render(request, 'account/edit.html', context)


@login_required
def user_list(request):
    # Получает список всех активных пользователей
    users = User.objects.filter(is_active=True)
    context = {
        'section': 'people',
        'users': users
    }
    return render(request, 'account/user/list.html', context)


@login_required
def user_detail(request, username):
    # Получения активного пользователя по его логину
    user = get_object_or_404(User, username=username, is_active=True)
    context = {
        'section': 'people',
        'user': user
    }
    return render(request, 'account/user/detail.html', context)


@require_POST
@login_required
def user_follow(request):
    data = json.loads(request.body.decode("utf-8"))
    user_id = data['id']
    action = data['action']
    if user_id and action:
        try:
            user = User.objects.get(id=user_id)
            if action == 'follow':
                Contact.objects.get_or_create(user_from=request.user, user_to=user)
                create_action(request.user, 'is following', user)
            else:
                Contact.objects.filter(user_from=request.user, user_to=user).delete()    
            return JsonResponse({'status': 'ok'})
        except User.DoesNotExist:
            return JsonResponse({'status': 'error_user'})       
    return JsonResponse({'status':'error_null'})         