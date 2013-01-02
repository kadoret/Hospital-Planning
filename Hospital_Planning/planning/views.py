# Create your views here.
from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from planning.models import planning
from planning.forms import PlanningSwapForm
from datetime import datetime, timedelta
import datetime

@login_required
def avaibilities_remove(request, avaibilities_id):
	if avaibilities.objects.get(id = avaibilities_id).pdoctor == request.user:
		avaibilities.objects.get(id = avaibilities_id).delete()
	#TODO error message if it's not the right user
	return HttpResponseRedirect('/planning/avaibilities_view')

@login_required
def avaibilities_view(request):
	avaibilities_list = avaibilities.objects.filter(pdoctor = request.user,
							day__range = [ datetime.date.today(),
									datetime.date.today() + timedelta( days = 360 ) ])
	return render(request, 'planning/ avaibilities.html', {'avaibilities_list': avaibilities_list}) 

@login_required
def import_planning(request):
	if request.method == 'POST':
		form = PlanningImportForm(request.POST, request.FILES)
		if form.is_valid():
			handle_uploaded_planning(request.FILES['file'])
			return HttpResponseRedirect('/planning/current')
	else:
		form = PlanningImportForm()
		return render(request, 'planning/import.html', {'form': form})

@login_required
def current(request):
	aPlanningList = planning.objects.filter(
						pdoctor = request.user,
						day__range = [ datetime.date.today(),
								datetime.date.today() + timedelta( days = 360 ) ])
	return render(request, 'planning/current.html', {'current_planning': aPlanningList})

@login_required
def history(request):
	aPlanningList = planning.objects.filter(
						puser = request.user
							).exclude( day__range = [ datetime.date.today(),
										  datetime.date.today() + timedelta( days = 360 )])
	return render (request, 'planning/history.html', {'current_planning': aPlanningList})

@login_required
def auto_swap(request, planning_id):
	if request.method == 'POST':
		form = PlanningSwapForm(request.POST, doctor_id = request.user.id, planning_id = planning_id)
		if form.is_valid():
			form.save(doctor_id = request.user.id, planning_id = planning_id)
			return HttpResponseRedirect('/planning/current')
	else:
		
		form = PlanningSwapForm(doctor_id = request.user.id, planning_id =  planning_id)
		return render(request, 'planning/auto_swap.html', {'form': form})

@login_required
def swap_request_display(request):
	aPlanningList = planning_swap.objects.filter( doctor_to_swap_with_id = request.user,
							day__range = [ datetime.date.today(),
									 datetime.date.today() + timedelta( days = 360 )])
	return render(request, 'planning/swap_request_display.html', {'planning_list': aPlanningList}) 

@login_required
def swap_request_accept(request, swap_id):
	aSwap = planning_swap.objects.get(id = swap_id)
	planning.objects.get(id = aSwap.doctor_to_swap_id).update(doctor_id = aSwap.doctor_to_swap_with_id)
	aSwap.delete()
	return HttpResponseRedirect('/planning/swap_request_display')

@login_required
#TODO
def swap(request):
	pass
