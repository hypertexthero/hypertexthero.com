from django import template
from django.template import Library, Node
from hth.models import Entry

import os
import random

register = template.Library()

# http://stackoverflow.com/a/12992277/412329
@register.filter(name="month_number_to_name")
def MonthNumberToName(value):
    """returns the month name for the given number - 1 indexed"""
    month_name = ["", "January", "February", "March", "April", "May", "June", "July",
               "August", "September", "October", "November", "December"
              ]
    return month_name[int(value)]

# http://stackoverflow.com/a/3540315/412329
# (Waterman's "Reservoir Algorithm") from Knuth's 
# "The Art of Computer Programming" is good (simplified version):
DIRECTORYNAME = os.path.dirname(__file__)

@register.simple_tag(name="kind_words")
def RandomLine(afile):
    # =todo: put kindwords.txt in templates folder?
    afile = open(os.path.join(DIRECTORYNAME, afile))
    line = next(afile)
    for num, aline in enumerate(afile):
      if random.randrange(num + 2): continue
      line = aline
    return line

# Also works but the above is shorter. Need to test which performs best.
# ==
# @register.simple_tag(name="kind_words")
# def randomLine(file_object):
#     file_object = open(os.path.join(DIRECTORYNAME, 'kindwords.txt'))
#     "Retrieve a random line from a file, reading through the file once"
#     lineNum = 0
#     selected_line = ''
# 
#     while 1:
#         aLine = file_object.readline(  )
#         if not aLine: break
#         lineNum = lineNum + 1
#         # How likely is it that this is the last line of the file?
#         if random.uniform(0,lineNum)<1:
#                               selected_line = aLine
#     file_object.close(  )
#     return selected_line

# http://mechanicalgirl.com/post/custom-template-tags-in-django/

@register.inclusion_tag("hth/latest_entries.html", name="latest_entries")
def LatestEntries():
        latest_entries = Entry.objects.filter(
                            is_active=1).order_by('-pub_date', 'title')[:11]
        return {'latest_entries': latest_entries}