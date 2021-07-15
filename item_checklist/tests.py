from datetime import datetime
from workspaces.models import Workspace
from lists.models import List
from boards.models import Board
from cards.models import Card
from .models import ItemChecklist
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
        self.item_checklist = ItemChecklist.objects.create(
            task="task",
            card=self.card
        )
        self.item_checklist.responsibles.add(self.user)
        response = self.client.post(
            f'{self.host}/login/',
            data={'email': 'user@user.com', 'password': 'root'}
        )
        assert response.status_code == 200
        self.token = response.data['access']

    def test_get_items(self):
        response = self.client.get(
            f'{self.host}/items/',
            HTTP_AUTHORIZATION = f'Bearer {self.token}'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_get_item_detail(self):
        response = self.client.get(
            f'{self.host}/items/{self.item_checklist.id}/',
            HTTP_AUTHORIZATION = f'Bearer {self.token}'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["task"], self.item_checklist.task)

    def test_post_item(self):
        data={
            'task': "task2",
            'card': self.card.id, 
            'responsibles': [self.user.id]
        }
        response = self.client.post(
            f'{self.host}/items/',
            HTTP_AUTHORIZATION = f'Bearer {self.token}',
            data= data,
            format = 'json'
        )
        item2 = ItemChecklist.objects.get(id = response.data['id'])
        self.assertEqual(response.status_code, 201)
        self.assertEqual(item2.task, "task2")

    def test_delete_item(self):
        response = self.client.delete(
            f'{self.host}/items/{self.item_checklist.id}/',
            HTTP_AUTHORIZATION = f'Bearer {self.token}'
        )
        self.assertEqual(response.status_code, 204)



    def test_put_item(self):
        data={
            'task': "task update",
            'card': self.card.id,
            'responsibles': [self.user.id]
        }
        response = self.client.put(
            f'{self.host}/items/{self.item_checklist.id}/',
            HTTP_AUTHORIZATION = f'Bearer {self.token}',
            data= data,
            format = 'json'
        )
        self.item_checklist.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['task'], self.item_checklist.task)


    def test_patch_item(self):
        data={
            'task': "task update",
        }
        response = self.client.patch(
            f'{self.host}/items/{self.item_checklist.id}/',
            HTTP_AUTHORIZATION = f'Bearer {self.token}',
            data= data,
            fromat = 'json'
        )
        self.item_checklist.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['task'], self.item_checklist.task)


    def test_get_responsibles(self):
        response = self.client.get(
            f'{self.host}/items/{self.item_checklist.id}/responsibles/',
            HTTP_AUTHORIZATION = f'Bearer {self.token}'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_post_responsibles(self):
        user = get_user_model().objects.create_user(username='', password='root', email='user2@user.com')
        response = self.client.post(
            f'{self.host}/items/{self.item_checklist.id}/responsibles/',
            HTTP_AUTHORIZATION = f'Bearer {self.token}',
            data = {'responsibles': [user.id]},
            format = 'json'
        )
        self.item_checklist.refresh_from_db()
        self.assertEqual(response.status_code, 201)
        self.assertEqual(self.item_checklist.responsibles.all().count(), 2)

    def test_delete_responsibles(self):
        response = self.client.delete(
            f'{self.host}/items/{self.item_checklist.id}/responsibles/',
            HTTP_AUTHORIZATION = f'Bearer {self.token}',
            data = {'responsibles': [self.user.id]},
            format = 'json'
        )
        self.item_checklist.refresh_from_db()
        self.assertEqual(response.status_code, 204)
        self.assertEqual(self.item_checklist.responsibles.count(), 0)
