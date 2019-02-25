from django.http import HttpResponseForbidden
from django.utils.deprecation import MiddlewareMixin

from user.utils import get_user_permission


class UserPermissionMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.path_info.__contains__('en/user/create/task') or request.path_info.__contains__(
                'ar/user/create/task'):
            user_login = request.user
            user = get_user_permission(user_login)
            if user:
                if user in [1, 2, 3]:
                    return
            else:
                return HttpResponseForbidden()
