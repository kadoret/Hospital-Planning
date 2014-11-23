from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth import logout
from services.form import LoginForm
from services.models import doctors

def hospital_login(request):
	if request.method == 'POST':
		form = LoginForm(request.POST)
		if form.is_valid(request = request):
			if 'old_password' not in request.POST:
				return HttpResponseRedirect('/planning/calendar_view/')
			else:
				if request.POST['new_password1'] == request.POST['new_password2']:
					aDoctor = doctors.objects.get(username = request.user)
					aDoctor.set_password(request.POST['new_password1'])
					aDoctor.save()
			return HttpResponseRedirect('/planning/calendar_view/')
		if 'old_password' not in request.POST:
			return render(request, 'services/login.html', {'form': form, 'redirect' : True, 'status': False, 'message' : 'Impossible de se connecter, utilisateur ou mot de passe invalide' })
		else:
			return HttpResponseRedirect('/services/change/')
	else:
		form = LoginForm()
		return render(request, 'services/login.html', {'form': form, 'redirect' : False})

def hospital_logout(request):
	logout(request)
	return HttpResponseRedirect('/')

def hospital_password_change(request):
	#TODO
	pass	
