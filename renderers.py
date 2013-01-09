from django_medusa.renderers import StaticSiteRenderer

# class HomeRenderer(StaticSiteRenderer):
#     def get_paths(self):
#         return frozenset([
#             "/",
#             # "work/",
#             # "/logbook/",
#             # "/linked/",
#             # "/about/",
#             # "/contact/",
#             # "/cv/",
#         ])
# 
# renderers = [HomeRenderer, ]



from hth.models import Entry


class EntryRenderer(StaticSiteRenderer):
    def get_paths(self):
        paths = ["/", "/logbook/", ]

        items = Entry.objects.filter(is_active=True).order_by('-pub_date')
        for item in items:
            paths.append(item.get_absolute_url())

        return paths

renderers = [EntryRenderer, ]