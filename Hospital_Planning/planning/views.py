# Create your views here.
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from planning.models import Planning
from planning.forms import PlanningChangeForm
from datetime import datetime

@login_required
def index(request):
	aPlanningList = Planning.objects.filter(puser=request.user).exclude(day < datetime.date.today())
	render (request, 'planning/index.html', {'current_planning': aPlanningList})

@login_required
def old_index(request):
	aPlanningList = Planning.objects.filter(puser=request.user).exclude(day>datetime.date.today())
	render (request, 'planning/index.html', {'current_planning': aPlanningList})

@login_required
def change_planning(request, service, timestamp):
	if request.method == 'POST':
		form = PlanningChangeForm(request.POST)
		if form.is_valid():
			form.requestPlanningSwap()
			return HttpResponseRedirect('/index/')
	else:
		form = PlanningChangeForm(request.user, service, timestamp)
		return render(request, 'planning/change.html', {'form': form})

@login_required
def dates_to_change(request):
	if request.method == 'POST':
		pass
	else:
		pass	
