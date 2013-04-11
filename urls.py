from __future__ import absolute_import
from django.conf.urls import patterns, include, url

# http://stackoverflow.com/a/523366/412329
# from django.views.generic.simple import redirect_to
from django.views.generic import RedirectView, TemplateView

from .models import Entry
from .views import LogbookView, LinkedListView, LogbookArchiveView,\
LinkedListMonthArchive, LogbookDetailView, LinkedDetailView,\
LogbookMonthArchive, LogbookYearArchive, Search

from django.views.generic.dates import YearArchiveView

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    # hypertexthero.com/logbook/2013/01/entry-title
    url(r'^logbook/(?P<year>\d+)/(?P<month>\d{2})/(?P<slug>[\w-]+)/$',
        view=LogbookDetailView.as_view(),
        name="logbook-entry-detail"),

    # hypertexthero.com/logbook/2013/01/28/entry-title
    url(r'^linked/(?P<year>\d+)/(?P<month>\d{2})/(?P<day>\d{2})/(?P<slug>[\w-]+)/$',
        view=LinkedDetailView.as_view(),
        name="linked-entry-detail"),   

    # hypertexthero.com/archive
    url(r'^archive/$', 
        view=LogbookArchiveView.as_view(), 
        name='logbook-archive'),

    # hypertexthero.com/2013/01
    url(r'^(?P<year>\d+)/(?P<month>\d{2})/$', 
        view=LogbookMonthArchive.as_view(),
        name='archive-month'),

    # hypertexthero.com/2013    
    url(r'^(?P<year>\d+)/$',
        view=LogbookYearArchive.as_view(),
        name='archive-year'),

    # hypertexthero.com/linked/2013/january
    url(r'^linked/(?P<year>\d+)/(?P<month>[-\w]+)/$', 
        view=LinkedListMonthArchive.as_view(),
        name='linked-archive'),
    # hypertexthero.com/linked/ and hypertexthero.com/linked/#archive
    url(r'^linked/$', 
        view=LinkedListView.as_view(), 
        name='linked-list'),
    
    # hypertexthero.com/logbook
    url(r'^logbook/$', view=LogbookView.as_view(), name='logbook'),    
    
    # In addition to the following url pattern we are also using the 
    # built-in redirect app to redirect /linked/archive to /linked#archive
    url(r'^linked/(?P<year>\d+)/$', RedirectView.as_view(url='/linked#archive')),
    
)

urlpatterns += patterns('views',
    # flatpage urls such as /about are served as per django.contrib.flatpages.urls    
    url(r'^work/(?P<slug>[-\w]+)$', TemplateView.as_view(
            template_name='work.html'), name='work-detail'),
    
    url(r'^contact/', include("contact.urls", namespace="contact_form")),
    url(r'^search/$', Search, name="search"),
    
    # =homepage
    url(r'^$', TemplateView.as_view(template_name='home.html'), name="home"),
)

# http://docs.djangoproject.com/en/dev/howto/static-files/#serving-static-files-in-development
from django.conf import settings

if settings.DEBUG :
    urlpatterns += patterns('',
        url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT, 'show_indexes': True}),
        url(r'^static/files/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
    )