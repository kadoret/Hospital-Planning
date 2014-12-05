from django.conf.urls import patterns, include, url
from django.contrib.auth.views import password_change
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('planning.views',
	url(r'^$', 'hospital_login'),
	url(r'^auto_swap_request/(\d+)/?$', 'auto_swap'),
	url(r'^swap_request/(\d+)/?$', 'swap'),
	url(r'^swap_request_display/?$', 'swap_request_display'),
	url(r'^validate_swap_display/?$', 'validate_swap_display'),
	url(r'^validate_swap/(\d+)/?$', 'validate_swap'),
	url(r'^my_swap_request_display/?$', 'my_swap_request_display'),
	url(r'^accept_swap/(\d+)/?$', 'accept_swap'),
	url(r'^cancel_swap/(\d+)/?$', 'cancel_swap'),
	url(r'^reserved_day_add/(\d{4})/(\d{2})/(\d{2})/?$', 'reserved_day_add'),
	url(r'^reserved_day_remove/(\d{4})/(\d{2})/(\d{2})/?$', 'reserved_day_remove'),
	url(r'^calendar_view/?$', 'calendar_view'),
	url(r'^import_planning/?$', 'import_planning'),
	url(r'^view/?$', 'view'),
	url(r'^create/?$', 'create'),
	url(r'^delete/(\d+)/?$', 'delete'),
	url(r'^login/?$', 'hospital_login'),
	url(r'^logout/?$', 'hospital_logout'),
	url(r'^change/?$', password_change,{'template_name':'planning/password.html' ,'post_change_redirect': 'hospital_password_change'}),
)
