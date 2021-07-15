from datetime import datetime
from workspaces.models import Workspace
from lists.models import List
from boards.models import Board
from cards.models import Card
from item_checklist.models import ItemChecklist
from .models import Comment
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
        self.user2 = UserModel.objects.create_user(
            username="",
            password="root",
            email="user2@user.com"
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
        self.comment = ItemChecklist.objects.create(
            task="task",
            card=self.card
        )
        self.comment.responsibles.set([self.user, self.user2])
        response = self.client.post(
            f'{self.host}/login/',
            data={'email': 'user@user.com', 'password': 'root'}
        )
        self.comment = Comment.objects.create(
            text = "Testing comments",
            creator = self.user,
            card = self.card
        )
        assert response.status_code == 200
        self.token = response.data['access']



    def test_get_comments(self):
        response = self.client.get(
            f'{self.host}/comments/',
            HTTP_AUTHORIZATION = f'Bearer {self.token}'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)



    def test_get_comment_detail(self):
        response = self.client.get(
            f'{self.host}/comments/{self.comment.id}/',
            HTTP_AUTHORIZATION = f'Bearer {self.token}'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["text"], self.comment.text)



    def test_post_comment(self):
        data={
            'text': "Testing comments 2",
            'card': self.card.id, 
            'creator': self.user.id
        }
        response = self.client.post(
            f'{self.host}/comments/',
            HTTP_AUTHORIZATION = f'Bearer {self.token}',
            data= data,
            format = 'json'
        )
        comment2 = Comment.objects.get(id = response.data['id'])
        self.assertEqual(response.status_code, 201)
        self.assertEqual(comment2.text, response.data["text"])



    def test_delete_comment(self):
        response = self.client.delete(
            f'{self.host}/comments/{self.comment.id}/',
            HTTP_AUTHORIZATION = f'Bearer {self.token}'
        )
        self.assertEqual(response.status_code, 204)



    def test_put_comment(self):
        data={
            'text': "Testing comments update",
            'card': self.card.id
        }
        response = self.client.put(
            f'{self.host}/comments/{self.comment.id}/',
            HTTP_AUTHORIZATION = f'Bearer {self.token}',
            data= data,
            format = 'json'
        )
        self.comment.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['text'], self.comment.text)



    def test_patch_comment(self):
        data={
            'task': "Testing comments update",
        }
        response = self.client.patch(
            f'{self.host}/comments/{self.comment.id}/',
            HTTP_AUTHORIZATION = f'Bearer {self.token}',
            data= data,
            fromat = 'json'
        )
        self.comment.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['text'], self.comment.text)
