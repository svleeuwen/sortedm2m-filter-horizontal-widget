=========================================
django-sortedm2m-filter-horizontal-widget
=========================================

``sortedm2m-filter-horizontal-widget`` is an admin widget for Gregor Mülleggers excellent django-sortedm2m_ library.

.. _django-sortedm2m: http://github.com/gregmuellegger/django-sortedm2m

This allows for a familiar filter horizontal widget.

Installation
============

``pip install django-sortedm2m-filter-horizontal-widget``

Usage
=====

Add ``sortedm2m-filter-horizontal-widget`` to your ``INSTALLED_APPS``. (needed for static files)

In your ``ModelAdmin`` add the following function to override the default widget. ::

    def formfield_for_manytomany(self, db_field, request=None, **kwargs):
        if db_field.name == 'sortedm2m_field_name':
            kwargs['widget'] = SortedFilteredSelectMultiple()

Todo
====

* Automatically assign widget if field is specified in ModelAdmin's ``filter_horizontal``.
* Add tests
