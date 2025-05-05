import uuid

from django.contrib.auth import get_user_model
from django.db import models

from auth_app.models import CustomUser

User = get_user_model()


class Queue(models.Model):
    name = models.CharField(max_length=255)
    keyword = models.SlugField(unique=True, default=uuid.uuid4, editable=False)
    password = models.CharField(max_length=128, blank=True, null=True)

    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='owned_queues')
    participants = models.ManyToManyField(User, through='QueueParticipant', related_name='queues')

    current_index = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    closed_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.name

    def add_user_to_queue(self, user):
        """Добавить пользователя в конец очереди"""
        last_position = QueueParticipant.objects.filter(queue=self).count()
        QueueParticipant.objects.create(queue=self, user=user, position=last_position + 1)

    def find_user_in_queue(self, user):
        """Найти id пользователя в очререди"""
        if QueueParticipant.objects.filter(queue=self, user=user).exists():
            return QueueParticipant.objects.filter(queue=self, user=user).first().position
        return -1

    def move_point(self):
        """Передвинуть очередь — сдвинуть всех участников"""
        participants = QueueParticipant.objects.filter(queue=self).order_by('position')
        for qp in participants:
            qp.position -= 1
            qp.save()
        QueueParticipant.objects.filter(queue=self, position__lte=0).delete()

    def clear_queue(self):
        """Очистить очередь"""
        QueueParticipant.objects.filter(queue=self).delete()

    def remove_user_from_queue(self, user):
        """Удаляет пользователя из очереди и пересчитывает позиции"""
        participant = QueueParticipant.objects.filter(queue=self, user=user).first()
        if not participant:
            return False

        participant.delete()

        remaining_participants = QueueParticipant.objects.filter(queue=self).order_by('position')
        for index, p in enumerate(remaining_participants, start=1):
            p.position = index
            p.save()

        return True

    def get_ordered_participants(self):
        return QueueParticipant.objects.filter(queue=self).order_by('position')


class QueueParticipant(models.Model):
    queue = models.ForeignKey(Queue, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    position = models.PositiveIntegerField()

    class Meta:
        unique_together = ('queue', 'user')
        ordering = ['position']

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} в {self.queue.name} (#{self.position})"