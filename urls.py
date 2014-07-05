from __future__ import absolute_import
from django.conf.urls import patterns, include, url

from django.conf import settings
from django.conf.urls.static import static

# http://stackoverflow.com/a/523366/412329
# from django.views.generic.simple import redirect_to
from django.views.generic import RedirectView, TemplateView

from .models import Entry
from .views import LogbookView, LinkedListView, LogbookArchiveView,\
LinkedListMonthArchive, LogbookDetailView, LinkedDetailView,\
LogbookMonthArchive, LogbookYearArchive, Search, RssLogbookFeed, AtomLogbookFeed

from django.views.generic.dates import YearArchiveView

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

# https://github.com/justquick/django-math-captcha
from contact_form.views import ContactFormView
from contact_form.forms import ContactForm
# from math_captcha.forms import MathCaptchaForm

# class CaptchaContactForm(ContactForm,MathCaptchaForm):
#     pass

urlpatterns = patterns('',
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    # =Mozilla =Persona authentication
    url(r'^browserid/', include('django_browserid.urls')),
    
    url(r'^taggit_autosuggest/', include('taggit_autosuggest.urls')),

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
    url(r'^linked/(?P<year>\d+)/(?P<month>\d{2})/$',
        view=LinkedListMonthArchive.as_view(),
        name='linked-archive'),
    # hypertexthero.com/linked/ and hypertexthero.com/linked/#archive
    url(r'^linked/$', 
        view=LinkedListView.as_view(), 
        name='linked-list'),
    
    # hypertexthero.com/logbook
    url(r'^logbook/$', view=LogbookView.as_view(), name='logbook'),    
    
    # contact
    url(r'^contact/$', view=ContactFormView.as_view(form_class=CaptchaContactForm), name='contact_form'),
    url(r'^contact/sent/$', TemplateView.as_view(template_name='contact_form/contact_form_sent.html'), name='contact_form_sent'),
    
    # In addition to the following url pattern we are also using the 
    # built-in redirect app to redirect /linked/archive to /linked#archive
    url(r'^linked/(?P<year>\d+)/$', RedirectView.as_view(url='/linked#archive')),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += patterns('views',
    
# # flatpage urls such as /about are served as per django.contrib.flatpages.urls
# # Superfluous, and if we keep this, append_slashes doest not work:
# url(r'^work/(?P<slug>[-\w]+)$', TemplateView.as_view(
#         template_name='flatpages/default.html'), name='work-detail'),

    # url(r'^contact/', include("contact_form.urls")),
    url(r'^search/$', Search, name="search"),

    # Feeds
    url(r'^logbook/rss/$', RssLogbookFeed()),
    url(r'^logbook/atom/$', AtomLogbookFeed()),
    
    # Robots
    url(r'^robots\.txt$', TemplateView.as_view(
        template_name='robots.txt', content_type='text/plain')),
    
    # =homepage
    url(r'^$', TemplateView.as_view(template_name='home.html'), name="home"),

    # =404 for testing
    # url(r'^error/$', TemplateView.as_view(template_name='404.html'), name="error"),

)


# sitemap.xml - https://docs.djangoproject.com/en/dev/ref/contrib/sitemaps/
# http://stackoverflow.com/questions/14169976/google-doesnt-accept-my-django-sitemap
from django.contrib.sitemaps import FlatPageSitemap, GenericSitemap

info_dict = {
    'queryset': Entry.objects.all(),
    'date_field': 'pub_date',
}
sitemaps = {
    'flatpages': FlatPageSitemap,
    'logbook': GenericSitemap(info_dict, priority=0.6),
}

urlpatterns += patterns('',
    # the sitemap
    url(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', 
        {'sitemaps': sitemaps}),
)


# http://docs.djangoproject.com/en/dev/howto/static-files/#serving-static-files-in-development
from django.conf import settings

if settings.DEBUG :
    urlpatterns += patterns('',
        url(r'^static/(?P<path>.*)$', 'django.views.static.serve', 
            {'document_root': settings.STATIC_ROOT, 'show_indexes': True}),
        url(r'^static/files/(?P<path>.*)$', 'django.views.static.serve', 
            {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
    )