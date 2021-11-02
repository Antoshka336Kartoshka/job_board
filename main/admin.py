from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from main.models import BoardUser, Job


# Register your models here.


class BoardUserAdmin(UserAdmin):
    model = BoardUser


class JobAdmin(admin.ModelAdmin):
    model = Job


admin.site.register(BoardUser, BoardUserAdmin)
admin.site.register(Job, JobAdmin)
