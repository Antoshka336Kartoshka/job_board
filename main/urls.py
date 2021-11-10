from django.urls import path
from main import views
from django.contrib.auth.views import PasswordResetConfirmView

urlpatterns = [
    path('', views.index, name='index'),
    path('jobs/', views.jobs, name='jobs'),
    path('jobs/post/', views.job_post, name='job_post'),
    path('jobs/<int:pk>', views.job_details, name='job_details'),
    path('jobs/<int:pk>/apply/', views.job_apply, name='job_apply'),
    path('jobs/<int:pk>/delete/', views.job_delete, name='job_delete'),
    path('candidates/', views.candidates, name='candidate'),
    path('candidates/<int:pk>', views.candidate_details, name='candidate_details'),
    path('blog/', views.blog, name='blog'),
    path('single_blog/', views.single_blog, name='single_blog'),
    path('contact/', views.contact, name='contact'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('registration/', views.user_registration, name='registration'),
    path('activate/<uidb64>/<token>/', views.activate_user, name='activate'),
    path('account/settings/', views.account_settings, name='account_settings'),
    path('account/password/reset/', views.password_reset, name='password_reset'),
    path('account/password/reset/confirm/<uidb64>/<token>/', views.password_reset_confirm, name='password_reset_confirm'),
    path('account/create_company/', views.create_company, name='create_company'),
    path('account/jobs/', views.applied_jobs, name='applied_jobs'),

]
