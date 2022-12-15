from django.shortcuts import redirect
from django.contrib import messages
from rest_framework.response import Response
from rest_framework import status


ADMIN = 1
USER = 9
CS = 19
DMS = 29
BSMS = 39


TYPES = (
    (ADMIN, 'Admin'),
    (USER, 'User'),
    (CS, 'Calculation Service'),
    (DMS, 'DMS'),
    (BSMS, 'BSMS'),
)


def role_required(role):

    def _outer(func):

        def _inner(request, *args, **kwargs):

            if request.user.role == role:
                return func(request, *args, **kwargs)
            messages.error(request,
                           f'Permission denied... You need to be an ADMIN!')
            return redirect('users:login')

        return _inner

    return _outer


def role_required_json(role):
    def _outer(func):
        def _inner(request, *args, **kwargs):
            if request.user.role in role:
                return func(request, *args, **kwargs)
            else:
                return Response({'resultCode': 0, 'errorDescription': f'Permission denied...'}, status=status.HTTP_400_BAD_REQUEST)
        return _inner
    return _outer
