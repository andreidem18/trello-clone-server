from notifications.serializer import NotificationSerializer
from rest_framework.response import Response
from rest_framework import status
from workspaces.permissions import WorkspacePermissions
from workspaces.serializer import WorkspaceSerializer
from workspaces.models import Workspace
from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from rest_framework.decorators import action
from .tasks import notification_email


class WorkspaceViewSet(ModelViewSet):
    queryset = Workspace.objects.all()
    serializer_class = WorkspaceSerializer
    permission_classes = (WorkspacePermissions,)

    def get_queryset(self):
        data = {}
        if self.request.query_params:
            for k, v in self.request.query_params.items():
                data[k] = v
        return self.queryset.filter(**data)

    def get_object(self):
        return get_object_or_404(Workspace, id=self.kwargs['pk'])

    def create(self, request, *args, **kwargs):
        data = request.data.copy()

        data['owner'] = request.user.id
        data['members'].append(request.user.id)
        letter = data['name'][0].lower()
        data["img_url"] = f'https://raw.githubusercontent.com/andreidem18/images-bank/main/workspaces/{letter}.jpg'
        serialized = WorkspaceSerializer(data = data)
        if not serialized.is_valid():
            return Response(
                status = status.HTTP_400_BAD_REQUEST,
                data = serialized.errors
            )
        serialized.save()
        notify(data['members'], request.user, data['name'], data['img_url'])
        return Response(
            status = status.HTTP_201_CREATED,
            data = serialized.data
        )




    @action(methods=['GET', 'POST', 'DELETE'], detail=True)
    def members(self, request, pk):
        workspace = self.get_object()

        if request.method == 'GET':
            return Response(
                status = status.HTTP_200_OK,
                data = workspace.members.values()
            )


        if request.method == 'POST':
            data = request.data.copy()

            #To remove of request list the users who already were in the workspace
            for member in list(workspace.members.values()):
                for member_request in data["members"]:
                    if str(member["id"]) == member_request:
                        data["members"].remove(member_request)

            for user_id in data["members"]:
                user = get_user_model().objects.get(id = user_id)
                workspace.members.add(user)
            notify(data["members"], request.user, workspace.name, workspace.img_url)
            return Response(status = status.HTTP_201_CREATED)


        if request.method == 'DELETE':
            for member_id in request.data["members"]:
                user = get_user_model().objects.get(id=member_id)
                workspace.members.remove(user)
            return Response(status = status.HTTP_204_NO_CONTENT)



        

    

def notify(members, user, workspace, img_url):
    emails = []
    UserModel = get_user_model()
    for member_id in members:
        user = UserModel.objects.get(id=member_id)
        emails.append(user.email)
        new_notification = {
            'text': f'{user.email} have added you to a new Workspace: {workspace}',
            'url': '',
            'img_url': img_url,
            'user': member_id
        }
        serialized = NotificationSerializer(data = new_notification)
        if not serialized.is_valid():
            print(serialized.errors)
        serialized.save()
        email = user.email
        notification_email.apply_async(
            args = [email, workspace, emails]
        )
        


