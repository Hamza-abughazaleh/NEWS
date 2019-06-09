from rest_framework.generics import UpdateAPIView
from rest_framework.response import Response

from user.api_v1 import serializers
from rest_framework import permissions, status

from user.models import User


class UserViewSet(UpdateAPIView):
    """ViewSet for the User class"""
    serializer_class = serializers.ProfileSerializer
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, format=None):
        # ser = self.serializer_class(instance=request.user, data=request.data)

        if not request.user.is_authenticated():
            return Response({'error': 'HTTP_401_UNAUTHORIZED '}, status=status.HTTP_401_UNAUTHORIZED)

        return super(UserViewSet, self).put(request, format=format)

    def get_object(self):
        return self.request.user

    def get(self, request, format=None):
        ser = self.serializer_class(instance=request.user)
        if request.user.is_authenticated():
            return Response(ser.data)

        return Response({'error': 'HTTP_401_UNAUTHORIZED '}, status=status.HTTP_401_UNAUTHORIZED)
