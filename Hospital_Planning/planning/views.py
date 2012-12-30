# Create your views here.
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from planning.models import Planning
from planning.forms import PlanningSwapForm
from datetime import datetime
import datetime

@login_required
def current(request):
	aPlanningList = Planning.objects.filter(
						puser = request.user
							).exclude( day = datetime.date.today() )
	return render(request, 'planning/current.html', {'current_planning': aPlanningList})

@login_required
def history(request):
	aPlanningList = Planning.objects.filter(
						puser = request.user
							).exclude( day > datetime.date.today() )
	return render (request, 'planning/history.html', {'current_planning': aPlanningList})

@login_required
def auto_swap(request, planning_id):
	if request.method == 'POST':
		print request.POST
		form = PlanningSwapForm(request.POST, user_id = request.user.id,planning_id = planning_id)
		print form
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/planning/current')
	else:
		
		form = PlanningSwapForm(user_id = request.user.id, planning_id =  planning_id)
		print form
		return render(request, 'planning/auto_swap.html', {'form': form})

@login_required
def swap(request):
	pass
