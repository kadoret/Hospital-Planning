from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from services.model import Calandars
from servicess.forms import CalandarsForm

@login_required
def index(request):
	aListServices = services.objects()
	return render( request,  'services/index.html', {'servicesList': aListServices})

@login_required
def add(request):
	if request.method == 'POST':
		form = ServicesForm(request.POST) 
		if form.is_valid():
			# TODO do something :)
			form.save() 
			return HttpResponseRedirect('/index/')
	else:
		form =  CalandarsForm()
		return render(request, 'services/add.html', {'form': form})
