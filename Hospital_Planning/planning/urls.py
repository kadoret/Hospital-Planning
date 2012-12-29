from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('planning.views',

	url(r'^current/?$', 'current'),
	url(r'^history/?$', 'history'),
	url(r'^auto_swap/(\d+)/?$', 'auto_swap'),
	url(r'^swap/(\d+)/?$', 'swap'),
	#url(r'^generate/?$', 'generate'),
)
