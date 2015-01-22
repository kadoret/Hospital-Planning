'''
Created on Jan 22, 2015

@author: knguyen
'''
# Create your views here.
from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from planning.forms import  PlanningImportForm, PlanningForm, JobsForm,DaysForm,TimestampsForm
from planning.admin import DoctorCreationForm
from planning.models import planning

@login_required
def create_login(request):
    if request.method == 'POST':
        form = DoctorCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/planning/')
    else:
        form = DoctorCreationForm()
        return render(request, 'planning/admin/create_user.html', {'form': form})    
    
@login_required
def import_planning(request):
    if request.method == 'POST':
        form = PlanningImportForm(request.POST, request.FILES)
        if form.is_valid():
            (status, failed, updated, created ) = form.save(file = request.FILES['file'])
            message = "created : " + str(created) + ", failed: " + str(failed) + ", updated : " +  str(updated)
            new_form = PlanningImportForm()
            print message
            return render(request,'planning/admin/import_planning.html', {'form': new_form,
                                        'redirect' : True, 
                                        'status': status,
                                        'message': message})
    else:
        form = PlanningImportForm()
        return render(request, 'planning/admin/import_planning.html', {'form': form, 'redirect' : False})

@login_required
def create_planning(request):    
    if request.method == 'POST':
        form = PlanningForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/planning/view_planning')
    else:
        form = PlanningForm()
        return render(request, 'planning/admin/create_planning.html', {'form': form})

@login_required
def delete_planning(request, planning_id):
    aPlanning = planning.objects.get(id = planning_id)
    aPlanning.delete()
    return HttpResponseRedirect('/planning/view_planning')

@login_required
def create_jobs(request):
    if request.method == 'POST':
        form = JobsForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/planning/')        
    else:
        form = JobsForm()
        return render(request, 'planning/admin/create_jobs.html', {'form': form})

@login_required
def create_days(request):
    if request.method == 'POST':
        form = DaysForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/planning/')        
    else:
        form = DaysForm()
        return render(request, 'planning/admin/create_days.html', {'form': form})

@login_required
def create_timestamps(request):
    if request.method == 'POST':
        form = TimestampsForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/planning/')        
    else:
        form = TimestampsForm()
        return render(request, 'planning/admin/create_timestamps.html', {'form': form})
                              
@login_required
def view_planning(request):
    planning_list = planning.objects.all()
    paginator = Paginator(planning_list, 15)
    page = request.GET.get('page')
    try:
        planning_page = paginator.page(page)
    except PageNotAnInteger:
        planning_page = paginator.page(1)
    except EmptyPage:
        planning_page = paginator.page(paginator.num_pages)
    return  render(request, 'planning/admin/view_planning.html', {'planning_list': planning_page})
