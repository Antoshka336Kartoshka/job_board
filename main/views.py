from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.mail import EmailMessage

from main.forms import RegistrationForm, LoginForm, AccountSettingsForm
from main.decorators import unauthenticated_user
from main.utils import account_activation_token, is_employer
from main.models import BoardUser

from logging import getLogger  # logging for Debug
log = getLogger(__name__)


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
    form = LoginForm(request)
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'You logged in')
            return redirect('index')
    context = {'form': form}
    return render(request, 'main/login.html', context)


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
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            if request.POST.get('employer'):
                user_group = Group.objects.get(name='employer')
            else:
                user_group = Group.objects.get(name='jobseeker')
            user.groups.add(user_group)
            current_site = get_current_site(request)
            mail_subject = 'Activation link from Job Board'
            message = render_to_string('main/email_confirmation.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            msg = 'Registration was successful, please confirm your email and you will be able to Log in'
            return render(request, 'main/message.html', context={'msg': msg})
    context = {'form': form}
    return render(request, 'main/registration.html', context=context)


def activate_user(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = BoardUser.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, BoardUser.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        msg = 'Thank you for your email confirmation. Now you can login your account.'
        return render(request, 'main/message.html', context={'msg': msg})
    else:
        return HttpResponse('Activation link is invalid!')


@login_required(login_url='login')
def account_settings(request):  # Print all columns from model
    user = request.user
    form = AccountSettingsForm(instance=request.user)
    context = {'user': user, 'is_employer': is_employer(user), 'form': form}
    return render(request, 'main/account_settings.html', context)