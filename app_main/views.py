from django.shortcuts import render, redirect


def index(request, *args, **kwargs):
    if bool(request.user and request.user.is_authenticated):
        return redirect('/admin/')
    return redirect('login')
