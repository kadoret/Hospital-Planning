from django.shortcuts import render
from calandars.model import Calandars

def index(request):
	aListCalandars = calandars.objects()
	return render( request,  'calandars/index.html', {'calandarsList': aListCalandars})

def add(request):
	if request.method == 'POST':
		form = CalandarsForm(request.POST) 
		if form.is_valid(): 
			return HttpResponseRedirect('/index/')
	else: 
		form =  CalandarsForm()
		return render(request, 'calandars/add.html', {'form': form,})
