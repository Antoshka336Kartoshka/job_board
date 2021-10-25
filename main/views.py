from django.shortcuts import render


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
