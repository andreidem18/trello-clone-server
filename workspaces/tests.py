from workspaces.models import Workspace
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

class WorkspaceTestCase(APITestCase):
    def setUp(self):
        UserModel = get_user_model()
        self.host = 'http://localhost:8000'
        self.user = UserModel.objects.create_user(
            username="",
            password="root",
            email="user@user.com"
        )
        self.workspace = Workspace.objects.create(
            name="my workspace",
            type="Small Business",
            owner = self.user
        )
        self.workspace.members.add(self.user)
        response = self.client.post(
            f'{self.host}/login/',
            data={'email': 'user@user.com', 'password': 'root'}
        )
        assert response.status_code == 200
        self.token = response.data['access']

    def test_get_workspaces(self):
        response = self.client.get(
            f'{self.host}/workspaces/',
            HTTP_AUTHORIZATION = f'Bearer {self.token}'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_get_workspace_detail(self):
        response = self.client.get(
            f'{self.host}/workspaces/{self.workspace.id}/',
            HTTP_AUTHORIZATION = f'Bearer {self.token}'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["name"], self.workspace.name)

    def test_post_workspace(self):
        data={
            'name': "my workspace2",
            'type': "Small Business",
            'members': []
        }
        response = self.client.post(
            f'{self.host}/workspaces/',
            HTTP_AUTHORIZATION = f'Bearer {self.token}',
            data= data,
            format = 'json'
        )
        workspace2 = Workspace.objects.get(id = response.data['id'])
        self.assertEqual(response.status_code, 201)
        self.assertEqual(workspace2.name, "my workspace2")

    def test_delete_workspace(self):
        response = self.client.delete(
            f'{self.host}/workspaces/{self.workspace.id}/',
            HTTP_AUTHORIZATION = f'Bearer {self.token}'
        )
        self.assertEqual(response.status_code, 204)



    def test_put_workspace(self):
        data={
            'name': "my workspace update",
            'type': "Small Business",
            'members': [self.user.id],
            'img_url': 'https://raw.githubusercontent.com/andreidem18/images-bank/main/workspaces/m.jpg'
        }
        response = self.client.put(
            f'{self.host}/workspaces/{self.workspace.id}/',
            HTTP_AUTHORIZATION = f'Bearer {self.token}',
            data= data,
            fromat = 'json'
        )
        self.workspace.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], self.workspace.name)


    def test_patch_workspace(self):
        data={
            'name': "my workspace update",
        }
        response = self.client.patch(
            f'{self.host}/workspaces/{self.workspace.id}/',
            HTTP_AUTHORIZATION = f'Bearer {self.token}',
            data= data,
            fromat = 'json'
        )
        self.workspace.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], self.workspace.name)



    def test_get_members_workspace(self):
        response = self.client.get(
            f'{self.host}/workspaces/{self.workspace.id}/members/',
            HTTP_AUTHORIZATION = f'Bearer {self.token}'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_post_members_workspace(self):
        user = get_user_model().objects.create_user(username='', password='root', email='user2@user.com')
        response = self.client.post(
            f'{self.host}/workspaces/{self.workspace.id}/members/',
            HTTP_AUTHORIZATION = f'Bearer {self.token}',
            data = {'members': [user.id]},
            format = 'json'
        )
        self.workspace.refresh_from_db()
        self.assertEqual(response.status_code, 201)
        self.assertEqual(self.workspace.members.all().count(), 2)

    def test_delete_members_workspace(self):
        response = self.client.delete(
            f'{self.host}/workspaces/{self.workspace.id}/members/',
            HTTP_AUTHORIZATION = f'Bearer {self.token}',
            data = {'members': [self.user.id]},
            format = 'json'
        )
        self.workspace.refresh_from_db()
        self.assertEqual(response.status_code, 204)
        self.assertEqual(self.workspace.members.all().count(), 0)

