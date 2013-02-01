from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from services.models import jobs, doctors, days, timestamps#, doctors_jobs
from services.form import doctorForm

class DoctorAdmin(admin.ModelAdmin):
	form = doctorForm

#admin.site.unregister(User)
admin.site.unregister(Site)

admin.site.register(jobs)
admin.site.register(days)
admin.site.register(doctors, DoctorAdmin)
admin.site.register(timestamps)
#admin.site.register(doctors_jobs)
