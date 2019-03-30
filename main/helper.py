from django.contrib.auth.decorators import user_passes_test

from django.urls import reverse_lazy


def anonymous_required(function=None, redirect_field_name='', login_url=reverse_lazy('permission-denied')):
    """
    Decorator for views that checks that the user is logged in, redirecting
    to the log-in page if necessary.
    """
    actual_decorator = user_passes_test(
        lambda u: not u.is_authenticated,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator