from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

User = get_user_model()

class ChangePasswordViewTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='testuser@example.com',
            password='testpassword',
            first_name='John',
            last_name='Doe',
            is_verified = True
        )
        self.login_url = reverse('token_obtain_pair')

    def test_change_password(self):
        # Authenticate the user and get the access token
        response = self.client.post(self.login_url, {'email': 'testuser@example.com', 'password': 'testpassword'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        access_token = response.data['access']

        # Change the password
        url = reverse('change_password')
        new_password_data = {
            'old_password': 'testpassword',
            'new_password': 'newtestpassword'
        }
        headers = {'Authorization': f'Bearer {access_token}'}
        response = self.client.put(url, new_password_data, format='json', headers=headers)
        print('response------', response)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Verify the new password works
        response = self.client.post(self.login_url, {'email': 'testuser@example.com', 'password': 'newtestpassword'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class ConfirmEmailViewTestCase(APITestCase):
    def test_confirm_email(self):
        # Create a user and generate a token for email confirmation
        user = User.objects.create_user(
            email='testuser@example.com',
            password='testpassword',
            first_name='John',
            last_name='Doe',
        )
        token = default_token_generator.make_token(user)
        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))

        # Confirm the email with the generated token
        url = reverse('confirm-email', args=[uidb64, token])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Email confirmation successful')


# class RegistrationViewTestCase(APITestCase):
#     def test_registration(self):
#         url = reverse("register")
#         registration_data = {
#             "email": "newuser@example.com",
#             "password": "2000money",
#             "first_name": "John",
#             "last_name": "Doe",
#         }
#         response = self.client.post(url, registration_data, format="json")
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)


# class UserListViewTestCase(APITestCase):
#     def setUp(self):
#         # Create a regular user
#         self.user = User.objects.create_user(
#             email="testuser@example.com",
#             password="testpassword",
#             first_name="John",
#             last_name="Doe",
#         )
#         # Create a superuser
#         self.superuser = User.objects.create_superuser(
#             email="superuser@example.com",
#             password="superpassword",
#             first_name="Super",
#             last_name="User",
#         )

#     def test_list_users_by_non_superuser(self):
#         # Authenticate the regular user
#         self.client.force_authenticate(user=self.user)
#         url = reverse("user-list")
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

#     def test_list_users_by_superuser(self):
#         # Authenticate the superuser
#         self.client.force_authenticate(user=self.superuser)
#         url = reverse("user-list")
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)


# class UserDetailViewTestCase(APITestCase):
#     def setUp(self):
#         self.user = User.objects.create_user(
#             email="testuser@example.com",
#             password="testpassword",
#             first_name="John",
#             last_name="Doe",
#         )
#         self.client.force_authenticate(user=self.user)

#     def test_retrieve_user(self):
#         url = reverse("user-detail", args=[str(self.user.id)])
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

#     def test_update_user(self):
#         url = reverse("user-detail", args=[str(self.user.id)])
#         updated_data = {"first_name": "Updated Name"}
#         response = self.client.patch(url, updated_data, format="json")
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

#     def test_delete_user(self):
#         url = reverse("user-detail", args=[str(self.user.id)])
#         response = self.client.delete(url)
#         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
