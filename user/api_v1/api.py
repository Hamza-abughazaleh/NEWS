from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.response import Response

from user.api_v1 import serializers
from rest_framework import permissions, status
from user.models import User


class UserViewSet(RetrieveUpdateAPIView):
    """ViewSet for the User class"""
    serializer_class = serializers.UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return User.objects.get(id=self.request.user.id)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        kwargs['context'] = self.get_serializer_context()
        serializer = self.serializer_class(instance, context={'request': request})
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user, data=request.data, partial=True, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)
