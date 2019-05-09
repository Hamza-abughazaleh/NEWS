from rest_framework.generics import UpdateAPIView
from rest_framework.response import Response

from user.api_v1 import serializers
from rest_framework import permissions, status


class UserViewSet(UpdateAPIView):
    """ViewSet for the User class"""
    serializer_class = serializers.UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    def get(self, request, format=None):
        ser = self.serializer_class(instance=request.user)
        if request.user.is_authenticated():
            return Response(ser.data)

        return Response({'error': 'HTTP_401_UNAUTHORIZED '}, status=status.HTTP_401_UNAUTHORIZED)

    def update(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user, data=request.data, partial=True, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)
