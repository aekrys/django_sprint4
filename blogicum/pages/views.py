from django.shortcuts import render
from django.views.generic import TemplateView


class AboutView(TemplateView):
    template_name = 'pages/about.html'


class RulesView(TemplateView):
    template_name = 'pages/rules.html'


def page_not_found(request, exception):
    """
    Кастомный обработчик ошибки 404 (Страница не найдена).

    Args:
        request (HttpRequest): Объект HTTP-запроса.
        exception (Exception): Объект исключения, вызвавший ошибку 404.

    Returns:
        HttpResponse: Рендерит кастомную страницу 404 с соответствующим статусом.
    """
    return render(request, 'pages/404.html', status=404)


def csrf_failure(request, reason=''):
    """
    Кастомный обработчик ошибки CSRF (403 Forbidden).

    Args:
        request (HttpRequest): Объект HTTP-запроса.
        reason (str): Причина ошибки CSRF (по умолчанию пустая строка).

    Returns:
        HttpResponse: Рендерит кастомную страницу 403 CSRF с соответствующим статусом.
    """
    return render(request, 'pages/403csrf.html', status=403)


def server_error(request):
    """
    Кастомный обработчик ошибки 500 (Внутренняя ошибка сервера).

    Args:
        request (HttpRequest): Объект HTTP-запроса.

    Returns:
        HttpResponse: Рендерит кастомную страницу 500 с соответствующим статусом.
    """
    return render(request, 'pages/500.html', status=500)