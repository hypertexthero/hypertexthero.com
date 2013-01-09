# import akismet
import datetime
# from docutils.core import publish_parts

from django.conf import settings
from django.db import models
from django.contrib.sites.models import Site
# from django.contrib.comments.signals import comment_was_posted
from django.utils.encoding import smart_str
from django.utils.translation import ugettext_lazy as _

from markdown import markdown
from typogrify.templatetags.typogrify_tags import typogrify
from django.template.defaultfilters import slugify


# BLOG_DOCUTILS_SETTINGS = getattr(settings, 'BLOG_DOCUTILS_SETTINGS',
#      {  'doctitle_xform': False,
#         'initial_header_level': 4,
#         'id_prefix': 's-',
#      }
# )


class EntryManager(models.Manager):
    
    def published(self):
        return self.active().filter(pub_date__lte=datetime.datetime.now())
    
    def active(self):
        return super(EntryManager, self).get_query_set().filter(is_active=True)

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
    kind = models.CharField(max_length=1, choices=KIND, default=1, help_text="Is this a link to other content or an original article?")
    # TODO: linkurl field and link/article slug
    url = models.URLField(blank=True, help_text="The link URL")
    body = models.TextField()
    body_html = models.TextField()
    content_format = models.CharField(choices=CONTENT_FORMAT_CHOICES, max_length=50, default=1)
    is_active = models.BooleanField(help_text=_("Tick to make this entry live (see also the publication date). Note that administrators (like yourself) are allowed to preview inactive entries whereas the general public aren't."), default=True)
    pub_date = models.DateTimeField(verbose_name=_("Publication date"), help_text=_("For an entry to be published, it must be active and its publication date must be in the past."))
    mod_date = models.DateTimeField(auto_now_add=True, editable=False)
    # author = models.CharField(max_length=100)

    objects = EntryManager()
    
    class Meta:
        db_table = 'blog_entries'
        verbose_name_plural = 'entries'
        ordering = ('-mod_date',)
        get_latest_by = 'pub_date'

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return "/logbook/%s/%s/" % (self.pub_date.strftime("%Y/%B").lower(), self.slug)
    
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
                # typogrify - http://code.google.com/p/typogrify/ and http://djangosnippets.org/snippets/381/
            self.body_html = typogrify(markdown(self.body, ['extra', 'codehilite']))
            # self.content_html = markdown(self.content_markdown)
            self.modified = datetime.datetime.now()
        super(Entry, self).save(*args, **kwargs)