import functools
from django.views.generic import date_based
from django.core.urlresolvers import reverse

from .models import Entry

# def prepare_arguments(view):
#     @functools.wraps(view)
#     def wrapped(request, *args, **kwargs):
#         kwargs['allow_future'] = request.user.is_staff
#         kwargs['queryset'] = Entry.objects.all() if request.user.is_staff else Entry.objects.published()
#         kwargs['date_field'] = 'pub_date'
#         return view(request, *args, **kwargs)
#     return wrapped

# @prepare_arguments
# def linked_archive_day(request, *args, **kwargs):
#     return date_based.archive_day(request, *args, **kwargs)
# 
# @prepare_arguments
# def linked_archive_month(request, *args, **kwargs):
#     return date_based.archive_month(request, *args, **kwargs)

# @prepare_arguments
# def logbook(request, *args, **kwargs):
#     return date_based.archive_index(request, *args, **kwargs)

# # generic archive_index view to display notes ordered by date and not display ones saved with a future date - https://docs.djangoproject.com/en/dev/ref/generic-views/#django-views-generic-date-based-archive-index
# def notes_list(request): 
#     """Show all notes"""
# 
#     return archive_index(request, 
#         queryset=Note.objects.all().order_by('-created', 'title'), # https://docs.djangoproject.com/en/dev/ref/models/querysets/#django.db.models.query.QuerySet.order_by
#         date_field='created', # don't forget to set {{ note.created|date:"d F Y" }} in notes/list.html
#         template_name='notes/list.html',
#         # template_object_name='note',
#         allow_future = False # this is the default, but am keeping it here to remember that it can be set to true for other use cases, such as calendar of upcoming events
#     )
# 
def logbook(request): 
    """Logbook homepage"""
    return date_based.archive_index(request,
        queryset=Entry.objects.filter(is_active=True).order_by('-pub_date', 'title'), # https://docs.djangoproject.com/en/dev/ref/models/querysets/#django.db.models.query.QuerySet.order_by
        num_latest=20, # https://docs.djangoproject.com/en/1.2/ref/generic-views/#date-based-generic-views
        date_field='pub_date', # don't forget to set {{ note.created|date:"d F Y" }} in notes/list.html
        template_name='hth/logbook.html',
        # template_object_name='note',
        allow_future = False # this is the default, but am keeping it here to remember that it can be set to true for other use cases, such as calendar of upcoming events
        )

def linked(request): 
    """Linked list (kind == Link)"""
    return date_based.archive_index(request,
        queryset=Entry.objects.filter(is_active=True, kind='L').order_by('-pub_date', 'title'), # https://docs.djangoproject.com/en/dev/ref/models/querysets/#django.db.models.query.QuerySet.order_by
        num_latest=30, # https://docs.djangoproject.com/en/1.2/ref/generic-views/#date-based-generic-views
        date_field='pub_date', # don't forget to set {{ note.created|date:"d F Y" }} in notes/list.html
        template_name='hth/linked.html',
        # template_object_name='note',
        allow_future = False # this is the default, but am keeping it here to remember that it can be set to true for other use cases, such as calendar of upcoming events
        )


def logbook_archive(request): 
    """Archive of original entries (kind == Article)"""
    return date_based.archive_index(request,
        queryset=Entry.objects.filter(kind='A').order_by('-pub_date', 'title'), # https://docs.djangoproject.com/en/dev/ref/models/querysets/#django.db.models.query.QuerySet.order_by
        num_latest=9999, # https://docs.djangoproject.com/en/1.2/ref/generic-views/#date-based-generic-views
        date_field='pub_date', # don't forget to set {{ note.created|date:"d F Y" }} in notes/list.html
        template_name='hth/archive.html',
        # template_object_name='note',
        allow_future = False # this is the default, but am keeping it here to remember that it can be set to true for other use cases, such as calendar of upcoming events
        )


# from django.views.generic import MonthArchiveView
# 
# def linked_archive(request): 
#     """Archive of links (kind == Link)"""
# 
#     return MonthArchiveView.as_view(request, 
#         queryset=Entry.objects.filter(kind='L').order_by('-pub_date', 'title'), # https://docs.djangoproject.com/en/dev/ref/models/querysets/#django.db.models.query.QuerySet.order_by
#         num_latest=9999, # https://docs.djangoproject.com/en/1.2/ref/generic-views/#date-based-generic-views
#         date_field='pub_date', # don't forget to set {{ note.created|date:"d F Y" }} in notes/list.html
#         month_format = '%b',
#         template_name='hth/linked_archive.html',
#         # template_object_name='note',
#         allow_future = False # this is the default, but am keeping it here to remember that it can be set to true for other use cases, such as calendar of upcoming events
#         )

# def linked_archive(request):
#    entries = Entry.objects.all()
#    archive = {}
# 
#    date_field = 'pub_date'
# 
#    years = entries.dates(date_field, 'year')[::-1]
#    for date_year in years:
#        months = entries.filter(date__year=date_year.year).dates(date_field, 'month')
#        archive[date_year] = months
# 
#    archive = sorted(archive.items(), reverse=True)
# 
#    return date_based.archive_index(
#         request,
#         date_field=date_field,
#         queryset=entries,
#         extra_context={'archive': archive},
#    )


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