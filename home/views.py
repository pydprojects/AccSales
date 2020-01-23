from django.shortcuts import render
from django.utils.translation import gettext as _


def e_handler404(request, exception):
    context = {'message': _("По указаной ссылке ничего не найдено.")}
    response = render(request, 'home/404.html', context=context, status=404)
    return response


def e_handler500(request):
    context = {'message': _("Внутренняя ошибка сервера.")}
    response = render(request, 'home/500.html', context=context, status=500)
    return response


def csrf_failure(request, reason=""):
    context = {'message': _("Проверка соответсвия CSRF провалена.")}
    return render(request, 'home/403.html', context=context, status=403)
