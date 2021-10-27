from django.urls import path
from main import views
"""job_board URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""


urlpatterns = [
    path('', views.index, name='index'),
    path('jobs/', views.jobs, name='jobs'),
    path('candidate/', views.candidate, name='candidate'),
    path('job_details/', views.job_details, name='job_details'),
    path('blog/', views.blog, name='blog'),
    path('single_blog/', views.single_blog, name='single_blog'),
    path('contact/', views.contact, name='contact'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('registration/', views.user_registration, name='registration'),
    path('activate/<uidb64>/<token>/', views.activate_user, name='activate'),
]