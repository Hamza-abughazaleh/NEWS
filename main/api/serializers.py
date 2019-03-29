from rest_framework import serializers

from django.contrib.auth import authenticate
from django.utils.translation import gettext as _

from main.models import WebsiteInfo, News, NewsWebsite
from user.models import User
from user.utils import normalise_email


def field_length(fieldname):
    field = next(
        field for field in User._meta.fields if field.name == fieldname)
    return field.max_length


class WebSiteInfoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = WebsiteInfo
        fields = ('pk', 'key', 'website_type', 'search_domain', 'image')


class NewsWebsiteSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = NewsWebsite
        fields = ('pk', 'name', 'url')


class NewsSerializer(serializers.ModelSerializer):
    news_details = serializers.HyperlinkedIdentityField(view_name='news-detail', lookup_field='pk')

    class Meta:
        model = News
        fields = ('pk', 'news_details', 'title', 'image',)


class NewsDetailsSerializer(serializers.ModelSerializer):
    news_website_details = serializers.HyperlinkedRelatedField(view_name='newswebsite-detail', source='news_website',
                                                               read_only=True)

    class Meta:
        model = News
        fields = ('pk', 'title', 'description', 'image', 'url', 'news_website_details')


class UserSerializer(serializers.ModelSerializer):
    user_detail = serializers.HyperlinkedIdentityField(view_name="user-detail", lookup_field='pk')
    phone_number = serializers.RegexField(required=False, regex=r'^\d{9,15}$' ,max_length=15, help_text=_("In case we need to contact you"),)

    class Meta:
        model = User
        fields = ('pk', 'email', 'user_detail','phone_number')
        read_only_fields = ('phone_number','email')


class UserDetailsSerializer(serializers.ModelSerializer):
    phone_number = serializers.RegexField(required=False, regex=r'^\d{9,15}$', max_length=15, help_text=_("In case we need to contact you"),)

    class Meta:
        model = User
        fields = ('email','first_name', 'last_name', 'gender', 'phone_number', 'address')
        read_only_fields = ('phone_number','email')


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=field_length(User.USERNAME_FIELD), required=True)
    password = serializers.CharField(
        max_length=field_length('password'), required=True)

    def validate(self, attrs):
        try:
            normalise_email(attrs['username'])
        except:
            raise serializers.ValidationError(_('invalid username or password'))
        user = authenticate(
            username=attrs['username'], password=attrs['password'])
        if user is None:
            raise serializers.ValidationError(_('invalid login'))
        elif not user.is_active:
            raise serializers.ValidationError(
                _('Can not log in as inactive user'))

        # set instance to the user so we can use this in the view
        self.instance = user
        return attrs
