import functools
# https://docs.djangoproject.com/en/1.4/topics/generic-views-migration/
# http://ccbv.co.uk/projects/Django/1.5/django.views.generic.list/MultipleObjectMixin/
# http://ccbv.co.uk/projects/Django/1.5/django.views.generic.dates/ArchiveIndexView/
from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Atom1Feed

from django.views.generic.list import MultipleObjectMixin
from django.views.generic import ArchiveIndexView, MonthArchiveView, YearArchiveView, DetailView
from django.core.urlresolvers import reverse

from django.contrib.flatpages.models import FlatPage
from .models import Entry

# =home, =list views ===================================

# http://stackoverflow.com/questions/8547880/listing-object-with-specific-tag-using-django-taggit
class LogbookView(ArchiveIndexView):
    """
    Logbook Homepage
        Extends the ArchiveIndexView view to add entries to the context
    """
    model = Entry
    date_field = 'pub_date' 
    template_name = 'hth/logbook.html'
    allow_future = False
    queryset = Entry.objects.filter(
            is_active=True).order_by('-pub_date', 'title')
# https://docs.djangoproject.com/en/1.5/topics/class-based-views/generic-display/#adding-extra-context
    # def get_context_data(self, **kwargs):
    #     context = super(LogbookView, self).get_context_data(**kwargs)
    #     context['latest'] = Entry.objects.filter(
    #         is_active=True).order_by('-pub_date', 'title')[:30]
    #     return context

class LinkedListView(ArchiveIndexView):
    """ 
    Linked List (kind == Link)
        Extends the ArchiveIndexView view to add entries to the context
    """
    model = Entry
    date_field = 'pub_date'
    template_name = 'hth/linked.html'
    allow_future = False
    queryset = Entry.objects.filter(
            is_active=True, kind="L").order_by('-pub_date', 'title')
    # def get_context_data(self, **kwargs):
    #     context = super(LinkedListView, self).get_context_data(**kwargs)
    #     context['latest'] = Entry.objects.filter(
    #         is_active=True, kind='L').order_by('-pub_date', 'title')[:30]
    #     return context


# =feeds ===================================

# http://stackoverflow.com/a/250373/412329
def smart_truncate(content, length=200, suffix='...'):
    if len(content) <= length:
        return content
    else:
        # return ' '.join(content[:length+1].split(' ')[0:-1]) + suffix
        return content[:length].rsplit(' ', 1)[0]+suffix

class RssLogbookFeed(Feed):
    title = "Hypertexthero Logbook by Simon Griffee"
    link = "/logbook/"
    description = "Writing and links on web, design and simplicity by Simon Griffee"
    # description_template = "hth/feed_description.html" # using default for now

    def items(self):
        return Entry.objects.order_by('-pub_date')[:15]

    def item_title(self, item):
        return item.title

    def item_pubdate(self, item):
        return item.pub_date

    def item_description(self, item):
        return smart_truncate(item.body_html)

class AtomLogbookFeed(RssLogbookFeed):
    feed_type = Atom1Feed
    subtitle = RssLogbookFeed.description


# =single pages ===================================

class LogbookDetailView(DetailView):
    """ Article permalink page """
    model = Entry

class LinkedDetailView(DetailView):
    """ Link permalink page """
    model = Entry
        

# =archives ===================================

class LogbookArchiveView(ArchiveIndexView):
    """
        Archive of original entries (kind == Article) - 
            Extends the ArchiveIndexView view to add entries to the context
    """
    model = Entry
    date_field = 'pub_date'
    template_name = 'hth/archive.html'
    allow_future = False
    queryset = Entry.objects.filter(
          is_active=True, kind='A').order_by('-pub_date', 'title')

class LinkedListMonthArchive(MonthArchiveView):
    """Linked List monthly archives"""
    model = Entry
    date_field = 'pub_date'
    month_format='%m'
    template_name = 'hth/linked_archive.html'
    allow_future = False
    queryset = Entry.objects.filter(
          is_active=True, kind='L').order_by('-pub_date', 'title')

class LogbookMonthArchive(MonthArchiveView):
    """Monthly archives of articles"""
    model = Entry
    date_field = 'pub_date'
    month_format='%m'
    template_name = 'hth/archive_month.html'
    allow_future = False
    queryset = Entry.objects.filter(
          is_active=True, kind='A').order_by('-pub_date', 'title')

class LogbookYearArchive(YearArchiveView):
    """Yearly archives of articles"""
    model = Entry
    date_field = 'pub_date'
    year_format='%Y'
    make_object_list=True, 
    template_name = 'hth/archive_year.html'
    allow_future = False
    queryset = Entry.objects.filter(
          is_active=True, kind='A').order_by('-pub_date', 'title')


# =Search ===================================

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
# http://stackoverflow.com/a/5478944/412329
from django.template import RequestContext 
# def search(request):
#     query = request.GET['q']
#     return render_to_response('hth/search.html',
#         {'query': query, 
#          'results': Note.objects.filter(content_html__icontains=query) })

# rewritten so /search/ URL can be accessed directly:

# http://stackoverflow.com/questions/744424/django-models-how-to-filter-out-duplicate-values-by-pk-after-the-fact
from itertools import chain

def Search(request):    
    query = request.GET.get('q', '') # both /search/ and /search/?q=query work
    entry_list = []
    work_list = []
    result_list = list(chain(entry_list, work_list))
    # http://stackoverflow.com/a/4338108/412329 - 
        # passing the user variable into the context
    user = request.user
    if query:
        # INSTEAD OF THIS:
        # title_results = Note.objects.filter(title__icontains=query)
        # results = Note.objects.filter(content_html__icontains=query)
        # DO THIS avoid duplicate results when query word is both in title 
            # and content_html:
# http://stackoverflow.com/questions/744424/django-models-how-to-filter-out-duplicate-values-by-pk-after-the-fact
# http://stackoverflow.com/questions/431628/how-to-combine-2-or-more-querysets-in-a-django-view
        entry_list = Entry.objects.filter(Q(title__icontains=query)|Q(
                                    body_html__icontains=query)).distinct()
        work_list = FlatPage.objects.filter(Q(title__icontains=query)|Q(
                                    content__icontains=query)).distinct()
        result_list = sorted(
            chain(entry_list, work_list),
            key=lambda instance: instance)
            # key=lambda instance: instance.pub_date)
        
    return render_to_response('hth/search.html',
        {'query': query, 
         'results': result_list,
         'user': user
         # http://stackoverflow.com/a/5478944/412329
        }, context_instance=RequestContext(request)) 


# =Static Generation of files on server ===================================

# https://github.com/hypertexthero/django-staticgenerator/
# from blog.models import Post
from django.dispatch import dispatcher
from django.db.models import signals
from staticgenerator import quick_delete
# from django.contrib.comments.models import Comment, FreeComment

def delete(sender, instance):
    quick_delete(instance, '/')

dispatcher.connect(delete, sender=Entry, signal=signals.post_save)
dispatcher.connect(delete, sender=FlatPage, signal=signals.post_save)

def delete_index(sender, instance):
    quick_delete(instance, '/')

signals.post_delete.connect(delete_index, sender=Entry)
signals.post_delete.connect(delete_index, sender=FlatPage)
signals.post_save.connect(publish_entry, sender=Entry)
signals.post_save.connect(publish_flatpage, sender=FlatPage)


# def publish_comment(sender, instance):
#     quick_delete(instance.get_content_object())

# signals.post_save.connect(publish_comment, sender=Comment)
# signals.post_save.connect(publish_comment, sender=FreeComment)