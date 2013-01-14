from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth import logout
from services.form import LoginForm

def hospital_login(request):
	if request.method == 'POST':
		form = LoginForm(request.POST)
		if form.is_valid(request = request):
			return HttpResponseRedirect('/planning/current')
		return render(request, 'services/login.html', {'form': form, 'redirect' : True, 'status': False, 'message' : 'Impossible de se connecter, utilisateur ou mot de passe invalide' })
	else:
		form = LoginForm()
		return render(request, 'services/login.html', {'form': form, 'redirect' : False})

def hospital_logout(request):
	logout(request)
	return HttpResponseRedirect('/')

def hospital_password_change(request):
	pass
