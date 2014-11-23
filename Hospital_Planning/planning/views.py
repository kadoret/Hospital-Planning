# Create your views here.
from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from planning.models import planning, planning_swap, reserved_days
from planning.forms import PlanningSwapForm, PlanningImportForm, PlanningForm
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime, timedelta
import datetime
from  planning.extra.date_methods import isNewMonth, getFirstDayOfMonth, calendar


	
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
	# Return the personal calendar of the user 
	first = getFirstDayOfMonth(datetime.date.today())
	end = datetime.date.today() + timedelta( days = 360 )
	calendar_list = []
	calendar_month_list = []
	while first < end:
		if first < datetime.date.today():
			passed_date = True
		else:
			passed_date = False
		aPlanning = planning.objects.filter(pdoctor = request.user, day = first)
		aReserved = reserved_days.objects.filter(pdoctor = request.user, day = first)
		if aPlanning and aReserved:
			aReserved.delete()
		if not aPlanning and not aReserved:
			calendar_month_list.append(calendar(first,first.weekday(),0,passed_date,range(first.weekday())))
		elif aReserved:
			calendar_month_list.append(calendar(first,first.weekday(),2,passed_date,range(first.weekday())))
		else:
			calendar_month_list.append(calendar(first,first.weekday(),1,passed_date,range(first.weekday()),aPlanning))
		
		if isNewMonth(first, first + timedelta( days = 1 )):
			calendar_list.append(calendar_month_list)
			calendar_month_list=[]
		first = first +  timedelta( days = 1 )

	# pagination by month			
	paginator = Paginator(calendar_list, 1)
	page = request.GET.get('page')
	try:
		my_calandar_page = paginator.page(page)
	except PageNotAnInteger:
		# If page is not an integer, deliver first page.
		my_calandar_page = paginator.page(1)
	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
		my_calandar_page = paginator.page(paginator.num_pages)
	return render(request, 'planning/avaibilities.html', 
				{'calendar_list': my_calandar_page }) 

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
def auto_swap(request, planning_id):
	if request.method == 'POST':
		form = PlanningSwapForm(request.POST, doctor_id = request.user.id, planning_id = planning_id)
		if form.is_valid():
			form.save(doctor_id = request.user.id, planning_id = planning_id)
			return HttpResponseRedirect('/planning/calendar_view/')
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
	other_swap = planning_swap.objects.filter(doctor_to_swap = aSwap.doctor_to_swap, planning_to_swap = aSwap.planning_to_swap, accepted = False ).exclude(id = swap_id)
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
def validate_swap_display(request):
	swap_list =  planning_swap.objects.filter(accepted = True, validated = False)
	paginator = Paginator(swap_list, 15)
	page = request.GET.get('page')
	try:
		planning_page = paginator.page(page)
	except PageNotAnInteger:
		planning_page = paginator.page(1)
	except EmptyPage:
		planning_page = paginator.page(paginator.num_pages)		
	return  render(request, 'planning/swap_validation_display.html', {'swap_list': planning_page})

@login_required
def validate_swap(request, swap_id):
	try:
		aSwap = planning_swap.objects.get(id = swap_id)
		aSwap.planning_to_swap.pdoctor = aSwap.doctor_to_swap_with
		aSwap.planning_to_swap.official_approved = True
		aSwap.planning_to_swap_with.pdoctor = aSwap.doctor_to_swap
		aSwap.planning_to_swap_with.official_approved = True
		aSwap.planning_to_swap.save()
		aSwap.planning_to_swap_with.save()
		aSwap.validated = True
		aSwap.save()
		return HttpResponseRedirect('/planning/validate_swap_display')
	except ObjectDoesNotExist:
		return HttpResponseRedirect('/planning/validate_swap_display')

@login_required
def create(request):
	if request.method == 'POST':
		form = PlanningForm(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/planning/view')
	else:
		form = PlanningForm()
		return render(request, 'planning/create.html', {'form': form})

@login_required
def delete(request, planning_id):
	aPlanning = planning.objects.get(id = planning_id)
	aPlanning.delete()
	return HttpResponseRedirect('/planning/view')

@login_required
def swap(request):
	pass

@login_required
def view(request):
	planning_list = planning.objects.all()
	paginator = Paginator(planning_list, 15)
	page = request.GET.get('page')
	try:
		planning_page = paginator.page(page)
	except PageNotAnInteger:
		planning_page = paginator.page(1)
	except EmptyPage:
		planning_page = paginator.page(paginator.num_pages)
	return  render(request, 'planning/view.html', {'planning_list': planning_page})
