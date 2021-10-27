from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.mail import EmailMessage

from main.forms import RegistrationForm
from main.decorators import unauthenticated_user
from main.utils import account_activation_token
from main.models import BoardUser

from logging import getLogger  # logging for Debug
logger = getLogger(__name__)


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
            user = form.save(commit=False)
            user.is_active = False
            user.save()
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
            return HttpResponse('Please confirm your email address to complete the registration')
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
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.') # Переделать на логин с сообщением
    else:
        return HttpResponse('Activation link is invalid!')
