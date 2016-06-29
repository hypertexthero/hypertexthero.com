# _*_ coding:utf-8 _*_
# https://github.com/sjkingo/mezzanine2jekyll
from django.core.management.base import BaseCommand

# http://stackoverflow.com/a/15364584/412329
from django.utils.encoding import smart_str, smart_unicode

from hth.models import Entry
import os
import re

class Command(BaseCommand):
    """ 
    Usage: $ python ../manage.py django2hugo /chosen/output/directory/

    """
    help = 'Export hth logbook entries as Hugo markdown files'

    def add_arguments(self, parser):
        parser.add_argument('output_dir', help='Where to put the outputted Hugo files')

    def handle(self, *args, **options):
        for post in Entry.objects.all():
            header = {
                # 'layout': 'notebook',
                'title': post.title.replace(':', ''),
                # =todo: make date format to 2005-03-22T00:00:00Z - http://stackoverflow.com/a/25120668/412329
                'date': post.pub_date,
                'what': '\n - ' + '\n - '.join([str(kw) for kw in post.tags.all()]),
                'kind': post.kind,
                'linkedurl': post.url
            }

            # output_dir = '/Users/simon/Desktop/django2hugo_output'
            output_dir = args[0]
            filename = '{d.year:02}-{d.month:02}-{d.day:02}-{slug}.markdown'.format(
                    d=post.pub_date, slug=post.slug)

            # content = post.body.decode('latin-1').decode('utf-8')
            content = post.body.encode('utf-8').replace('\r', '')
            
            # Write out the file
            with open(os.path.join(output_dir, filename), 'w') as fp:
                fp.write('---' + os.linesep)
                for k, v in header.items():
                    fp.write(smart_str('%s: %s%s' % (k, v, os.linesep)))
                fp.write('---' + os.linesep)
                fp.write(smart_str(content))
