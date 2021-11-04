from django.http import HttpResponse, Http404
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string

from main.forms import RegistrationForm, LoginForm, AccountSettingsForm, JobForm
from main.decorators import unauthenticated_user, employer_permission, jobseeker_permission
from main.utils import account_activation_token, is_employer
from main.models import BoardUser, Job

from logging import getLogger  # logging for Debug

log = getLogger(__name__)


def index(request):
    return render(request, 'main/index.html')


def jobs(request):
    jobs_list = Job.objects.all().order_by('-published_date')
    paginator = Paginator(jobs_list, 5, 1)
    if 'page' in request.GET:
        page_num = request.GET['page']
    else:
        page_num = 1
    page = paginator.get_page(page_num)
    context = {'jobs_list': page.object_list, 'page': page}
    return render(request, 'main/jobs.html', context)


def job_details(request, pk: int):
    job = Job.objects.get(pk=pk)
    applied = False
    employer = False
    if request.user.is_authenticated:
        if is_employer(request.user) and job.created_by == request.user:
            employer = True
        elif request.user.applied_jobs.filter(pk=pk):
            applied = True
    context = {'job': job, 'applied': applied, 'is_employer': employer}
    return render(request, 'main/job_details.html', context)


@login_required(login_url='login')
@employer_permission
def job_post(request):
    form = JobForm
    if request.method == 'POST':
        form = JobForm(request.POST, request.FILES)
        if form.is_valid():
            job = form.save(commit=False)
            job.created_by = request.user
            job.save()
            messages.success(request, 'Your job was added')
            return redirect('index')  # <- должен быть переход на страницу вакансии
    context = {'form': form}
    return render(request, 'main/job_post.html', context)


@login_required(login_url='login')
@jobseeker_permission
def job_apply(request, pk: int):
    user = request.user
    log.debug(user)
    if user.portfolio_link and user.cv_file:
        job = Job.objects.get(pk=pk)
        if user not in job.responding_users.all():
            job.responding_users.add(user)
            msg = 'You are successfully applied for a job'
        else:
            msg = 'You are already applied for this job'
        messages.info(request, msg)
        return redirect('index')  # <- Rebuild to redirect on user applied jobs pageuse
    else:
        messages.error(request, 'You should add CV and Portfolio before applying for a job')
        return redirect('account_settings')


@login_required(login_url='login')
@employer_permission
def job_delete(request, pk: int):
    job = get_object_or_404(Job, pk=pk)
    job.delete()
    messages.success(request, 'Job was successfully deleted')
    return redirect('index')


def candidates(request):
    candidates_list = Group.objects.get(name='jobseeker').user_set.all()
    paginator = Paginator(candidates_list, 8, 4)
    if 'page' in request.GET:
        page_num = request.GET['page']
    else:
        page_num = 1
    page = paginator.get_page(page_num)
    context = {'candidates_list': page.object_list, 'page': page}
    return render(request, 'main/candidates.html', context)


def candidate_details(request, pk: int):
    candidate = BoardUser.objects.get(pk=pk)
    if is_employer(candidate):
        raise Http404('User does not exists')
    context = {'candidate': candidate}
    return render(request, 'main/candidate_details.html', context)


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
            if request.GET.get('next', ):
                return redirect(request.GET.get('next', ))
            else:
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
            msg = 'Registration was successful, please confirm your email'
            messages.success(request, msg)
            return redirect('index')
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
    if request.method == 'POST':
        form = AccountSettingsForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account details were changed')
    context = {'user': user, 'is_employer': is_employer(user), 'form': form}
    return render(request, 'main/account_settings.html', context)


@login_required(login_url='login')
def applied_jobs(request):
    if is_employer(request.user):
        jobs_list = request.user.created_by.all()
    else:
        jobs_list = request.user.applied_jobs.all()
    context = {'jobs_list': jobs_list}
    return render(request, 'main/jobs.html', context)
