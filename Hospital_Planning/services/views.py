from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from services.model import Calandars
from servicess.forms import CalandarsForm

@login_required
def service(request):
	aListServices = services.objects()
	return render( request,  'services/service.html', {'servicesList': aListServices})

@login_required
def service_add(request):
	if request.method == 'POST':
		form = ServicesForm(request.POST) 
		if form.is_valid():
			form.save() 
			return HttpResponseRedirect('/index/')
	else:
		form =  ServicesForm()
		return render(request, 'services/add.html', {'form': form})
