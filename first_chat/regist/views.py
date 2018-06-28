from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage

from regist.forms import RegForm, LoginForm
from regist.models import Profile

def LoginView(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            # if request.user.is_authenticated():
            #     logout(request)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username = username, password = password)
            if user is not None:
                login(request, user)
                url = reverse('chat:chat')
                return HttpResponseRedirect(url)
    else:
        form = LoginForm()
    return render(request, 'regist/login.html', {
        'form': form,
        })

def RegistView(request):
    if request.method == 'POST':
        form = RegForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()

            url = reverse('chat:chat')
            return HttpResponseRedirect(url)
        print(form.errors)
    else:
        form = RegForm()

    return render(request, 'regist/reg.html', {'form': form})

def LogoutView(request):
    logout(request)
    url = reverse('chat:chat')

    return HttpResponseRedirect(url)