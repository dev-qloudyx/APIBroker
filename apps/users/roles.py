from django.shortcuts import redirect
from django.contrib import messages


ADMIN = 1
USER = 9

TYPES = (
    (ADMIN, 'admin'),
    (USER, 'user')
)


def role_required(role):

    def _outer(func):

        def _inner(request, *args, **kwargs):
            if request.user.role == role:
                return func(request, *args, **kwargs)
            messages.error(request,
                'Permission denied... You need to be an ADMIN!')
            return redirect('users:login')
        
        return _inner

    return _outer