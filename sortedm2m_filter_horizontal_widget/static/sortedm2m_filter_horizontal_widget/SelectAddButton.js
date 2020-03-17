$(function(){
    $(".related-widget-wrapper").each(function(idx) {  // each = For if use m2m more than one.
        let chk_script_cnt = $(this).find("script").length;
        if (chk_script_cnt === 2) {  // forms.py > class SortedFilteredSelectMultiple -> def render-> output
            let $addBtn = $(this).find("a.related-widget-wrapper-link.add-related");
            $addBtn.addClass("sortedm2m_filter_horizontal_widget_add_button");
        }
    });
});