from django.shortcuts import redirect
from django.contrib import messages
from main.utils import is_employer, is_jobseeker


def restrict_auth_users(view):
    """
    Restrict authenticated users from view
    """

    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.info(request, 'You have no access to this page')
            return redirect('index')
        return view(request, *args, **kwargs)

    return wrapper


def employer_permission(view):  # user should be authenticated
    """
    Check if the user is an employer and restricting access if not
    """

    def wrapper(request, *args, **kwargs):
        if is_employer(request.user):
            return view(request, *args, **kwargs)
        else:
            messages.info(request, 'You must be an employer to use this functional')
            return redirect('index')

    return wrapper


def jobseeker_permission(view):  # user should be authenticated
    """
    Check if the user is a jobseeker and restricting access if not
    """

    def wrapper(request, *args, **kwargs):
        if is_jobseeker(request.user):
            return view(request, *args, **kwargs)
        else:
            messages.info(request, 'You must be a jobseeker to use this functional')
            return redirect('index')

    return wrapper
