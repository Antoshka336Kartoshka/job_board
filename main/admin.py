from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from main.models import BoardUser, Job, Category, Company


class StackedUser(admin.StackedInline):
    model = BoardUser
    fields = ['username', 'first_name', 'last_name', 'email']
    readonly_fields = ['username', 'first_name', 'last_name', 'email']


class CompanyAdmin(admin.ModelAdmin):
    model = Company
    search_fields = ['name']
    inlines = [StackedUser]


class BoardUserAdmin(UserAdmin):
    model = BoardUser
    ordering = ['date_joined']
    search_fields = ['username', 'first_name', 'last_name', 'email']
    readonly_fields = ['username', 'first_name', 'last_name', 'email', 'last_login', 'date_joined']


class JobAdmin(admin.ModelAdmin):
    model = Job
    list_display = ['name', 'category', 'created_by']
    search_fields = ['name']
    view_on_site = True


class CategoryAdmin(admin.ModelAdmin):
    model = Category


admin.site.register(BoardUser, BoardUserAdmin)
admin.site.register(Job, JobAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Company, CompanyAdmin)
