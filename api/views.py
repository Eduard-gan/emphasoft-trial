from django.contrib.auth.models import User
from rest_framework import viewsets

from api.serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):

    serializer_class = UserSerializer
    queryset = User.objects.all()

    def retrieve(self, request, *args, **kwargs):
        data = super().retrieve(request, *args, **kwargs)
        print("LOL")
        return data

    def destroy(self, request, *args, **kwargs):
        print("KEK")
