from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from .models import CustomUser


class AuthTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_open_auth_index_page(self):
        response = self.client.get(reverse("auth:index"))
        self.assertEqual(response.status_code, 302)

    def test_open_sign_in_page(self):
        response = self.client.get(reverse('auth:sign-in'))
        self.assertEqual(response.status_code, 200)

        response_content = response.content.decode('utf-8')
        form_index = response_content.find('<form')
        self.assertNotEqual(form_index, -1, "Форма не найдена в ответе")

    def test_open_sign_up_page(self):
        response = self.client.get(reverse('auth:sign-up'))
        self.assertEqual(response.status_code, 200)

        response_content = response.content.decode('utf-8')
        form_index = response_content.find('<form')
        self.assertNotEqual(form_index, -1, "Форма не найдена в ответе")

    def test_sign_up_with_non_existing_email(self):
        form_data = {
            "first_name": "example_first_name",
            "last_name": "example_last_name",
            "email": "example@example.com",
            "password": "password123",
            "confirm_password": "password123"
        }

        response = self.client.post(reverse('auth:sign-up-processing'), form_data)

        self.assertEqual(response.status_code, 302)

        self.assertTrue(CustomUser.objects.filter(email=form_data['email']).exists())

        new_user = CustomUser.objects.get(email=form_data['email'])
        self.assertEqual(new_user.first_name, form_data['first_name'])
        self.assertEqual(new_user.last_name, form_data['last_name'])

    def test_sign_out_redirects_to_sign_in(self):
        CustomUser.objects.create_user(
            email="user@example.com",
            password="password123",
            first_name="User",
            last_name="Example"
        )
        self.client.login(email="user@example.com", password="password123")

        response = self.client.get(reverse('auth:sign-out'), follow=True)

        self.assertRedirects(response, reverse('auth:sign-in'))
        self.assertFalse(response.context['user'].is_authenticated)

    def test_sign_in_with_non_existing_user(self):
        response = self.client.post(reverse('auth:sign-in-processing'), {
            'email': 'fakeuser@example.com',
            'password': 'fakeuserpassword'
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('auth:sign-in'))

    def test_sign_in_with_existing_user(self):
        CustomUser.objects.create_user(
            email="user2@example.com",
            password="mypassword",
            first_name="Second",
            last_name="User"
        )

        self.client.post(reverse('auth:sign-in-processing'), {
            'email': 'user2@example.com',
            'password': 'mypassword'
        })

        session = self.client.session
        self.assertIn('_auth_user_id', session)

        logged_in_user = get_user_model().objects.get(pk=session['_auth_user_id'])
        self.assertEqual(logged_in_user.email, 'user2@example.com')

    def test_sign_up_with_existing_email(self):
        CustomUser.objects.create_user(
            email="duplicate@example.com",
            password="originalpass",
            first_name="Existing",
            last_name="User"
        )

        form_data = {
            "first_name": "New",
            "last_name": "User",
            "email": "duplicate@example.com",
            "password": "password123",
            "confirm_password": "password123"
        }

        response = self.client.post(reverse('auth:sign-up-processing'), form_data, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Пользователь с таким email уже существует")
        self.assertEqual(CustomUser.objects.filter(email="duplicate@example.com").count(), 1)
