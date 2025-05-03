from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render

from .models import Queue


@login_required(login_url="auth:sign-in")
def index(request):
    query = request.GET.get('search_request', '')
    if query:
        queues = Queue.objects.filter(keyword__icontains=query)
    else:
        queues = Queue.objects.all()
    return render(
        request,
        'queue_app/queue_search.html',
        {
            'user': request.user,
            'queues': queues,
            'search_request': query if query else None,
        })


@login_required(login_url="auth:sign-in")
def queue_page_view(request, queue_id):
    return render(
        request,
        'queue_app/queue_password_enter.html',
        {
            'queue': Queue.objects.get(pk=queue_id),
        })


@login_required(login_url="auth:sign-in")
def queue_create_view(request):
    return HttpResponse("Страница создания очереди")
