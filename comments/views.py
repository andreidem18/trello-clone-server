# from rest_framework import status
# from rest_framework.response import Response
# from rest_framework.viewsets import ModelViewSet
# from .models import Comment
# from .serializer import CommentSerializer

# class CommentViewSet(ModelViewSet):
#     queryset = Comment.objets.all()
#     serializer_class = CommentSerializer

#     def create(self, request, *args, **kwargs):
#         data = request.data.copy()
#         data["creator"] = request.user
#         serialized = CommentSerializer(data = data)
#         if not serialized.is_valid():
#             return Response(
#                 status = status.HTTP_400_BAD_REQUEST,
#                 data = serialized.errors
#             )
#         serialized.save()
#         notify(data['members'], request.user, data['name'], data['img_url'])
#         return Response(
#             status = status.HTTP_201_CREATED,
#             data = serialized.data
#         )


# def notify(user_name, task, card, responsibles):
#     emails = []
#     img = Card.objects.get(id=card).list.board.img_url
#     for user_id in responsibles:
#         user = User.objects.get(id=user_id)
#         emails.append(user.email)
#         Notification.objects.create(
#             text = f"{user_name} have added you to a new task: {task}",
#             url = '',
#             img_url = img,
#             user = user
#         )    
#         emails.append(user.email)
#     notification_email.apply_async(
#         args = [user_name, task, emails]
#     )

