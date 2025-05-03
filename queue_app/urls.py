from django.urls import path

from . import views

app_name = "queue"
urlpatterns = [
    path("", views.index, name="index"),
    path("queue/<int:queue_id>/", views.queue_page_view, name="queue_page"),
    path("queue/create/", views.queue_create_view, name="queue_create"),
]