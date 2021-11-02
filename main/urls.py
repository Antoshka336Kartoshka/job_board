from django.urls import path
from main import views

urlpatterns = [
    path('', views.index, name='index'),
    path('jobs/', views.jobs, name='jobs'),
    path('jobs/post/', views.post_job, name='post_job'),
    path('jobs/<int:pk>', views.job_details, name='job_details'),
    path('candidate/', views.candidate, name='candidate'),
    path('blog/', views.blog, name='blog'),
    path('single_blog/', views.single_blog, name='single_blog'),
    path('contact/', views.contact, name='contact'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('registration/', views.user_registration, name='registration'),
    path('activate/<uidb64>/<token>/', views.activate_user, name='activate'),
    path('account/settings/', views.account_settings, name='account_settings'),
]
