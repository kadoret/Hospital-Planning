from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('planning.views',
	url(r'^$', 'my_planning_view'),
	url(r'^my_planning_view/(\d+)/?$', 'my_planning_view'),
	url(r'^auto_swap_request/(\d+)/?$', 'auto_swap'),
	url(r'^swap_request/(\d+)/?$', 'swap'),
	url(r'^swap_request_display/?$', 'swap_request_display'),
	url(r'^my_swap_request_display/?$', 'my_swap_request_display'),
	url(r'^accept_swap/(\d+)/?$', 'accept_swap'),
	url(r'^cancel_swap/(\d+)/?$', 'cancel_swap'),
	url(r'^reserved_day_add/(\d{4})/(\d{2})/(\d{2})/?$', 'reserved_day_add'),
	url(r'^reserved_day_remove/(\d{4})/(\d{2})/(\d{2})/?$', 'reserved_day_remove'),
	url(r'^calendar_view/?$', 'calendar_view'),
	url(r'^import_planning/?$', 'import_planning'),
	#url(r'^generate/?$', 'generate'),
)
