from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from main.models import BoardUser, Company


# Register your models here.


class BoardUserAdmin(UserAdmin):
    model = BoardUser


class CompanyAdmin(admin.ModelAdmin):
    model = Company


admin.site.register(BoardUser, BoardUserAdmin)
admin.site.register(Company, CompanyAdmin)
