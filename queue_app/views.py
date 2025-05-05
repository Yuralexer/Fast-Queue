from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .models import Queue, QueueParticipant


@login_required(login_url="auth:sign-in")
def index(request):
    query = request.GET.get('search_request', '')
    if query:
        queues = Queue.objects.filter(keyword__icontains=query)
    else:
        queues = Queue.objects.all()
    return render(
        request,
        'queue_app/queue_search_page.html',
        {
            'user': request.user,
            'queues': queues,
            'search_request': query if query else None,
        })


@login_required(login_url="auth:sign-in")
def queue_create_view(request):
    if request.method == 'POST':
        return queue_create_view_post(request)
    return render(
        request,
        "queue_app/queue_create.html",
        {
            'user': request.user,
        }
    )

def queue_create_view_post(request):
    name = request.POST.get('queue_name')
    keyword = request.POST.get('queue_keyword')
    is_private = request.POST.get('queue_private')
    password = request.POST.get('queue_password')

    if not name or not keyword:
        messages.error(request, "Имя и ключевое слово не могут быть пустыми.")
        return redirect("queue:queue_create")
    if is_private and not password:
        messages.error(request, "Вы указали очередь как приватную, однако не указали пароль.")
        return redirect("queue:queue_create")

    if Queue.objects.filter(keyword=keyword).exists():
        messages.error(request, "Очередь с таким ключевым словом уже есть. Придумайте другое ключевое слово.")
        return redirect("queue:queue_create")

    created_queue = Queue.objects.create(
        name=name,
        keyword=keyword,
        password=password if password else None,
        owner=request.user,
    )

    if not created_queue:
        messages.error(request, "Очередь не была создана.")
        return redirect("queue:queue_create")

    return redirect("queue:queue_page", created_queue.id)

@login_required(login_url="auth:sign-in")
def queue_password_processing(request, queue_id):
    if request.method != 'POST':
        return redirect("queue:index")
    queue = Queue.objects.get(id=queue_id)
    if queue.password != request.POST.get('queue_password'):
        messages.error(request, "Неправильный пароль.")
        return redirect("queue:queue_page_join", queue_id)
    queue.add_user_to_queue(request.user)
    return redirect("queue:queue_page", queue_id)

@login_required(login_url="auth:sign-in")
def queue_page_view_join(request, queue_id):
    queue = Queue.objects.filter(id=queue_id)
    if not queue.exists():
        return render(
            request,
            "queue_app/queue_404.html",
            {
                'user': request.user,
            }
        )
    queue = queue.first()
    if request.user == queue.owner or queue.find_user_in_queue(request.user) != -1:
        return redirect("queue:queue_page", queue_id)
    if queue.password:
        return render(
            request,
            'queue_app/queue_password_enter.html',
            {
                'user': request.user,
                'queue': queue,
            }
        )
    queue.add_user_to_queue(request.user)
    return redirect("queue:queue_page", queue_id)

@login_required(login_url="auth:sign-in")
def queue_page_view(request, queue_id):
    queue = Queue.objects.filter(id=queue_id)
    if not queue.exists():
        return render(
            request,
            "queue_app/queue_404.html",
            {
                'user': request.user,
            }
        )
    queue = queue.first()
    if request.user != queue.owner and queue.find_user_in_queue(request.user) == -1:
        return redirect("queue:index")
    else:
        return render(
            request,
            'queue_app/queue.html',
            {
                'user': request.user,
                'queue': queue,
            }
        )


@login_required(login_url="auth:sign-in")
def queue_page_view_next(request, queue_id):
    queue = Queue.objects.get(id=queue_id)
    if queue is not None and request.user == queue.owner:
        queue.move_point()
    return redirect("queue:queue_page", queue_id)


@login_required(login_url="auth:sign-in")
def queue_page_view_clear(request, queue_id):
    queue = Queue.objects.get(id=queue_id)
    if queue is not None and request.user == queue.owner:
        queue.clear_queue()
    return redirect("queue:queue_page", queue_id)


@login_required(login_url="auth:sign-in")
def queue_page_view_delete(request, queue_id):
    queue = Queue.objects.get(id=queue_id)
    if queue is not None and request.user == queue.owner:
        queue.delete()
    return redirect("queue:index")


@login_required(login_url="auth:sign-in")
def queue_page_view_exit(request, queue_id):
    queue = Queue.objects.filter(id=queue_id).first()
    if queue and queue.find_user_in_queue(request.user) != -1:
        queue.remove_user_from_queue(request.user)
        return redirect("queue:index")
    return redirect("queue:queue_page", queue_id=queue_id)
