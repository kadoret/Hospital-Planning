from django.conf.urls import patterns, include, url
from django.contrib.auth.views import password_change

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('services.views',
	url(r'^$', 'hospital_login'),
	url(r'^login/?$', 'hospital_login'),
	url(r'^logout/?$', 'hospital_logout'),
	url(r'^change/?$', password_change,{'template_name':'services/password.html' ,'post_change_redirect': 'hospital_password_change'}),
	#url(r'^generate/?$', 'generate'),
)
