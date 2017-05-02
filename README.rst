=========================================
django-sortedm2m-filter-horizontal-widget
=========================================

``sortedm2m-filter-horizontal-widget`` is an admin widget for Gregor Mülleggers excellent django-sortedm2m_ library.

.. _django-sortedm2m: http://github.com/gregmuellegger/django-sortedm2m

This allows for a familiar filter horizontal widget.

.. figure:: https://d1ro8r1rbfn3jf.cloudfront.net/ms_144103/11clLqJhyNUbvQj29D1oJ5gnhbqmct/screencast%2B2017-05-02%2B10-11-01.gif?Expires=1493799115&Signature=P00zKop9k0s7sljA1NH8ckcbM62wXJyWLm8~nsN3GL92N6yXBkaW7AtyPeMgOH~8uDrTjzNOn-xP99REq1C2FWiFHXg-PC91U9hPw1LsIFEREqelyWuqBw4uCa2ACRgdFpeWi8XoRYRvOgEG98grwecQlxS4spX-KjNi7myeL95RxchdSvvV02~dd6pIQdPC0IqJNpECLK1o3e5XNfpMP71uCOQQn7KYIg0OM4bTHwDyQVE9-7HW6jvQJJ5NXrJXrJIrtyNOO5CV~UhgFEyyNn8-2vFNB5Q-IUkU9EstpgUpNehuJS0ygaDLFXE9zjQOCLiJb~gecASIboe5YZ0etQ__&Key-Pair-Id=APKAJHEJJBIZWFB73RSA

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
