from __future__ import absolute_import

from django.contrib import admin

from .models import Entry

def make_published(modeladmin, request, queryset):
    queryset.update(is_active=True)
make_published.short_description = "Make Active"

def make_draft(modeladmin, request, queryset):
    queryset.update(is_active=False)
make_draft.short_description = "Make Draft"

def make_article(modeladmin, request, queryset):
    queryset.update(kind='A')
make_article.short_description = "Change Kind to Article"

def make_link(modeladmin, request, queryset):
    queryset.update(kind='L')
make_link.short_description = "Change Kind to Link"

class EntryAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'kind', 'url', 'pub_date', 'is_active', 'is_published',)
    list_filter = ('is_active', 'pub_date',)
    save_on_top = True
    exclude = ('body_html',)
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ['title','body', 'body_html']
    actions = [make_article, make_link, make_published, make_draft]
    
    # class Media:
    #   js = ("/static/js/jquery-1.7.2.min.js",
    #         # "/static/js/jquery-ui-1.8.20.custom.min.js",
    #         # "/static/js/admin_sorting.js",
    #         )

    def formfield_for_dbfield(self, db_field, **kwargs):
        formfield = super(EntryAdmin, self).formfield_for_dbfield(db_field, **kwargs)
        if db_field.name == 'body':
            formfield.widget.attrs['rows'] = 25
        return formfield

admin.site.register(Entry, EntryAdmin)
