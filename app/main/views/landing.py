from django.shortcuts import render

from app.settings.base import LOGIN_URL


def landing(request):
    return render(request, 'landing.html', {'login_url': LOGIN_URL, })