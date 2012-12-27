# Create your views here.
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from planning.models import Planning
from planning.forms import PlanningSwapForm
from datetime import datetime

@login_required
def all(request):
	aPlanningList = Planning.objects.filter(
						puser = request.user
							).exclude( day < datetime.date.today() )
	render (request, 'planning/all.html', {'current_planning': aPlanningList})

@login_required
def old(request):
	aPlanningList = Planning.objects.filter(
						puser = request.user
							).exclude( day > datetime.date.today() )
	render (request, 'planning/all.html', {'current_planning': aPlanningList})

@login_required
def swap_planning(request, service, timestamp):
	if request.method == 'POST':
		form = PlanningSwapForm(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/index/')
	else:
		form = PlanningSwapForm(request.user, service, timestamp)
		return render(request, 'planning/change.html', {'form': form})
