from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm, SetPasswordForm

from user.utils import normalise_email, get_user_permission
from user.models import User


from user.models import Task


class UpdateProfileForm(forms.ModelForm):
    phone_number = forms.RegexField(required=False, regex=r'^\d{9,15}$', max_length=15,
                                    help_text=_("In case we need to contact you"),
                                    widget=forms.TextInput(
                                        attrs={'class': 'form-control', 'placeholder': _("Phone Number")}))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'gender', 'phone_number', 'address',)
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('First Name')}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Last Name')}),
            # 'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone number'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Address')}),
        }

    def __init__(self, user, *args, **kwargs):
        try:
            instance = User.objects.get(pk=user.pk)
        except User.DoesNotExist:
            # User has no profile, try a blank one
            instance = User(user=user)
        kwargs['instance'] = instance

        super(UpdateProfileForm, self).__init__(*args, **kwargs)
        self.fields['gender'].widget.attrs['class'] = 'form-control'

    def save(self, *args, **kwargs):
        user = self.instance

        # Save user also
        for field_name in self.fields:
            setattr(user, field_name, self.cleaned_data[field_name])
        user.save()

        return super(UpdateProfileForm, self).save(*args, **kwargs)


class LoginForm(forms.ModelForm):
    # password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('email', 'password')

        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': _('Email address')}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': _('Password')}),
        }


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'password1', 'password2',)

        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': _('Email address')}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': _('Password')})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': _('Confirm Password')})

    def clean_email(self):
        email = normalise_email(self.cleaned_data["email"])
        if User._default_manager.filter(email__iexact=email).exists():
            raise forms.ValidationError(_("A user with that email address already exists"))
        return email

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.username = user.email = self.cleaned_data["email"]
        user.password1 = self.cleaned_data["password1"]
        user.password2 = self.cleaned_data["password2"]
        if commit:
            user.save()
        return user


class ChangePasswordForm(UserCreationForm, forms.Form):
    old_password_flag = True  # Used to raise the validation error when it is set to False
    old_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('old_password', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': _('New Password')})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': _('Confirm Password')})
        self.fields['old_password'].widget.attrs.update({'class': 'form-control', 'placeholder': _('Old Password')})

    def set_old_password_flag(self):

        self.old_password_flag = False

        return 0

    def clean_old_password(self, *args, **kwargs):
        old_password = self.cleaned_data.get('old_password')

        if not old_password:
            raise forms.ValidationError(_("You must enter your old password."))

        if not self.old_password_flag:
            raise forms.ValidationError(_("The old password that you have entered is wrong."))

        return old_password


# def get_website_choices():
#     result = CrawlerApi('crawling')
#     data = result.sites_info(False)
#     final_data = []
#     for val in data:
#         if 'key' in val:
#             final_data.append((val['key'], val['logo']))
#     return final_data
#
#
# class CreateTaskForm(forms.ModelForm):
#     action_type = forms.ChoiceField(widget=forms.RadioSelect())
#     website = forms.MultipleChoiceField(choices=get_website_choices(), widget=PrettyCheckboxWidget())
#
#     class Meta:
#         model = Task
#         fields = ('search_term', 'action_type', 'website')
#
#     def __init__(self, user, *args, **kwargs):
#         super(CreateTaskForm, self).__init__(*args, **kwargs)
#         user_permission = get_user_permission(user)
#
#         if user_permission:
#             if user_permission in [1, 2, 3]:
#                 self.fields['action_type'].choices = [
#                     ('CS', _('Crawler with schedule'))]
#                 self.fields['action_type'].initial = 'CS'
#                 self.fields['action_type'].widget = forms.HiddenInput()
#             # if user_permission == 3:
#             #     self.fields['action_type'].choices = [
#             #         ('CW', _('Crawler without schedule'))]
#
#         self.fields['search_term'].widget.attrs.update(
#             {'class': 'form-control', 'placeholder': _('What are you looking for')})
#
#     def save(self, user, user_ip, commit=True):
#         task = super(CreateTaskForm, self).save(commit=False)
#         task.user = user
#         task.ip_address = user_ip
#         task.status = 0
#         if commit:
#             task.save()
#         return task


class CustomPasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': _('Enter your email...')})

    def clean_email(self):
        email = normalise_email(self.cleaned_data["email"])
        if not User._default_manager.filter(email__iexact=email).exists():
            raise forms.ValidationError(_("Email Not Registred"))
        return email


class CustomSetPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['new_password1'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': _('New Password')})
        self.fields['new_password2'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': _('Confirm Password')})
