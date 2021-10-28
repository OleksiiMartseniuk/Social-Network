import json
from django.core import paginator
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .forms import ImageCreateForm
from .models import Image


@login_required
def image_create(request):
    """Добавления картинки """
    if request.method == 'POST':
        # Форма отправлена
        form = ImageCreateForm(data=request.POST)
        if form.is_valid():
            cd = form.cleaned_data

            new_item = form.save(commit=False)
            # Добавляем пользователя к созданному объекту.
            new_item.user = request.user
            new_item.save()
            messages.success(request, 'Image added successfully')
            # Перенаправляем пользователя на страницу сохраненного изображения.
            return redirect(new_item.get_absolute_url())
    else:
        # Заполняем форму данными из GET-запроса
        form = ImageCreateForm(data=request.GET)
    context = {
        'section': 'images',
        'form': form
    }
    return render(request, 'images/image/create.html', context)


def image_detail(request, id, slug):
    image = get_object_or_404(Image, id=id, slug=slug)
    context = {
        'section': 'images',
        'image': image
    }
    return render(request, 'images/image/detail.html', context)


@login_required
@require_POST
def image_like(request):
    """like """
    data = json.loads(request.body.decode("utf-8"))
    image_id = data['id']
    action = data['action']

    if image_id and action:
        try:
            image = Image.objects.get(id=image_id)
            if action == 'like':
                image.user_like.add(request.user)
            else:
                image.user_like.remove(request.user)
            return JsonResponse({'status': 'ok'})
        except:
            return JsonResponse({'status': 'error'})
    return JsonResponse({'status': 'not'})


@login_required
def image_list(request):
    """Динамический список изображений"""
    images = Image.objects.all()
    paginator = Paginator(images, 8)
    page = request.GET.get('page')
    try:
        images = paginator.page(page)
    except PageNotAnInteger:
        # Если переданная страница не является числом, возвращаем первую.
        images = paginator.page(1)
    except EmptyPage:
        if request.is_ajax():
            # Если получили AJAX-запрос с номером страницы, большим, чем их количество,
            # возвращаем пустую страницу.
            return HttpResponse('')
        # Если номер страницы больше, чем их количество, возвращаем последнюю.
        images = paginator.page(paginator.num_pages)
    context = {
        'section': 'images',
        'images': images
    }    
    if request.is_ajax():
        return render(request, 'images/image/list_ajax.html', context)        
    return render(request, 'images/image/list.html', context)    