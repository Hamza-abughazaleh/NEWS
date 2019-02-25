from django.conf.urls import url
from user import views

from django.contrib.auth.decorators import login_required

# TEMPLATE TAGGING
app_name = 'user'

urlpatterns = (
    url('^login', views.UserLogin.as_view(), name='user_login'),
    url('^logout', views.user_logout, name='user_logout'),
    url(r'^register/$', views.UserRegister.as_view(), name='user_register'),
    url(r'^profile/$', login_required(views.ProfileDetailView.as_view()), name='profile'),
    url(r'^profile/update/$', login_required(views.ProfileUpdateView.as_view()), name='update_profile'),
    url(r'^change_password/$', login_required(views.ChangePassword.as_view()), name='change_password'),
    url(r'^password_reset/$', views.PasswordReset.as_view(), name='password_reset'),
    url(r'^password_reset/done/$', views.PasswordResetDone.as_view(), name='password_reset_done'),
    url(r'^password_reset_confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.PasswordResetConfirm.as_view(), name='password_reset_confirm'),
    url(r'^password_reset/complete/$', views.PasswordResetComplete.as_view(), name='password_reset_complete'),

)
