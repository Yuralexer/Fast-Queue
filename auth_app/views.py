
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from . import forms

REDIRECT_URL = "http://127.0.0.1:8000/dashboard/"


def index(request):
    if request.user.is_authenticated:
        return redirect(REDIRECT_URL)
    return redirect("auth:sign-in")


def sign_in_view(request):
    if request.user.is_authenticated:
        return redirect(REDIRECT_URL)
    form = forms.SignInForm()
    return render(
        request,
        "auth_app/sign_in.html",
        {
            "form": form,
        })


def sign_in_processing_view(request):
    if request.method == "POST":
        form = forms.SignInForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data["user"]
            login(request, user)
            return redirect(REDIRECT_URL)
        messages.error(request, "Неправильный email или пароль.")
        return redirect("auth:sign-in")
    messages.error(request, "Что-то пошло не так.")
    return redirect("auth:sign-in")


def sign_up_view(request):
    if request.user.is_authenticated:
        return redirect(REDIRECT_URL)
    form = forms.SignUpForm()
    return render(
        request,
        "auth_app/sign_up.html",
        {
            "form": form
        })


def sign_up_processing_view(request):
    if request.method == "POST":
        form = forms.SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.save()
            login(request, user)
            return redirect(REDIRECT_URL)
        else:
            messages.error(request, "Пользователь с таким email уже существует или был введен простой пароль.")
            return redirect("auth:sign-up")
    messages.error(request, "Что-то пошло не так.")
    return redirect("auth:sign-up")


@login_required(login_url="auth:sign-in")
def sign_out_view(request):
    logout(request)
    return redirect("auth:sign-in")
