from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from services.model import jobs
from servicess.forms import JobsForm

@login_required
def job(request):
	aListServices = services.objects()
	return render( request,  'services/job.html', {'servicesList': aListServices})

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
