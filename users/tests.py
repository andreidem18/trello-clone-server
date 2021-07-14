from rest_framework import response
from rest_framework.test import APITestCase
from users.models import User

class UserTestCase(APITestCase):
    def setUp(self):
        self.host = 'http://localhost:8000'
        self.user = User.objects.create_user(
            firstname="user",
            lastname="user_lastname",
            password="root",
            email="user@user.com"
        )
        response = self.client.post(
            f'{self.host}/login/',
            data={'email': 'user@user.com', 'password': 'root'}
        )
        assert response.status_code == 200
        self.token = response.data['access']

    def test_get_users(self):
        response = self.client.get(
            f'{self.host}/users/',
            HTTP_AUTHORIZATION = f'Bearer {self.token}'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_get_user_detail(self):
        response = self.client.get(
            f'{self.host}/users/{self.user.id}/',
            HTTP_AUTHORIZATION = f'Bearer {self.token}'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["firstname"], self.user.firstname)

    def test_post_user(self):
        data={
            'firstname': "user2",
            'lastname': "user2_lastname",
            'password': "root",
            'email': "user2@user.com"
        }
        response = self.client.post(
            f'{self.host}/users/',
            HTTP_AUTHORIZATION = f'Bearer {self.token}',
            data= data,
            format = 'json'
        )
        user2 = User.objects.get(id = response.data['id'])
        self.assertEqual(response.status_code, 201)
        self.assertEqual(user2.firstname, "user2")


    def test_get_my_user(self):
        response = self.client.get(
            f'{self.host}/users/myself/',
            HTTP_AUTHORIZATION = f'Bearer {self.token}'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.user.firstname, response.data["firstname"])

    def test_update_my_user(self):
        data={
            'firstname': "user update",
            'lastname': "user_lastname",
            'email': "user@user.com"
        }
        response = self.client.get(
            f'{self.host}/users/myself/',
            HTTP_AUTHORIZATION = f'Bearer {self.token}',
            data = data,
            format = 'json'
        )
        self.user.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.user.firstname, response.data["firstname"])

    def test_patch_my_user(self):
        data={
            'firstname': "user update"
        }
        response = self.client.get(
            f'{self.host}/users/myself/',
            HTTP_AUTHORIZATION = f'Bearer {self.token}',
            data = data,
            format = 'json'
        )
        self.user.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.user.firstname, response.data["firstname"])