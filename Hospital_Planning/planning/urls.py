from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('planning.views',
	url(r'^$', 'current'),
	url(r'^current/?$', 'current'),
	url(r'^history/?$', 'history'),
	url(r'^auto_swap/(\d+)/?$', 'auto_swap'),
	url(r'^swap/(\d+)/?$', 'swap'),
	url(r'^swap_request_display/?$', 'swap_request_display'),
	url(r'^swap_request_accept/(\d+)/?$', 'swap_request_accept'),
	url(r'^avaibilities_view/?$', 'avaibilities_view'),
	url(r'^avaibilities_remove/(\d+)/?$', 'avaibilities_remove'),
	url(r'^import_planning/?$', 'import_planning'),
	#url(r'^generate/?$', 'generate'),
)
