=========================================
django-sortedm2m-filter-horizontal-widget
=========================================

``sortedm2m-filter-horizontal-widget`` is an admin widget for Gregor Mülleggers excellent django-sortedm2m_ library.

.. _django-sortedm2m: http://github.com/gregmuellegger/django-sortedm2m

This allows for a familiar filter horizontal widget.

Installation
============

``pip install django-sortedm2m-filter-horizontal-widget``

What version do I need?
=======================

+------------+------------+
| Django     | Install    |
+============+============+
| < 1.8      | 0.2        |
+------------+------------+
| 1.8        | 1.1        |
+------------+------------+
| >= 1.9     | latest     |
+------------+------------+

Usage
=====

Add ``sortedm2m_filter_horizontal_widget`` to your ``INSTALLED_APPS``. (needed for static files)

In your ``ModelAdmin`` add the following function to override the default widget. ::

    from sortedm2m_filter_horizontal_widget.forms import SortedFilteredSelectMultiple

    class MyModelAdmin(admin.ModelAdmin):
        # ...

        def formfield_for_manytomany(self, db_field, request=None, **kwargs):
            if db_field.name == 'your_sortedm2m_field_name':
                kwargs['widget'] = SortedFilteredSelectMultiple()
            return super(MyModelAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)

Todo
====

* Automatically assign widget if field is specified in ModelAdmin's ``filter_horizontal``.
* Add tests
