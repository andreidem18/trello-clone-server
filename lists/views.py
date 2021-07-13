from rest_framework.serializers import ListSerializer
from lists.models import List
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet

class ListViewSet(ModelViewSet):
    queryset = List.objects.all()
    serializer_class = ListSerializer


    def get_queryset(self):
        data = {}
        if self.request.query_params:
            for k, v in self.request.query_params.items():
                data[k] = v
        return self.queryset.filter(**data)
