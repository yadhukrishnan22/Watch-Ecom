from django.shortcuts import render, redirect

from django.contrib import messages

def signin_required(fn):

    def wrapper(request, *args, **kwargs):

        if not request.user.is_authenticated:

            messages.error(request, 'invalid session')

            return redirect('sign-in')
        
        else:

            return fn(request, *args, **kwargs)
        
    return wrapper