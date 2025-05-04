from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from .models import Queue, QueueParticipant


class QueueTest(TestCase):
    def setUp(self):
        self.first_auth_user = get_user_model().objects.create_user(
            first_name='first',
            last_name='user',
            email='test@example.com',
        )
        self.first_auth_user.set_password('test')
        self.first_auth_user.save()

        self.second_auth_user = get_user_model().objects.create_user(
            first_name='second',
            last_name='user',
            email='test2@example.com',
        )
        self.second_auth_user.set_password('test')
        self.second_auth_user.save()

        self.client1 = Client()
        self.client1.login(email=self.first_auth_user.email, password='test')
        self.client2 = Client()
        self.client2.login(email=self.second_auth_user.email, password='test')
        self.bad_client = Client()

        self.public_queue = Queue.objects.create(
            name='test queue',
            keyword="test",
            password=None,
            owner=self.first_auth_user,
        )
        self.private_queue = Queue.objects.create(
            name='second test queue',
            keyword="test2",
            password="test",
            owner=self.first_auth_user,
        )

    def test_deny_access_for_non_auth_client(self):
        response = self.bad_client.get(reverse('queue:index'))
        self.assertTrue(response.url.startswith(reverse('auth:sign-in')))
        self.assertEqual(response.status_code, 302)

        response = self.bad_client.get(reverse('queue:queue_create'))
        self.assertTrue(response.url.startswith(reverse('auth:sign-in')))
        self.assertEqual(response.status_code, 302)

        response = self.bad_client.get(reverse('queue:queue_page', args=[self.public_queue.id]))
        self.assertTrue(response.url.startswith(reverse('auth:sign-in')))
        self.assertEqual(response.status_code, 302)

        response = self.bad_client.get(reverse('queue:queue_page', args=[self.private_queue.id]))
        self.assertTrue(response.url.startswith(reverse('auth:sign-in')))
        self.assertEqual(response.status_code, 302)

        response = self.bad_client.get(reverse('queue:queue_page', args=[self.public_queue.id]))
        self.assertTrue(response.url.startswith(reverse('auth:sign-in')))
        self.assertEqual(response.status_code, 302)

        response = self.bad_client.get(reverse('queue:queue_page', args=[self.private_queue.id]))
        self.assertTrue(response.url.startswith(reverse('auth:sign-in')))
        self.assertEqual(response.status_code, 302)

        response = self.bad_client.get(reverse('queue:queue_page', args=[self.public_queue.id]))
        self.assertTrue(response.url.startswith(reverse('auth:sign-in')))
        self.assertEqual(response.status_code, 302)

        response = self.bad_client.get(reverse('queue:queue_page', args=[self.private_queue.id]))
        self.assertTrue(response.url.startswith(reverse('auth:sign-in')))
        self.assertEqual(response.status_code, 302)

        response = self.bad_client.get(reverse('queue:queue_page', args=[self.public_queue.id]))
        self.assertTrue(response.url.startswith(reverse('auth:sign-in')))
        self.assertEqual(response.status_code, 302)

        response = self.bad_client.get(reverse('queue:queue_page', args=[self.private_queue.id]))
        self.assertTrue(response.url.startswith(reverse('auth:sign-in')))
        self.assertEqual(response.status_code, 302)

        response = self.bad_client.get(reverse('queue:queue_page', args=[self.public_queue.id]))
        self.assertTrue(response.url.startswith(reverse('auth:sign-in')))
        self.assertEqual(response.status_code, 302)

        response = self.bad_client.get(reverse('queue:queue_page', args=[self.private_queue.id]))
        self.assertTrue(response.url.startswith(reverse('auth:sign-in')))
        self.assertEqual(response.status_code, 302)

        response = self.bad_client.get(reverse('queue:queue_page', args=[self.public_queue.id]))
        self.assertTrue(response.url.startswith(reverse('auth:sign-in')))
        self.assertEqual(response.status_code, 302)

        response = self.bad_client.get(reverse('queue:queue_page', args=[self.private_queue.id]))
        self.assertTrue(response.url.startswith(reverse('auth:sign-in')))
        self.assertEqual(response.status_code, 302)

    def test_access_request_for_auth_client(self):
        response = self.client1.get(reverse('queue:index'), follow=True)
        self.assertContains(response, 'Поиск очереди')

        response = self.client1.get(reverse('queue:queue_create'), follow=True)
        self.assertContains(response, 'Создание очереди')

    def test_create_queue_success_public(self):
        self.client1.login(email=self.first_auth_user.email, password='test')
        response = self.client1.post(reverse('queue:queue_create'), {
            'queue_name': 'Public Queue',
            'queue_keyword': 'public',
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Queue.objects.filter(keyword='public').exists())

    def test_create_queue_success_private(self):
        self.client1.login(email=self.first_auth_user.email, password='test')
        response = self.client1.post(reverse('queue:queue_create'), {
            'queue_name': 'Private Queue',
            'queue_keyword': 'private',
            'queue_private': 'on',
            'queue_password': 'secret123'
        }, follow=True)
        queue = Queue.objects.filter(keyword='private').first()
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(queue)
        self.assertEqual(queue.password, 'secret123')

    def test_create_queue_missing_fields(self):
        self.client1.login(email=self.first_auth_user.email, password='test')
        response = self.client1.post(reverse('queue:queue_create'), {
            'queue_name': '',
            'queue_keyword': ''
        }, follow=True)
        self.assertContains(response, "Имя и ключевое слово не могут быть пустыми.")

    def test_create_private_queue_without_password(self):
        self.client1.login(email=self.first_auth_user.email, password='test')
        response = self.client1.post(reverse('queue:queue_create'), {
            'queue_name': 'NoPass',
            'queue_keyword': 'nopass',
            'queue_private': 'on'
        }, follow=True)
        self.assertContains(response, "Вы указали очередь как приватную, однако не указали пароль.")

    def test_create_queue_with_existing_keyword(self):
        self.client1.login(email=self.first_auth_user.email, password='test')
        response = self.client1.post(reverse('queue:queue_create'), {
            'queue_name': 'Duplicate',
            'queue_keyword': 'test'
        }, follow=True)
        self.assertContains(response, "Очередь с таким ключевым словом уже есть.")

    def test_create_queue_success(self):
        response = self.client1.post(reverse('queue:queue_create'), {
            'queue_name': 'new queue',
            'queue_keyword': 'newkeyword',
            'queue_private': '',
            'queue_password': '',
        })
        self.assertEqual(response.status_code, 302)
        new_queue = Queue.objects.get(keyword='newkeyword')
        self.assertRedirects(response, reverse('queue:queue_page', args=[new_queue.id]))

    def test_create_queue_missing_name(self):
        response = self.client1.post(reverse('queue:queue_create'), {
            'queue_name': '',
            'queue_keyword': 'something',
        }, follow=True)
        self.assertContains(response, "Имя и ключевое слово не могут быть пустыми.")

    def test_create_queue_private_without_password(self):
        response = self.client1.post(reverse('queue:queue_create'), {
            'queue_name': 'PrivQueue',
            'queue_keyword': 'priv',
            'queue_private': 'on',
            'queue_password': '',
        }, follow=True)
        self.assertContains(response, "Вы указали очередь как приватную, однако не указали пароль.")

    def test_create_queue_duplicate_keyword(self):
        response = self.client1.post(reverse('queue:queue_create'), {
            'queue_name': 'Another Queue',
            'queue_keyword': self.public_queue.keyword,
        }, follow=True)
        self.assertContains(response, "Очередь с таким ключевым словом уже есть. Придумайте другое ключевое слово.")

    def test_join_public_queue(self):
        response = self.client2.get(reverse('queue:queue_page_join', args=[self.public_queue.id]))
        self.assertRedirects(response, reverse('queue:queue_page', args=[self.public_queue.id]))
        self.assertEqual(self.public_queue.find_user_in_queue(self.second_auth_user) >= 0, True)

    def test_join_private_queue_get_password_page(self):
        response = self.client2.get(reverse('queue:queue_page_join', args=[self.private_queue.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'queue_app/queue_password_enter.html')

    def test_join_private_queue_with_wrong_password(self):
        response = self.client2.post(reverse('queue:queue_password_processing', args=[self.private_queue.id]), {
            'queue_password': 'wrongpass',
        }, follow=True)
        self.assertContains(response, "Неправильный пароль.")

    def test_join_private_queue_with_correct_password(self):
        response = self.client2.post(reverse('queue:queue_password_processing', args=[self.private_queue.id]), {
            'queue_password': 'test',
        })
        self.assertRedirects(response, reverse('queue:queue_page', args=[self.private_queue.id]))
        self.assertEqual(self.private_queue.find_user_in_queue(self.second_auth_user) >= 0, True)

    def test_view_queue_page(self):
        response = self.client1.get(reverse('queue:queue_page', args=[self.public_queue.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'queue_app/queue.html')

    def test_owner_next_in_queue(self):
        self.public_queue.add_user_to_queue(self.second_auth_user)
        response = self.client1.get(reverse('queue:queue_page_next', args=[self.public_queue.id]))
        self.assertRedirects(response, reverse('queue:queue_page', args=[self.public_queue.id]))
        self.public_queue.refresh_from_db()
        self.assertEqual(self.public_queue.participants.count(), 0)

    def test_owner_clear_queue(self):
        self.public_queue.add_user_to_queue(self.second_auth_user)
        response = self.client1.get(reverse('queue:queue_page_clear', args=[self.public_queue.id]))
        self.assertRedirects(response, reverse('queue:queue_page', args=[self.public_queue.id]))
        self.public_queue.refresh_from_db()
        self.assertEqual(self.public_queue.participants.count(), 0)

    def test_owner_delete_queue(self):
        queue_id = self.public_queue.id
        response = self.client1.get(reverse('queue:queue_page_delete', args=[queue_id]))
        self.assertRedirects(response, reverse('queue:index'))
        with self.assertRaises(Queue.DoesNotExist):
            Queue.objects.get(id=queue_id)

    def test_user_exit_queue(self):
        self.public_queue.add_user_to_queue(self.second_auth_user)
        response = self.client2.get(reverse('queue:queue_page_exit', args=[self.public_queue.id]))
        self.assertRedirects(response, reverse('queue:index'))
        self.public_queue.refresh_from_db()
        self.assertTrue(self.public_queue.find_user_in_queue(self.second_auth_user) == -1)
