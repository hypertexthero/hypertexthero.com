# from django_medusa.renderers import StaticSiteRenderer
#
# class HomeRenderer(StaticSiteRenderer):
#     def get_paths(self):
#         return frozenset([
#             "/",
#             "work/",
#             "/logbook/",
#             "/linked/",
#             "/archive/",
#             "/contact/",
#             # "/cv/",
#         ])
#
# renderers = [HomeRenderer, ]
#
#
# # =todo
# from hth.models import Entry
# from django.contrib.flatpages.models import FlatPage
#
# class EntryRenderer(StaticSiteRenderer):
#     def get_paths(self):
#         paths = ["/logbook/",]
#
#         items = Entry.objects.filter(is_active=True, kind="A").order_by('-pub_date')
#         for item in items:
#             paths.append(item.get_absolute_url())
#
#         return paths
#
# class WorkRenderer(StaticSiteRenderer):
#     def get_paths(self):
#         paths = ["/work/", ]
#
#         items = FlatPage.objects.all()
#         for item in items:
#             paths.append(item.get_absolute_url())
#
#         return paths
#
# class LinkRenderer(StaticSiteRenderer):
#     def get_paths(self):
#         paths = ["/linked/", ]
#
#         items = Entry.objects.filter(is_active=True, kind="L").order_by('-pub_date')
#         for item in items:
#             paths.append(item.get_absolute_url())
#
#         return paths
#
# renderers = [EntryRenderer, WorkRenderer, LinkRenderer,]

# =todo
# from hth.models import Entry
# from django.contrib.flatpages.models import FlatPage
#
# from itertools import chain
#
# class EntryRenderer(StaticSiteRenderer):
#     def get_paths(self):
#         paths = ["/", "/logbook/", "/work/", ]
#         entry_list = []
#         work_list = []
#         result_list = list(chain(entry_list, work_list))
#
#         entry_list = Entry.objects.filter(is_active=True).order_by('-pub_date')
#         for entry in entry_list:
#             paths.append(entry.get_absolute_url())
#
#         work_list = FlatPage.objects.all()
#         for work in work_list:
#             paths.append(work.get_absolute_url())
#
#         result_list = sorted(
#             chain(entry_list, work_list),
#             key=lambda instance: instance)
#
#         return paths
#
# renderers = [EntryRenderer, ]
#
#
