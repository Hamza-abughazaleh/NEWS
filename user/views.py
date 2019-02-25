from django.contrib.auth import authenticate, login, logout

from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages

from django.shortcuts import render
from django.contrib.auth import update_session_auth_hash

from user.forms import User, LoginForm, RegisterForm, UpdateProfileForm, ChangePasswordForm, CustomPasswordResetForm, \
    CustomSetPasswordForm

from django.views.generic import TemplateView, FormView, CreateView
from django.urls import reverse_lazy
from django.shortcuts import redirect

from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, \
    PasswordResetCompleteView

from django.utils.translation import ugettext_lazy as _
from django.utils.translation import get_language

from user.utils import get_user_ip, CustomView, get_user_permission


class UserLogin(FormView):
    template_name = 'login.html'
    form_class = LoginForm

    # success_url = '/login/'

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = authenticate(username=form.cleaned_data.get('email'), password=form.cleaned_data.get('password'))

            if user and user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('home'))
            else:
                messages.error(request, _("Please enter a correct email address and password."))
                return render(request, self.template_name, {'form': form})


def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))


class UserRegister(FormView):
    template_name = 'register.html'
    form_class = RegisterForm

    # success_url = '/login/'

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save()
            user.set_password(user.password1)
            user.save()

            # after the user is registered go to login page
            # return HttpResponseRedirect(reverse('user:user_login'))
            user = authenticate(username=form.cleaned_data.get('email'), password=form.cleaned_data.get('password1'))
            if user and user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('home'))

        return render(request, self.template_name, {'form': form})


class ProfileDetailView(TemplateView):
    template_name = "user_profile.html"

    def get_context_data(self, **kwargs):
        ctx = super(ProfileDetailView, self).get_context_data(**kwargs)
        ctx['user'] = self.request.user
        return ctx

    def get_object(self):
        return self.request.user


class ProfileUpdateView(FormView):
    form_class = UpdateProfileForm
    template_name = "update_profile.html"
    success_url = reverse_lazy('user:profile')

    def get_form_kwargs(self):
        kwargs = super(ProfileUpdateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        # Grab current user instance before we save form.  We may need this to
        # send a warning email if the email address is changed.
        try:
            old_user = User.objects.get(id=self.request.user.id)
        except User.DoesNotExist:
            old_user = None

        form.save()
        messages.success(self.request, _("Profile updated"))
        return redirect(self.get_success_url())


class ChangePassword(FormView):
    form_class = ChangePasswordForm
    template_name = 'change_user_password.html'
    success_url = reverse_lazy('user:profile')

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        try:
            old_user = User.objects.get(id=self.request.user.id)
            if old_user.check_password(form.data.get("old_password")) == False:
                form.set_old_password_flag()

            if form.is_valid():
                old_user.set_password(form.data.get("password1"))
                old_user.save()
                update_session_auth_hash(self.request, old_user)

                messages.success(self.request, _("Password Changed Successfully"))
                return redirect(self.get_success_url())
            else:
                return render(request, self.template_name, {'form': form})
        except User.DoesNotExist:
            old_user = None


# class CreateTask(CreateView, CustomView):
#     template_name = "create_task.html"
#     form_class = CreateTaskForm
#     success_url = reverse_lazy('user:create_task')
#     custom_permissions = ['only_logged_in', 'user_permission']
#
#     def user_permission(self, request, *args, **kwargs):
#         user_login = request.user
#         user = get_user_permission(user_login)
#         if user:
#             if user in [1, 2, 3]:
#                 return True
#         else:
#             return redirect(reverse('permission-denied'))
#
#     def get_form_kwargs(self):
#         kwargs = super(CreateTask, self).get_form_kwargs()
#         kwargs['user'] = self.request.user
#         return kwargs
#
#     def form_valid(self, form):
#         search_term = form.cleaned_data.get('search_term')
#         website = form.cleaned_data.get('website')
#         action_type = form.cleaned_data.get('action_type')
#         try:
#             result = CrawlerApi('crawling')
#             result.create_task(search_term=search_term, action_type=action_type, websites=website)
#             if self.request.user:
#                 user_ip = get_user_ip(self.request)
#                 self.object = form.save(self.request.user, user_ip)
#         except:
#             messages.info(self.request, "Something is wrong check your data")
#             return super(CreateTask, self).form_invalid(form)
#
#         messages.info(self.request, _("Your results will be available soon."))
#         return redirect(self.get_success_url())


class PasswordReset(PasswordResetView, CustomView):
    template_name = 'password_reset_form.html'
    email_template_name = 'password_reset_email.html'
    success_url = reverse_lazy('user:password_reset_done')
    form_class = CustomPasswordResetForm
    custom_permissions = ['only_not_logged_in']

    def __init__(self, *args, **kwargs):
        super(PasswordReset, self).__init__(*args, **kwargs)
        if get_language() == 'ar':
            self.email_template_name = "password_reset_email_ar.html"


class PasswordResetDone(PasswordResetDoneView, CustomView):
    template_name = 'password_reset_done.html'
    custom_permissions = ['only_not_logged_in']


class PasswordResetConfirm(PasswordResetConfirmView, CustomView):
    template_name = 'password_reset_confirm.html'
    success_url = reverse_lazy('user:password_reset_complete')
    form_class = CustomSetPasswordForm
    custom_permissions = ['only_not_logged_in']


class PasswordResetComplete(PasswordResetCompleteView, CustomView):
    template_name = 'password_reset_complete.html'
    custom_permissions = ['only_not_logged_in']
