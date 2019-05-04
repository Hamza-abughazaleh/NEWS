from requests import Request
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.response import Response

from user import models
from user.api_v1 import serializers
from rest_framework import permissions, status


class UserViewSet(RetrieveUpdateAPIView):
    """ViewSet for the User class"""
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer
    details_serializer_class = serializers.UserDetailsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        kwargs['context'] = self.get_serializer_context()
        serializer = self.details_serializer_class(instance, context={'request': request})
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user, data=request.data, partial=True, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)
