from django.contrib import admin

from sortedm2m_filter_horizontal_widget.forms import SortedFilteredSelectMultiple
from .models import Book, Author


class BookAdmin(admin.ModelAdmin):

    def formfield_for_manytomany(self, db_field, request=None, **kwargs):
        if db_field.name == 'authors':
            kwargs['widget'] = SortedFilteredSelectMultiple()
        return super(BookAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)


admin.site.register(Book, BookAdmin)
admin.site.register(Author)