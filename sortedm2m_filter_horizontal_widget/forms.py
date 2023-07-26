from itertools import chain
from django import forms
from django.conf import settings
from django.db.models.query import QuerySet
from django.utils.encoding import force_str
from django.utils.html import conditional_escape, escape
from django.utils.safestring import mark_safe

from django.forms.utils import flatatt

STATIC_URL = getattr(settings, "STATIC_URL", settings.MEDIA_URL)


class SortedMultipleChoiceField(forms.ModelMultipleChoiceField):
    def __init__(self, *args, **kwargs):
        if not kwargs.get("widget"):
            kwargs["widget"] = SortedFilteredSelectMultiple(
                is_stacked=kwargs.get("is_stacked", False)
            )
        super(SortedMultipleChoiceField, self).__init__(*args, **kwargs)

    def clean(self, value):
        queryset = super(SortedMultipleChoiceField, self).clean(value)
        if value is None or not isinstance(queryset, QuerySet):
            return queryset
        object_list = dict(
            ((str(key), value) for key, value in iter(queryset.in_bulk(value).items()))
        )
        return [object_list[str(pk)] for pk in value]

    def _has_changed(self, initial, data):
        if initial is None:
            initial = []
        if data is None:
            data = []
        if len(initial) != len(data):
            return True
        initial_set = [force_str(value) for value in self.prepare_value(initial)]
        data_set = [force_str(value) for value in data]
        return data_set != initial_set


class SortedFilteredSelectMultiple(forms.SelectMultiple):
    """
    A SortableSelectMultiple with a JavaScript filter interface.

        Requires jQuery to be loaded.

    Note that the resulting JavaScript assumes that the jsi18n
    catalog has been loaded in the page
    """

    def __init__(self, is_stacked=False, attrs=None, choices=()):
        self.is_stacked = is_stacked
        super(SortedFilteredSelectMultiple, self).__init__(attrs, choices)

    class Media:
        css = {
            "screen": (STATIC_URL + "sortedm2m_filter_horizontal_widget/widget.css",)
        }

        js = (
            STATIC_URL + "sortedm2m_filter_horizontal_widget/OrderedSelectBox.js",
            STATIC_URL + "sortedm2m_filter_horizontal_widget/OrderedSelectFilter.js",
            STATIC_URL + "sortedm2m_filter_horizontal_widget/jquery.min.js",
        )

    def build_attrs(self, attrs=None, extra_attrs=None, **kwargs):
        attrs = dict(attrs, **kwargs)
        if extra_attrs:
            attrs.update(extra_attrs)
        classes = attrs.setdefault("class", "").split()
        classes.append("sortedm2m")
        if self.is_stacked:
            classes.append("stacked")
        attrs["class"] = " ".join(classes)
        return attrs

    def render(self, name, value, attrs=None, choices=(), renderer=None):
        if attrs is None:
            attrs = {}
        if value is None:
            value = []
        admin_media_prefix = getattr(
            settings, "ADMIN_MEDIA_PREFIX", STATIC_URL + "admin/"
        )
        final_attrs = self.build_attrs(self.attrs, attrs, name=name)
        output = [f'<select multiple="multiple"{flatatt(final_attrs)}>']
        options = self.render_options(choices, value)
        if options:
            output.append(options)
        if "verbose_name" in final_attrs.keys():
            verbose_name = final_attrs["verbose_name"]
        else:
            verbose_name = name.split("-")[-1]
        output.append("</select>")
        output.append('<script>window.addEventListener("load", function(e) {')
        output.append(
            f"OrderedSelectFilter.init('id_{name}', '{verbose_name}', {int(self.is_stacked)}, '{admin_media_prefix}')"
        )
        output.append("});</script>\n")
        output.append(
            """
        <script>
        (function($) {
            $(document).ready(function() {
                var updateOrderedSelectFilter = function() {
                    // If any SelectFilter widgets are a part of the new form,
                    // instantiate a new SelectFilter instance for it.
                    if (typeof OrderedSelectFilter != "undefined"){
                        $(".sortedm2m").each(function(index, value){
                            var namearr = value.name.split('-');
                            OrderedSelectFilter.init(value.id, namearr[namearr.length-1], false, "%s");
                        });
                        $(".sortedm2mstacked").each(function(index, value){
                            var namearr = value.name.split('-');
                            OrderedSelectFilter.init(value.id, namearr[namearr.length-1], true, "%s");
                        });
                    }
                }
                $(document).on('formset:added', function(row, prefix) {
                    updateOrderedSelectFilter();
                });
            });
        })(django.jQuery)
        </script>"""
            % (admin_media_prefix, admin_media_prefix)
        )

        return mark_safe("\n".join(output))

    def render_option(self, selected_choices, option_value, option_label):
        option_value = force_str(option_value)
        selected_html = (
            (option_value in selected_choices) and ' selected="selected"' or ""
        )
        try:
            index = list(selected_choices).index(escape(option_value))
            selected_html = f' data-sort-value="{index}" {selected_html}'
        except ValueError:
            pass

        return f'<option value="{escape(option_value)}"{selected_html}>{conditional_escape(force_str(option_label))}</option>'

    def render_options(self, choices, selected_choices):
        # Normalize to strings.
        selected_choices = list(force_str(v) for v in selected_choices)
        output = []
        for option_value, option_label in chain(self.choices, choices):
            if isinstance(option_label, (list, tuple)):
                output.append(f'<optgroup label="{escape(force_str(option_value))}">')
                for option in option_label:
                    output.append(self.render_option(selected_choices, *option))
                output.append("</optgroup>")
            else:
                output.append(
                    self.render_option(selected_choices, option_value, option_label)
                )
        return "\n".join(output)

    def _has_changed(self, initial, data):
        if initial is None:
            initial = []
        if data is None:
            data = []
        if len(initial) != len(data):
            return True
        initial_set = [force_str(value) for value in initial]
        data_set = [force_str(value) for value in data]
        return data_set != initial_set
