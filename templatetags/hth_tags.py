import datetime
import os
import random

# import Image, ImageOps

from django import template
from django.template import Library, Node
from hth.models import Entry

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
                            is_active=1, kind="A", pub_date__lte=datetime.datetime.now()).order_by('-pub_date', 'title')[:7]
        return {'latest_entries': latest_entries}

@register.inclusion_tag("hth/latest_linked_list_entries.html", name="latest_linked_list_entries")
def LatestLinkedListEntries():
        latest_linked_list_entries = Entry.objects.published().filter(
                            is_active=1, kind="L").order_by('-pub_date', 'title')[:15]
        return {'latest_linked_list_entries': latest_linked_list_entries}


def last_word_in_url(request):
    last_word  = request.path.split('/')[-1:]
    return { 'last_word': last_word }

# Template tags in flatpages.
# http://stackoverflow.com/a/3067759/412329 http://stackoverflow.com/questions/1278042/in-django-is-there-an-easy-way-to-render-a-text-field-as-a-template-in-a-templ/1278507#1278507
@register.tag(name="evaluate")
def do_evaluate(parser, token):
    """
    tag usage {% evaluate object.textfield %}
    """
    try:
        tag_name, variable = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires a single argument" % token.contents.split()[0]
    return EvaluateNode(variable)

class EvaluateNode(template.Node):
    def __init__(self, variable):
        self.variable = template.Variable(variable)

    def render(self, context):
        try:
            content = self.variable.resolve(context)
            t = template.Template(content)
            return t.render(context)
        except template.VariableDoesNotExist, template.TemplateSyntaxError:
            return 'Error rendering', self.variable
