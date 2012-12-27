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
def swap(request, service, timestamp):
	if request.method == 'POST':
		form = PlanningSwapForm(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/planning/my_planning')
	else:
		
		form = PlanningSwapForm(**{'user_id': request.user,	
						'service_id': service, 
						'timestamp_id': timestama})

		return render(request, 'planning/swap.html', {'form': form})
