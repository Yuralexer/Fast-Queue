from django.urls import path

from . import views

app_name = "queue"
urlpatterns = [
    path("", views.index, name="index"),
    path("queue/create/", views.queue_create_view, name="queue_create"),
    path("queue/<int:queue_id>/password_processing", views.queue_password_processing, name="queue_password_processing"),
    path("queue/<int:queue_id>/", views.queue_page_view, name="queue_page"),
    path("queue/<int:queue_id>/join", views.queue_page_view_join, name="queue_page_join"),
    path("queue/<int:queue_id>/next/", views.queue_page_view_next, name="queue_page_next"),
    path("queue/<int:queue_id>/clear/", views.queue_page_view_clear, name="queue_page_clear"),
    path("queue/<int:queue_id>/delete/", views.queue_page_view_delete, name="queue_page_delete"),
    path("queue/<int:queue_id>/exit/", views.queue_page_view_exit, name="queue_page_exit"),
]
