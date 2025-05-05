from django.urls import path

from . import views

app_name = "auth"
urlpatterns = [
    path('', views.index, name='index'),
    path("sign-in/", views.sign_in_view, name="sign-in"),
    path("sign-in/processing/", views.sign_in_processing_view, name="sign-in-processing"),
    path("sign-up/", views.sign_up_view, name="sign-up"),
    path("sign-up/processing", views.sign_up_processing_view, name="sign-up-processing"),
    path("sign-out/", views.sign_out_view, name="sign-out"),
]
