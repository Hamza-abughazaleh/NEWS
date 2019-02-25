import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models as models
from django.utils.translation import ugettext_lazy as _


class User(AbstractUser):
    GENDER_CHOICES = (
        (None, _('Choose gender')),
        ('M', _('Male')),
        ('F', _('Female')),
    )
    gender = models.CharField(max_length=1, blank=True, null=True, choices=GENDER_CHOICES)
    phone_number = models.CharField(_("Phone number"), blank=True, help_text=_("In case we need to contact you"),
                                    max_length=200)
    address = models.CharField(_("Address"), blank=True, max_length=350)
    is_user_paid = models.BooleanField(default=False)

    def __str__(self):
        full_name = self.get_full_name()
        if full_name == "":
            return self.email
        return full_name

    def get_full_name(self):
        full_name = super(User, self).get_full_name()
        if not full_name:
            full_name = self.email
        return full_name

    def get_gender_display(self):
        if self.gender == "M":
            return _("Male")
        else:
            return _("Female")


class Task(models.Model):
    search_term = models.CharField(max_length=200, )
    website = models.CharField(max_length=100, )
    action_type = models.CharField(max_length=10, )
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=50, null=True, blank=True)
    created_date = models.DateTimeField(default=datetime.datetime.now())
    ip_address = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.search_term
