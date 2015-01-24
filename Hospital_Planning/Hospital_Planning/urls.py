from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

	url(r'^planning/', include('planning.urls')),
	url(r'^$' , include('planning.urls')),
	#url(r'^blog/', include('blog.urls')),
#	url(r'^login/', include('services.urls')),
#	url(r'^logout/', include('services.urls')),
	#url(r'^service/', include('services.urls')),
	#url(r'^accueil/', include('blog.urls')),
	#url(r'^mail/', include('mail.urls')),

    # Examples:
    # url(r'^$', 'Hospital_Planning.views.home', name='home'),
    # url(r'^Hospital_Planning/', include('Hospital_Planning.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    #	url(r'^admin/', include(admin.site.urls)),
)
