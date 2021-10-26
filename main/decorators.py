from django.shortcuts import redirect


def unauthenticated_user(view):  # Переделать на вывод ошибки (рендер шаблона ошибики)
    '''
    Restrict unauthenticated users from view
    :param view:
    :return:
    '''
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('index')
        return view(request, *args, **kwargs)
    return wrapper