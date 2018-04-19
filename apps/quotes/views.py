# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .models import *

# Create your views here.

def index(request):
    return render(request, 'quotes/index.html')

def create_user(request):
    validation=User.objects.reg_validation(request.POST)
    if validation[0]:
        request.session['user_id']=validation[1].id
        request.session['user_name']=validation[1].name
        return redirect('/dashboard')
    else:
        for error in validation[1]:
            messages.add_message(request, messages.INFO, error)
        return redirect('/')

def login(request):
    validation=User.objects.log_validation(request.POST)
    if validation[0]:
        request.session['user_id']=validation[1].id
        request.session['user_name']=validation[1].name
        return redirect ('/dashboard')
    else:
        for error in validation[1]:
            messages.add_message(request, messages.INFO, error)
        return redirect ('/')

def logout(request):
    request.session.clear()
    return redirect ('/')

def dashboard(request):
    user = User.objects.get(id=request.session['user_id'])
    context={
        'quotable':Quote.objects.exclude(liked_by=user),
        'favorites':user.liked.all()
    }
    return render(request, 'quotes/dashboard.html', context)

def post_quote(request):
    id=request.session['user_id']
    errors=Quote.objects.quote_validation(request.POST, id)
    if errors[0]:
        return redirect ('/dashboard')
    else:
        for error in errors[1]:
            messages.add_message(request, messages.INFO, error)
        return redirect ('/dashboard')
    

def displayuserquotes(request, id):
    context={
        'posted':User.objects.get(id=id).posted.all(),
        'poster':User.objects.get(id=id),
        'count':User.objects.get(id=id).posted.count()
    }
    return render (request, 'quotes/user.html', context)

def addquote(request, id):
    quote_liked=Quote.objects.get(id=id)
    this_user=User.objects.get(id=request.session['user_id'])
    quote_liked.liked_by.add(this_user)
    return redirect("/dashboard")

def removequote(request, id):
    quote_liked=Quote.objects.get(id=id)
    this_user=User.objects.get(id=request.session['user_id'])
    quote_liked.liked_by.remove(this_user)
    return redirect('/dashboard')