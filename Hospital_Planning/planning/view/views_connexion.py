'''
Created on Jan 23, 2015

@author: knguyen
'''

from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth import logout
from planning.forms import LoginForm
from planning.models import doctors

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid(request = request):
            if 'old_password' not in request.POST:
                return HttpResponseRedirect('/planning/view_calendar/')
            else:
                if request.POST['new_password1'] == request.POST['new_password2']:
                    aDoctor = doctors.objects.get(username = request.user)
                    aDoctor.set_password(request.POST['new_password1'])
                    aDoctor.save()
            return HttpResponseRedirect('/planning/view_calendar/')
        if 'old_password' not in request.POST:
            return render(request, 'planning/login.html', {'form': form, 'redirect' : True, 'status': False, 'message' : 'Impossible de se connecter, utilisateur ou mot de passe invalide' })
        else:
            return HttpResponseRedirect('/planning/change_login')
    else:
        form = LoginForm()
        return render(request, 'planning/login.html', {'form': form, 'redirect' : False})

def logout_(request):
    logout(request)
    return HttpResponseRedirect('/')

def change_login(request):
    #TODO
    pass    