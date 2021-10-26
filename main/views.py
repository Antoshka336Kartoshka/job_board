from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from main.forms import RegistrationForm
from main.decorators import unauthenticated_user
# Create your views here.


def index(request):
    return render(request, 'main/index.html')


def jobs(request):
    return render(request, 'main/jobs.html')


def candidate(request):
    return render(request, 'main/candidate.html')


def job_details(request):
    return render(request, 'main/job_details.html')


def blog(request):
    return render(request, 'main/blog.html')


def single_blog(request):
    return render(request, 'main/single_blog.html')


def contact(request):
    return render(request, 'main/contact.html')


@unauthenticated_user
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('index')
        else:
            messages.info(request, 'Sorry, username or password is incorrect')
    return render(request, 'main/login.html')


@login_required(login_url='login')
def user_logout(request):
    logout(request)
    return redirect('index')


@unauthenticated_user
def user_registration(request):
    form = RegistrationForm
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('index')
    context = {'form': form}
    return render(request, 'main/registration.html', context=context)
