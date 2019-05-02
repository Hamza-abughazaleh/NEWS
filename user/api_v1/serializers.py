from django.core.files import File

from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email
from allauth.utils import email_address_exists

from News import settings

from user import models
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _


class UserSerializer(serializers.ModelSerializer):
    user_details = serializers.HyperlinkedIdentityField(view_name='user-v1:user-detail',
                                                        read_only=True)

    class Meta:
        model = models.User
        fields = (
            'pk',
            'email',
            'first_name',
            'user_details',
        )


class UserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = (
            'pk',
            'email',
            'username',
            'first_name',
            'last_name',
            'phone_number',
            'is_staff',
            'is_active',
            'date_joined'
        )


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField(required=settings.ACCOUNT_EMAIL_REQUIRED)
    password1 = serializers.CharField(required=True, write_only=True)

    def validate_email(self, email):
        email = get_adapter().clean_email(email)
        if settings.ACCOUNT_UNIQUE_EMAIL:
            if email and email_address_exists(email):
                raise serializers.ValidationError(
                    _("A user is already registered with this e-mail address."))
        return email

    def validate_password1(self, password):
        return get_adapter().clean_password(password)

    def get_cleaned_data(self):
        return {
            'email': self.validated_data.get('email', ''),
            'password1': self.validated_data.get('password1', ''),
            'dob': self.validated_data.get('dob', ''),
            'gender': self.validated_data.get('gender', ''),

        }

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        adapter.save_user(request, user, self)
        setup_user_email(request, user, [])
        user.save()
        return user
