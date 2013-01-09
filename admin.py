from __future__ import absolute_import

from django.contrib import admin

from .models import Entry

class EntryAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'kind', 'url', 'pub_date', 'is_active', 'is_published')
    list_filter = ('is_active',)
    exclude = ('body_html',)
    prepopulated_fields = {"slug": ("title",)}

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
