from django.contrib import admin
# from django import forms
from user.models import User, Task


class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'gender', 'address',)
    list_display_links = ('first_name', 'email')


class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'search_term', 'website', 'action_type', 'created_date', 'ip_address')
    list_display_links = ('id', 'search_term')
    readonly_fields = ["user"]


admin.site.register(User, UserAdmin)
admin.site.register(Task, TaskAdmin)
