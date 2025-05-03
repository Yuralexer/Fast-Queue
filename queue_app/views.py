from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

# from django.shortcuts import render, redirect


@login_required(login_url="auth:sign-in")
def index(request):
    return HttpResponse("Вы авторизовались! Ура!")


@login_required(login_url="auth:sign-in")
def queue_page_view(request):
    return HttpResponse("Страница очереди")


@login_required(login_url="auth:sign-in")
def queue_create_view(request):
    return HttpResponse("Страница создания очереди")
