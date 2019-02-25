from django.shortcuts import redirect
from django.views import View
from django.urls import reverse


def normalise_email(email):
    """
    The local part of an email address is case-sensitive, the domain part
    isn't.  This function lowercases the host and should be used in all email
    handling.
    """
    clean_email = email.strip()
    if '@' in clean_email:
        local, host = clean_email.split('@')
        return local + '@' + host.lower()
    return clean_email


def get_user_permission(user):
    if user.is_superuser:
        return 1
    if user.is_staff:
        return 2
    if not user.is_anonymous:
        if user.is_user_paid:
            return 3
    return 0


def get_user_ip(request):
    result = request.META.get('HTTP_X_FORWARDED_FOR')
    if result:
        ip = result.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


class CustomView(View):
    def only_not_logged_in(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse('permission-denied'))
        return True

    def only_logged_in(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('permission-denied')
        return True

    def dispatch(self, request, *args, **kwargs):
        if hasattr(self, 'custom_permissions'):
            for custom_permission in self.custom_permissions:
                result = getattr(self, custom_permission)(request, *args, **kwargs)
                if result != True:
                    return result
        return super(CustomView, self).dispatch(request, *args, **kwargs)
