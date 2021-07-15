from datetime import datetime
from workspaces.models import Workspace
from lists.models import List
from boards.models import Board
from .models import Card
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

class CardTestCase(APITestCase):
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
        self.my_list = List.objects.create(
            name="my list",
            board=self.board,
            position = 1
        )
        self.card = Card.objects.create(
            name="my card",
            list=self.my_list,
            description = "Card test",
            deadline = datetime.now(),
            position = 1
        )
        response = self.client.post(
            f'{self.host}/login/',
            data={'email': 'user@user.com', 'password': 'root'}
        )
        assert response.status_code == 200
        self.token = response.data['access']

    def test_get_cards(self):
        response = self.client.get(
            f'{self.host}/cards/',
            HTTP_AUTHORIZATION = f'Bearer {self.token}'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_get_card_detail(self):
        response = self.client.get(
            f'{self.host}/cards/{self.card.id}/',
            HTTP_AUTHORIZATION = f'Bearer {self.token}'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["name"], self.card.name)

    def test_post_card(self):
        data={
            'name': "my card2",
            'list': self.my_list.id,
            'description': "Card test",
            'deadline': str(datetime.now()),
            'position': 1
        }
        response = self.client.post(
            f'{self.host}/cards/',
            HTTP_AUTHORIZATION = f'Bearer {self.token}',
            data= data,
            fromat = 'json'
        )
        card2 = Card.objects.get(id = response.data['id'])
        self.assertEqual(response.status_code, 201)
        self.assertEqual(card2.name, "my card2")

    def test_delete_card(self):
        response = self.client.delete(
            f'{self.host}/cards/{self.card.id}/',
            HTTP_AUTHORIZATION = f'Bearer {self.token}'
        )
        self.assertEqual(response.status_code, 204)



    def test_put_card(self):
        data={
            'name': "my card update",
            'list': self.my_list.id,
            'description': "Card test",
            'deadline': datetime.now(),
            'position': 1
        }
        response = self.client.put(
            f'{self.host}/cards/{self.card.id}/',
            HTTP_AUTHORIZATION = f'Bearer {self.token}',
            data= data,
            fromat = 'json'
        )
        self.card.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], self.card.name)


    def test_patch_card(self):
        data={
            'name': "my card update",
        }
        response = self.client.patch(
            f'{self.host}/cards/{self.card.id}/',
            HTTP_AUTHORIZATION = f'Bearer {self.token}',
            data= data,
            fromat = 'json'
        )
        self.card.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], self.card.name)

    def test_change_position(self):
        self.card2 = Card.objects.create(
            name="my card2",
            list=self.my_list,
            description = "Card test",
            deadline = "2021-09-01",
            position = 2
        )
        response = self.client.post(
            f'{self.host}/cards/{self.card2.id}/position/',
            HTTP_AUTHORIZATION = f'Bearer {self.token}',
            data= {'position': 1},
            fromat = 'json'
        )
        self.card.refresh_from_db()
        self.card2.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.card.position, 2)
        self.assertEqual(self.card2.position, 1)