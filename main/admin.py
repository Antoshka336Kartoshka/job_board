from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from main.models import BoardUser, Job, Category, Company


# Register your models here.


class BoardUserAdmin(UserAdmin):
    model = BoardUser


class JobAdmin(admin.ModelAdmin):
    model = Job


class CategoryAdmin(admin.ModelAdmin):
    model = Category


class CompanyAdmin(admin.ModelAdmin):
    model = Company


admin.site.register(BoardUser, BoardUserAdmin)
admin.site.register(Job, JobAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Company, CompanyAdmin)
