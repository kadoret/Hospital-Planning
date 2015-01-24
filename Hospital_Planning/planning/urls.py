from django.conf.urls import patterns, include, url
from django.contrib.auth.views import password_change
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('planning.view',
	url(r'^$', 'views_connexion.login'),
	url(r'^auto_swap_request/(\d+)/?$', 'views_functional.auto_swap'),
	url(r'^swap_request/(\d+)/?$', 'views_functional.swap'),
	url(r'^swap_request_display/?$', 'views_functional.swap_request_display'),
	url(r'^validate_swap_display/?$', 'views_functional.validate_swap_display'),
	url(r'^validate_swap/(\d+)/?$', 'views_functional.validate_swap'),
	url(r'^my_swap_request_display/?$', 'views_functional.my_swap_request_display'),
	url(r'^accept_swap/(\d+)/?$', 'views_functional.accept_swap'),
	url(r'^cancel_swap/(\d+)/?$', 'views_functional.cancel_swap'),
	url(r'^reserved_day_add/(\d{4})/(\d{2})/(\d{2})/?$', 'views_functional.reserved_day_add'),
	url(r'^reserved_day_remove/(\d{4})/(\d{2})/(\d{2})/?$', 'views_functional.reserved_day_remove'),
	url(r'^view_calendar/?$', 'views_functional.view_calendar'),

	url(r'^login/?$', 'views_connexion.login'),
	url(r'^logout/?$', 'views_connexion.logout_'),
	
	url(r'^admin/view_planning/?$', 'views_admin.view_planning'),
	url(r'^admin/create_planning/?$', 'views_admin.create_planning'),
	url(r'^admin/create_days/?$', 'views_admin.create_days'),
	url(r'^admin/create_jobs/?$', 'views_admin.create_jobs'),
	url(r'^admin/create_timestamps/?$', 'views_admin.create_timestamps'),
	url(r'^admin/delete_planning/(\d+)/?$', 'views_admin.delete_planning'),
	url(r'^admin/import_planning/?$', 'views_admin.import_planning'),
	url(r'^admin/create_login/?$', 'views_admin.create_login'),
	
	url(r'^change/?$', password_change,{'template_name':'planning/password.html' ,'post_change_redirect': 'hospital_password_change'}),
)
