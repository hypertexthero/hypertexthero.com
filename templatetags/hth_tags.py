from django import template
from django.template import Library, Node
from hth.models import Entry

import os
import random

register = template.Library()

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