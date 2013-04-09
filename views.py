import functools
# https://docs.djangoproject.com/en/1.4/topics/generic-views-migration/
# from django.views.generic import dates
# http://ccbv.co.uk/projects/Django/1.5/django.views.generic.list/MultipleObjectMixin/
from django.views.generic.list import MultipleObjectMixin
# http://ccbv.co.uk/projects/Django/1.5/django.views.generic.dates/ArchiveIndexView/
from django.views.generic import ArchiveIndexView
from django.core.urlresolvers import reverse

from .models import Entry

# http://stackoverflow.com/q/8547880/412329
class LogbookView(ArchiveIndexView):
    """
    Logbook homepage - Extends the ArchiveIndexView view to add entries to the context
    """
    model = Entry
    date_field = 'pub_date' # don't forget to set {{ note.created|date:"d F Y" }} in notes/list.html
    template_name = 'hth/logbook.html'
    allow_future = False
    def get_context_data(self, **kwargs):
        context = super(LogbookView, self).get_context_data(**kwargs)
        context['entries'] = Entry.objects.filter(is_active=True
                                                    ).order_by('-pub_date', 'title')[:30]
        # context['comments'] = Comment.objects.filter(allow=True).order_by('created').reverse()[:4]
        return context

class LinkedListView(ArchiveIndexView):
    """ 
    Linked list (kind == Link)
        Extends the ArchiveIndexView view to add entries to the context
    """
    model = Entry
    date_field = 'pub_date' # don't forget to set {{ note.created|date:"d F Y" }} in notes/list.html
    template_name = 'hth/linked.html'
    allow_future = False
    def get_context_data(self, **kwargs):
        context = super(LinkedListView, self).get_context_data(**kwargs)
        context['latest'] = Entry.objects.filter(is_active=True, kind='L').order_by('-pub_date', 'title')[:30]
        # context['comments'] = Comment.objects.filter(allow=True).order_by('created').reverse()[:4]
        return context

class LogbookArchiveView(ArchiveIndexView):
    """
        Archive of original entries (kind == Article) - 
            Extends the ArchiveIndexView view to add entries to the context
    """
    model = Entry
    date_field = 'pub_date' # don't forget to set {{ note.created|date:"d F Y" }} in notes/list.html
    template_name = 'hth/archive.html'
    allow_future = False
    def get_context_data(self, **kwargs):
        context = super(LogbookArchiveView, self).get_context_data(**kwargs)
        context['latest'] = Entry.objects.filter(is_active=True, kind='A').order_by('-pub_date', 'title')[:9999]
        # context['comments'] = Comment.objects.filter(allow=True).order_by('created').reverse()[:4]
        return context


# =Search

# from django.http import HttpResponse 
# from django.template import loader, Context
# 
# def search(request): 
#     query = request.GET['q']
#     results = Note.objects.filter(content_html__icontains=query)
#     template = loader.get_template('hth/search.html')
#     context = Context({ 'query': query, 'results': results })
#     response = template.render(context)
#     return HttpResponse(response)

# or use django's render_to_response shortcut:

from django.shortcuts import render_to_response
from django.db.models import Q
from django.template import RequestContext # http://stackoverflow.com/a/5478944/412329

# def search(request):
#     query = request.GET['q']
#     return render_to_response('hth/search.html',
#         {   'query': query, 
#             'results': Note.objects.filter(content_html__icontains=query) })

# rewritten so /search/ URL can be accessed directly:

def search(request):    
    query = request.GET.get('q', '') # both /search/ and /search/?q=query work
    results = []
    # http://stackoverflow.com/a/4338108/412329 - passing the user variable into the context
    user = request.user
    if query:
        # INSTEAD OF THIS:
        # title_results = Note.objects.filter(title__icontains=query)
        # results = Note.objects.filter(content_html__icontains=query)
        # DO THIS avoid duplicate results when query word is both in title and content_html:
        # http://stackoverflow.com/questions/744424/django-models-how-to-filter-out-duplicate-values-by-pk-after-the-fact
        results = Entry.objects.filter(Q(title__icontains=query)|Q(body_html__icontains=query)).distinct()
    return render_to_response('hth/search.html',
        {   'query': query, 
            'results': results,
            'user': user
             }, context_instance=RequestContext(request)) # http://stackoverflow.com/a/5478944/412329