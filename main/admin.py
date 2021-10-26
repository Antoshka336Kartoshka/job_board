from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from main.models import BoardUser
# Register your models here.


class BoardUserAdmin(UserAdmin):
    model = BoardUser
    ordering = ['first_name']


admin.site.register(BoardUser, BoardUserAdmin)
