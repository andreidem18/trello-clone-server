from boards.models import Board
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from workspaces.models import Workspace

class BoardTestCase(APITestCase):
    def setUp(self):
        UserModel = get_user_model()
        self.host = 'http://localhost:8000'
        self.user = UserModel.objects.create_user(
            username="",
            password="root",
            email="user@user.com"
        )
        self.workspace = Workspace.objects.create(
            name = "my workspace",
            type = "Small Business",
            owner = self.user
        )
        self.board = Board.objects.create(
            name = "my board",
            description = "testing board",
            img_url = "https://raw.githubusercontent.com/andreidem18/images-bank/main/templates/1.jpg",
            creator = self.user,
            is_public = True,
            workspace = self.workspace
        )
        self.board.members.add(self.user)
        response = self.client.post(
            f'{self.host}/login/',
            data={'email': 'user@user.com', 'password': 'root'}
        )
        assert response.status_code == 200
        self.token = response.data['access']

    def test_get_boards(self):
        response = self.client.get(
            f'{self.host}/boards/',
            HTTP_AUTHORIZATION = f'Bearer {self.token}'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)


    def test_get_board_detail(self):
        response = self.client.get(
            f'{self.host}/boards/{self.board.id}/',
            HTTP_AUTHORIZATION = f'Bearer {self.token}'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["name"], self.board.name)


    def test_post_board(self):
        data={
            'name': "my board2",
            'description': "Board to test",
            'members': [self.user.id],
            'img_url': "https://raw.githubusercontent.com/andreidem18/images-bank/main/templates/1.jpg",
            'is_public': True,
            'workspace': self.workspace.id
        }
        response = self.client.post(
            f'{self.host}/boards/',
            HTTP_AUTHORIZATION = f'Bearer {self.token}',
            data= data,
            format = 'json'
        )
        board2 = Board.objects.get(id = response.data['id'])
        self.assertEqual(response.status_code, 201)
        self.assertEqual(board2.name, "my board2")

    def test_delete_board(self):
        response = self.client.delete(
            f'{self.host}/boards/{self.board.id}/',
            HTTP_AUTHORIZATION = f'Bearer {self.token}'
        )
        self.assertEqual(response.status_code, 204)



    def test_put_board(self):
        data={
            'name': "my board Update",
            'description': "Board to test",
            'members': [self.user.id],
            'favorite': [],
            'img_url': "https://raw.githubusercontent.com/andreidem18/images-bank/main/templates/1.jpg",
            'is_public': True,
            'workspace': self.workspace.id
        }
        response = self.client.put(
            f'{self.host}/boards/{self.board.id}/',
            HTTP_AUTHORIZATION = f'Bearer {self.token}',
            data= data,
            fromat = 'json'
        )
        self.board.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], self.board.name)


    def test_patch_board(self):
        data={
            'name': "my board update",
        }
        response = self.client.patch(
            f'{self.host}/boards/{self.board.id}/',
            HTTP_AUTHORIZATION = f'Bearer {self.token}',
            data= data,
            fromat = 'json'
        )
        self.board.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], self.board.name)



    def test_get_members_board(self):
        response = self.client.get(
            f'{self.host}/boards/{self.board.id}/members/',
            HTTP_AUTHORIZATION = f'Bearer {self.token}'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_post_members_board(self):
        user = get_user_model().objects.create_user(password='root', email='user2@user.com')
        response = self.client.post(
            f'{self.host}/boards/{self.board.id}/members/',
            HTTP_AUTHORIZATION = f'Bearer {self.token}',
            data = {'members': [user.id]},
            format = 'json'
        )
        self.board.refresh_from_db()
        self.assertEqual(response.status_code, 201)
        self.assertEqual(self.board.members.all().count(), 2)

    def test_delete_members_board(self):
        response = self.client.delete(
            f'{self.host}/boards/{self.board.id}/members/',
            HTTP_AUTHORIZATION = f'Bearer {self.token}',
            data = {'members': [self.user.id]},
            format = 'json'
        )
        self.board.refresh_from_db()
        self.assertEqual(response.status_code, 204)
        self.assertEqual(self.board.members.all().count(), 0)


