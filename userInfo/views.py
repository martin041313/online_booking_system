# -*- coding:utf-8 -*-  
from django.contrib import auth
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib import messages

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            new_user.save()
            return HttpResponseRedirect("/accouts/login/")
    else:
        form = UserCreationForm()
    return render_to_response("register.html", {
        'form': form,
    },context_instance=RequestContext(request))



def login_view(request):
    next_page = request.GET.get('next_page','/booking/')
    if request.user is not None and request.user.is_active:
        messages.add_message(request, messages.INFO, 'You have logged in.')
        return HttpResponseRedirect(next_page)
    elif request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_active:
            # Correct password, and the user is marked "active"
            auth.login(request, user)
            # Redirect to a success page.
            return HttpResponseRedirect(next_page)
        else:
            messages.add_message(request, messages.INFO,'user name or password is not correct.')
            return render_to_response('login.html',{},context_instance=RequestContext(request))
    else:
        return render_to_response('login.html',{},context_instance=RequestContext(request))
