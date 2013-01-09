from __future__ import absolute_import
from django.conf.urls import patterns, include, url

from .models import Entry
from . import views

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from django.views.generic import DetailView, MonthArchiveView

urlpatterns = patterns('',
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    
    # linked list detail - hypertexthero.com/linked/2013/january/01/entry-title
    # url(r'^linked/(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\d{2})/$', 'hth.views.linked_archive_day', name='linked-archive-day'),
    
    # linked list archive month - hypertexthero.com/linked/2013/january
    # this doesn't fucking work
    # url(r'^linked/(?P<year>\d+)/(?P<month>[a-z]{3})/$', 'hth.views.linked_archive', name='linked-archive'),
    
    url(r'^linked/(?P<year>\d+)/(?P<month>[a-z]{3})/$', 
            MonthArchiveView.as_view(
                model=Entry, 
                date_field='pub_date', 
                template_name='hth/linked_archive.html',
                queryset=Entry.objects.filter(kind='L').order_by('-pub_date', 'title')), 
            name='linked-archive'),

    # logbook entry detail - hypertexthero.com/logbook/2013/january/entry-title
    url(r'^logbook/(?P<year>\d+)/(?P<month>[-\w]+)/(?P<slug>[\w-]+)/$',
        DetailView.as_view(model=Entry),
        name="logbook-entry-detail"),

    
    # hypertexthero.com/linked/#archive
    
    # linked list index hypertexthero.com/linked/ and hypertexthero.com/linked/#archive - will need template tag?
    url(r'^linked/$', 'hth.views.linked', name='linked'),

    # logbook original articles - hypertexthero.com/archive/
    url(r'^archive/$', 'hth.views.logbook_archive', name='archive'),
    
    # logbook index - hypertexthero.com/logbook/
    url(r'^logbook/$', 'hth.views.logbook', name='logbook'),    
)

urlpatterns += patterns('django.views.generic.simple',
    
    url(r'^search/$', views.search, name="search"),

    # note that flatpage urls such as /about/ are served as per django.contrib.flatpages.urls    
    # url(r'^about/$', 'direct_to_template', {'template': 'about.html'}),
    # todo - contact form
    # url(r'^contact/$', 'direct_to_template', {'template': 'contact.html'}),
    url(r'^work/(?P<slug>[-\w]+)$', 'direct_to_template', {'template': 'work.html'}, name='work-detail'),    
    
    # homepage and work index - hypertexthero.com/
    url(r'^$', 'direct_to_template', {'template': 'home.html'}, name="home"),
    
)

# http://docs.djangoproject.com/en/dev/howto/static-files/#serving-static-files-in-development
from django.conf import settings

if settings.DEBUG :
    urlpatterns += patterns('',
        url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT, 'show_indexes': True}),
        url(r'^static/files/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
    )