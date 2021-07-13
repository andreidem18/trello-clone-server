from boards.models import Board
from lists.models import List
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

class ListTestCase(APITestCase):
    def setUp(self):
        UserModel = get_user_model()
        self.host = 'http://localhost:8000'
        self.user = UserModel.objects.create_user(
            username="",
            password="root",
            email="user@user.com"
        )
        self.board = Board.objects.create(
            name = "my board",
            description = "testing board",
            img_url = "https://raw.githubusercontent.com/andreidem18/images-bank/main/templates/1.jpg",
            creator = self.user,
            is_public = True
        )
        self.my_list = List.objects.create(
            name="my list",
            board=self.board,
            position = 1
        )
        response = self.client.post(
            f'{self.host}/login/',
            data={'email': 'user@user.com', 'password': 'root'}
        )
        assert response.status_code == 200
        self.token = response.data['access']

    def test_get_lists(self):
        response = self.client.get(
            f'{self.host}/lists/',
            HTTP_AUTHORIZATION = f'Bearer {self.token}'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_get_list_detail(self):
        response = self.client.get(
            f'{self.host}/lists/{self.my_list.id}/',
            HTTP_AUTHORIZATION = f'Bearer {self.token}'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["name"], self.my_list.name)

    def test_post_list(self):
        data={
            'name': "my list2",
            'board': self.board.id
        }
        response = self.client.post(
            f'{self.host}/lists/',
            HTTP_AUTHORIZATION = f'Bearer {self.token}',
            data= data,
            fromat = 'json'
        )
        my_list2 = List.objects.get(id = response.data['id'])
        self.assertEqual(response.status_code, 201)
        self.assertEqual(my_list2.name, "my list2")

    def test_delete_list(self):
        response = self.client.delete(
            f'{self.host}/lists/{self.my_list.id}/',
            HTTP_AUTHORIZATION = f'Bearer {self.token}'
        )
        self.assertEqual(response.status_code, 204)



    def test_put_my_list(self):
        data={
            'name': "my list2 update",
            'board': self.board.id,
            'position': 1
        }
        response = self.client.put(
            f'{self.host}/lists/{self.my_list.id}/',
            HTTP_AUTHORIZATION = f'Bearer {self.token}',
            data= data,
            fromat = 'json'
        )
        self.my_list.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], self.my_list.name)


    def test_patch_list(self):
        data={
            'name': "my list update",
        }
        response = self.client.patch(
            f'{self.host}/lists/{self.my_list.id}/',
            HTTP_AUTHORIZATION = f'Bearer {self.token}',
            data= data,
            fromat = 'json'
        )
        self.my_list.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], self.my_list.name)

    def test_change_position(self):
        self.my_list2 = List.objects.create(
            name="my list2",
            board=self.board,
            position = 2
        )
        response = self.client.post(
            f'{self.host}/lists/{self.my_list2.id}/position/',
            HTTP_AUTHORIZATION = f'Bearer {self.token}',
            data= {'position': 1},
            fromat = 'json'
        )
        self.my_list.refresh_from_db()
        self.my_list2.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.my_list.position, 2)
        self.assertEqual(self.my_list2.position, 1)