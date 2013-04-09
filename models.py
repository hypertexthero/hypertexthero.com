# import akismet
import datetime
# from docutils.core import publish_parts

from django.conf import settings
from django.db import models
from django.contrib.sites.models import Site
# from django.contrib.comments.signals import comment_was_posted
from django.utils.encoding import smart_str
from django.utils.translation import ugettext_lazy as _

import markdown
from typogrify.templatetags.typogrify_tags import typogrify
from django.template.defaultfilters import slugify

from django.core.urlresolvers import reverse
# from django.views.generic import DetailView

from taggit.managers import TaggableManager

class EntryManager(models.Manager):
    
    def published(self):
        return self.active().filter(pub_date__lte=datetime.datetime.now())
    
    def active(self):
        return super(EntryManager, 
                        self).get_query_set().filter(is_active=True)

CONTENT_FORMAT_CHOICES = (
    (u'markdown', u'Markdown'),
    (u'html', u'Raw HTML'),
)
    
class Entry(models.Model):
    
    KIND = (
        ('L', 'Link'),
        ('A', 'Article'),
    )
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique_for_date='pub_date')
    kind = models.CharField(max_length=1, choices=KIND, default=1,
     help_text="Is this a link to other content or an original article?")
    url = models.URLField(blank=True, help_text="The link URL")
    body = models.TextField(blank=True)
    body_html = models.TextField()
    content_format = models.CharField(choices=CONTENT_FORMAT_CHOICES, 
                                            max_length=50, default=1)
    is_active = models.BooleanField(help_text=_("Tick to make this entry\
        live (see also the publication date). Note that administrators\
        (like yourself) are allowed to preview inactive entries whereas\
        the general public aren't."), default=True)
    pub_date = models.DateTimeField(verbose_name=_("Publication date"),
     help_text=_("For an entry to be published, it must be active and its\
      publication date must be in the past."))
    mod_date = models.DateTimeField(auto_now_add=True, editable=False)

    tags = TaggableManager()

    objects = EntryManager()
    
    class Meta:
        db_table = 'blog_entries'
        verbose_name_plural = 'entries'
        ordering = ('-mod_date',)
        get_latest_by = 'pub_date'

    def __unicode__(self):
        return self.title
    
# =todo: http://devwiki.beloblotskiy.com/index.php5/Django:_Decoupling_the_URLs
# http://www.achanceofbrainshowers.com/blog/tech/2010/11/29/djangos_permalink_decorator/
# http://stackoverflow.com/questions/712878/how-to-get-a-reverse-url-for-a-generic-view
    def get_absolute_url(self): # "view on site" link will be visible in admin interface
        """Construct the absolute URL for an Entry."""
        # old (hard-coded url):
        return "/logbook/%s/%s/" % (self.pub_date.strftime(
                                                "%Y/%m").lower(), self.slug)
        # return reverse('logbook-entry-detail', (), {
        #                     'year': self.pub_date.strftime("%Y"),
        #                     'month': self.pub_date.strftime("%d").lower(),
        #                             # 'day': self.pub_date.strftime("%d"),
        #                     'slug': self.slug})
    
    # =todo: remove hardcoded /linked/ link (see =todo above)
    def get_linked_list_url(self): # "view on site" link will be visible in admin interface
        """Construct the absolute URL for an Entry whose kind == L."""
        return "/linked/%s/%s/" % (self.pub_date.strftime(
                                                "%Y/%m/%d").lower(), self.slug)
        # return reverse('project.app.views.view_name', None, [str(self.id)])

# http://stackoverflow.com/questions/2214852/next-previous-links-from-a-query-set-generic-views
    def get_next_article(self):
      next = Entry.objects.filter(id__gt=self.id, kind='A')
      if next:
        return next[0]
      return False
    
    def get_prev_article(self):
      prev = Entry.objects.filter(id__lt=self.id, kind='A')
      if prev:
        return prev[0]
      return False
      
    def is_published(self):
        """
        Return True if the entry is publicly accessible.
        """
        return self.is_active and self.pub_date <= datetime.datetime.now()
    is_published.boolean = True
    

    def save(self, *args, **kwargs):
        if self.content_format == u'html':
            self.body_html = self.body
        elif self.content_format == u'markdown':
            # Also applying codehilite and footnotes markdown extensions: 
                # http://fi.am/entry/code-highlighting-in-django/
                # http://freewisdom.org/projects/python-markdown/CodeHilite
                # http://freewisdom.org/projects/python-markdown/Footnotes
                # typogrify - http://code.google.com/p/typogrify/ 
                    # and http://djangosnippets.org/snippets/381/
            self.body_html = typogrify(markdown.markdown(
                                    self.body, ["extra", "codehilite"]))
            # self.content_html = markdown(self.content_markdown)
            self.modified = datetime.datetime.now()
        super(Entry, self).save(*args, **kwargs)