import uuid

from django.contrib.auth import get_user_model
from django.db import models

from auth_app.models import CustomUser

User = get_user_model()


class Queue(models.Model):
    name = models.CharField(max_length=255)
    keyword = models.SlugField(unique=True, default=uuid.uuid4, editable=False)
    is_private = models.BooleanField(default=False)
    password = models.CharField(max_length=128, blank=True, null=True)

    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='owned_queues')
    participants = models.ManyToManyField(User, through='QueueMembership', related_name='queues')

    current_index = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    closed_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"Очередь '{self.name}' / {self.owner.first_name} {self.owner.last_name}"

    def move_point(self):
        total = self.participants.count()
        if total == 0:
            return None
        self.current_index = (self.current_index + 1) % total
        self.save()
        return self.get_current_participant()

    def get_current_participant(self):
        participants = list(self.participants.all().order_by('queuemembership__joined_at'))
        if not participants:
            return None
        return participants[self.current_index]

    def clear_queue(self):
        self.participants.clear()
        self.current_index = 0
        self.save()


class QueueMembership(models.Model):
    queue = models.ForeignKey(Queue, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('queue', 'user')
        ordering = ['joined_at']

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} в очереди '{self.queue.name}'"
