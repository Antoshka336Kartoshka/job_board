from django.http import HttpResponse, Http404, HttpResponseNotFound, JsonResponse
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.core.mail import EmailMessage
from django.core.paginator import Paginator
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count, Q
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from rest_framework.decorators import api_view

from main.forms import RegistrationForm, LoginForm, AccountSettingsForm, JobForm, CompanyForm
from main.decorators import restrict_auth_users, employer_permission, jobseeker_permission
from main.utils import account_activation_token, is_employer
from main.models import BoardUser, Job, Category, Company
from main.serializers import JobSerializer

from logging import getLogger  # logging for Debug

log = getLogger(__name__)


def index(request):
    categories = Category.objects.annotate(jobs_count=Count('job')).order_by('-jobs_count')[:8]
    jobs_list = Job.objects.order_by('-published_date')[:5]
    featured_candidates = Group.objects.get(name='jobseeker').user_set.filter(is_active=True)[:8]
    top_companies = Group.objects.get(name='employer').user_set.annotate(jobs_count=Count('created_by')).order_by(
        '-jobs_count')[:4]
    context = {'jobs_count': Job.objects.count(), 'categories': categories, 'jobs_list': jobs_list,
               'featured_candidates': featured_candidates, 'top_companies': top_companies}
    return render(request, 'main/index.html', context)


def jobs(request):
    if request.GET:  # if get parameters -> search
        q = request.GET.get('q', default='')
        location = request.GET.get('location', default='')
        category = request.GET.get('category', default='')
        job_nature = request.GET.get('job_nature', default='')
        company = request.GET.get('company', default='')
        jobs_list = Job.objects.filter(
            Q(name__icontains=q), Q(location__icontains=location), Q(category__name__icontains=category),
            Q(job_nature__icontains=job_nature), Q(created_by__company__name__icontains=company)).distinct().order_by(
            '-published_date')
    else:  # return all entities
        jobs_list = Job.objects.order_by('-published_date')

    companies = Group.objects.get(name='employer').user_set.annotate(
        jobs_count=Count('created_by')).order_by('-jobs_count')
    categories = Category.objects.all()
    paginator = Paginator(jobs_list, 5, 1)
    if 'page' in request.GET:
        page_num = request.GET['page']
    else:
        page_num = 1
    page = paginator.get_page(page_num)
    context = {'jobs_list': page.object_list, 'page': page, 'categories': categories, 'companies': companies}
    return render(request, 'main/job/jobs.html', context)


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
    return render(request, 'main/job/job_details.html', context)


@login_required(login_url='login')
@employer_permission
def job_post(request):
    if not request.user.company:
        messages.warning(request, 'To post a job you should register your company')
        return redirect('account_settings')
    form = JobForm
    if request.method == 'POST':
        form = JobForm(request.POST, request.FILES)
        if form.is_valid():
            job = form.save(commit=False)
            job.created_by = request.user
            job.save()
            messages.success(request, 'Your job was added')
            return redirect('job_details', pk=job.pk)
    context = {'form': form}
    return render(request, 'main/job/job_post.html', context)


@login_required(login_url='login')
@jobseeker_permission
def job_apply(request, pk: int):
    user = request.user
    if user.portfolio_link and user.cv_file:
        job = Job.objects.get(pk=pk)
        if user not in job.responding_users.all():
            job.responding_users.add(user)
            msg = 'You are successfully applied for a job'
        else:
            msg = 'You are already applied for this job'
        messages.info(request, msg)
        return redirect('applied_jobs')
    else:
        messages.error(request, 'You should add CV and Portfolio before applying for a job')
        return redirect('account_settings')


@login_required(login_url='login')
@employer_permission
def job_delete(request, pk: int):
    if request.method == 'POST':
        if request.POST.get('confirmation'):
            job = get_object_or_404(Job, pk=pk)
            job.delete()
            messages.success(request, 'Job was successfully deleted')
            return redirect('index')
    return HttpResponseNotFound()


def candidates(request):
    candidates_list = Group.objects.get(name='jobseeker').user_set.filter(is_active=True)
    paginator = Paginator(candidates_list, 8, 4)
    if 'page' in request.GET:
        page_num = request.GET['page']
    else:
        page_num = 1
    page = paginator.get_page(page_num)
    context = {'candidates_list': page.object_list, 'page': page}
    return render(request, 'main/candidate/candidates.html', context)


def candidate_details(request, pk: int):
    candidate = BoardUser.objects.get(pk=pk)
    if is_employer(candidate):
        raise Http404('User does not exists')
    context = {'candidate': candidate}
    return render(request, 'main/candidate/candidate_details.html', context)


def blog(request):
    return render(request, 'main/blog.html')


def single_blog(request):
    return render(request, 'main/single_blog.html')


def contact(request):
    if request.method == 'POST':
        body = f"Message from {request.POST['name']}\n{request.POST['message']}"
        email = EmailMessage(subject=request.POST['subject'], body=body,
                             from_email=request.POST['email'], to=(settings.EMAIL_HOST_USER,))
        email.send()
        messages.success(request, 'Your email was sent, we will contact you via Email soon')
    return render(request, 'main/contact.html')


@restrict_auth_users
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
    return render(request, 'main/account/login.html', context)


@login_required(login_url='login')
def user_logout(request):
    logout(request)
    return redirect('index')


@restrict_auth_users
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
            message = render_to_string('main/account/email_confirmation.html', {
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
    return render(request, 'main/account/registration.html', context=context)


@restrict_auth_users
def activate_user(request, uidb64: str, token: str):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = BoardUser.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, BoardUser.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Thank you for your email confirmation. Now you can log in to your account.')
        return redirect('index')
    else:
        return HttpResponse('Activation link is invalid!')


@restrict_auth_users
def password_reset(request):
    form = PasswordResetForm()
    if request.method == "POST":
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            form.save(subject_template_name='main/account/password_reset_subject.txt',
                      email_template_name='main/account/password_reset_email.html',
                      request=request)
            messages.success(request, "We've emailed you instructions for setting your password")
            return redirect('index')
    return render(request, "main/account/password_reset.html", context={"form": form})


@restrict_auth_users
def password_reset_confirm(request, uidb64: str, token: str):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = BoardUser.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, BoardUser.DoesNotExist):
        user = None
    if user and default_token_generator.check_token(user, token):
        form = SetPasswordForm
        if request.method == 'POST':
            form = SetPasswordForm(user, data=request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Your password was successfully changed. Now you can Log in')
                return redirect('login')
        return render(request, 'main/account/password_reset_confirm.html', context={'form': form})
    else:
        return HttpResponse('Activation link is invalid!')


@login_required(login_url='login')
def account_settings(request):
    user = request.user
    form = AccountSettingsForm(instance=request.user)
    if request.method == 'POST':
        form = AccountSettingsForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account details were changed')
    context = {'user': user, 'is_employer': is_employer(user), 'form': form}
    return render(request, 'main/account/account_settings.html', context)


@login_required(login_url='login')
def account_delete(request, pk: int):
    if request.method == 'POST':
        if request.POST.get('confirmation'):
            user = get_object_or_404(BoardUser, pk=pk)
            if user.company:
                company = get_object_or_404(Company, pk=user.company.pk)
                company.delete()
            user.delete()
            messages.success(request, 'Your account was deleted!')
            return redirect('index')
    return HttpResponseNotFound()


@login_required(login_url='login')
@employer_permission
def create_company(request):
    if request.method == 'POST':
        form = CompanyForm(request.POST, request.FILES)
        if form.is_valid():
            company = form.save()
            user = BoardUser.objects.get(pk=request.user.pk)
            user.company = company
            user.save()
            messages.success(request, 'The company was successfully registered')
            return redirect('account_settings')


@login_required(login_url='login')
def applied_jobs(request):
    if is_employer(request.user):
        jobs_list = request.user.created_by.all()
    else:
        jobs_list = request.user.applied_jobs.all()
    context = {'jobs_list': jobs_list}
    return render(request, 'main/job/jobs.html', context)


# REST

@api_view(['GET'])
def jobs_api(request):
    jobs = Job.objects.all()
    serializer = JobSerializer(jobs, many=True)
    return JsonResponse(serializer.data, safe=False)


@api_view(['GET'])
def job_details_api(request, pk: int):
    job = get_object_or_404(Job, pk=pk)
    serializer = JobSerializer(job)
    return JsonResponse(serializer.data, safe=False)
