# Create your views here.
from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from planning.models import planning, planning_swap, reserved_days
from planning.forms import PlanningSwapForm, PlanningImportForm
from datetime import datetime, timedelta
import datetime


class calendar:
	def __init__(self, day, description):
		self.day = day
		self.description = description	
	
@login_required
def reserved_day_add(request, year, month, day):
	aDay = datetime.date(int(year),int(month),int(day))
	page = request.GET.get('page')
	reserved_days.objects.create(day = aDay, pdoctor_id = request.user.id)
	return HttpResponseRedirect('/planning/calendar_view?page='+ str(page))

@login_required
def reserved_day_remove(request, year, month, day):
	aDay = datetime.date(int(year),int(month),int(day))
	page = request.GET.get('page')
	object_to_remove = reserved_days.objects.get(day = aDay, pdoctor_id = request.user.id)
	object_to_remove.delete()
	return HttpResponseRedirect('/planning/calendar_view?page='+ str(page))

@login_required
def calendar_view(request):
	#get working day
	day_begin =  datetime.date.today()
	day_end = datetime.date.today() + timedelta( days = 360 )
	calendar_list = []

	while day_begin < day_end:
		aPlanning = planning.objects.filter(pdoctor = request.user, day = day_begin)
		aReserved = reserved_days.objects.filter(pdoctor = request.user, day = day_begin)
		if aPlanning and aReserved:
			aReserved.delete()
		if not aPlanning and not aReserved:
			calendar_list.append(calendar(day_begin, 0))
		elif aReserved:
			calendar_list.append(calendar(day_begin, 2))
		else:
			calendar_list.append(calendar(day_begin, 1))
		day_begin = day_begin +  timedelta( days = 1 )
				
	paginator = Paginator(calendar_list, 15)
	page = request.GET.get('page')
	print page
	try:
		my_calandar_page = paginator.page(page)
	except PageNotAnInteger:
        # If page is not an integer, deliver first page.
		my_calandar_page = paginator.page(1)
	except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
		my_calandar_page = paginator.page(paginator.num_pages)
	return render(request, 'planning/avaibilities.html', {'calendar_list': my_calandar_page}) 

@login_required
def import_planning(request):
	if request.method == 'POST':
		form = PlanningImportForm(request.POST, request.FILES)
		if form.is_valid():
			(status, failed, updated, created ) = form.save(file = request.FILES['file'])
			message = "created : " + str(created) + ", failed: " + str(failed) + ", updated : " +  str(updated)
			new_form = PlanningImportForm()
			print message
			return render(request,'planning/import.html', {'form': new_form,
										'redirect' : True, 
										'status': status,
										'message': message})
	else:
		form = PlanningImportForm()
		return render(request, 'planning/import.html', {'form': form, 'redirect' : False})

@login_required
def my_planning_view(request, old = '0'):
	if old == '0':
		aPlanningList = planning.objects.filter(
						pdoctor = request.user,
						day__range = [ datetime.date.today(),
								datetime.date.today() + timedelta( days = 360 ) ])
		
		paginator = Paginator(aPlanningList, 15)
		page = request.GET.get('page')
		try:
			planning_page = paginator.page(page)
		except PageNotAnInteger:
			planning_page = paginator.page(1)
		except EmptyPage:
			planning_page = paginator.page(paginator.num_pages)
		return render(request, 'planning/planning_view.html', {'current_planning': planning_page, 'old': False})

	else:
		aPlanningList = planning.objects.filter(pdoctor = request.user
							).exclude( day__range = [ datetime.date.today(),
										  datetime.date.today() + timedelta( days = 360 )])
	paginator = Paginator(aPlanningList, 15)
	page = request.GET.get('page')
	try:
		planning_page = paginator.page(page)
	except PageNotAnInteger:
		planning_page = paginator.page(1)
	except EmptyPage:
		planning_page = paginator.page(paginator.num_pages)
	return render (request, 'planning/planning_view.html', {'current_planning': planning_page, 'old': True})

@login_required
def auto_swap(request, planning_id):
	if request.method == 'POST':
		form = PlanningSwapForm(request.POST, doctor_id = request.user.id, planning_id = planning_id)
		if form.is_valid():
			form.save(doctor_id = request.user.id, planning_id = planning_id)
			return HttpResponseRedirect('/planning/my_planning_view/0')
	else:
		
		form = PlanningSwapForm(doctor_id = request.user.id, planning_id =  planning_id)
		return render(request, 'planning/auto_swap.html', {'form': form})

@login_required
def swap_request_display(request):
	aPlanningList = planning_swap.objects.filter( doctor_to_swap_with_id = request.user,
							date__range = [ datetime.date.today(),
									 datetime.date.today() + timedelta( days = 360 )])
	return render(request, 'planning/swap_request_display.html', {'planning_list': aPlanningList, 'my' : False})

@login_required
def my_swap_request_display(request):
	aPlanningList = planning_swap.objects.filter( doctor_to_swap_id = request.user,
							date__range = [ datetime.date.today(),
									datetime.date.today() + timedelta( days = 360 )])
	return render(request, 'planning/swap_request_display.html', {'planning_list': aPlanningList, 'my' : True})

@login_required
def cancel_swap(request, swap_id):
	aSwap = planning_swap.objects.get(id = swap_id)
	if not planning_swap.objects.filter(date = aSwap.date, doctor_to_swap_id = aSwap.doctor_to_swap.id, accepted = False ).exclude(id = swap_id):
		aSwap.planning_to_swap.official_approved = True
		aSwap.planning_to_swap.request_swap = False
		aSwap.planning_to_swap.save()
	aSwap.delete()
	return HttpResponseRedirect('/planning/my_swap_request_display')

@login_required
def accept_swap(request, swap_id):
	aSwap = planning_swap.objects.get(id = swap_id)
	# remove if exist other swap request
	other_swap = planning_swap.objects.filter(date = aSwap.date, doctor_to_swap_id = aSwap.doctor_to_swap.id, accepted = False ).exclude(id = swap_id)
	for swap in other_swap:
		swap.delete()
	# update planning
	user1_planning = planning.objects.get(id = aSwap.planning_to_swap.id)
	user1_planning.request_swap = False
	user1_planning.official_approved = False
	user1_planning.save()
	
	user2_planning = planning.objects.get(id = aSwap.planning_to_swap_with.id)
	user2_planning.request_swap = False
	user2_planning.official_approved = False
	user2_planning.save()
	
	aSwap.accepted = True
	aSwap.save()
	
	return HttpResponseRedirect('/planning/swap_request_display')

@login_required
#TODO
def swap(request):
	pass
