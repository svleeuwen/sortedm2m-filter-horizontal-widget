var OrderedSelectBox = {
    cache: new Object(),
    init: function(id) {
        var box = document.getElementById(id);
        var node;

        OrderedSelectBox.cache[id] = new Array();
        var cache = OrderedSelectBox.cache[id];
        for (var i = 0; (node = box.options[i]); i++) {
            OrderedSelectBox.add_to_cache(id, node);
        }
    },
    redisplay: function(id) {
        // Repopulate HTML select box from cache
        var box = document.getElementById(id);
        box.options.length = 0; // clear all options
        for (var i = 0, j = OrderedSelectBox.cache[id].length; i < j; i++) {
            var node = OrderedSelectBox.cache[id][i];
            if (node.displayed) {
                box.options[box.options.length] = new Option(node.text, node.value, false, false);
            }
        }
    },
    filter: function(id, text) {
        // Redisplay the HTML select box, displaying only the choices containing ALL
        // the words in text. (It's an AND search.)
        var tokens = text.toLowerCase().split(/\s+/);
        var node, token;
        for (var i = 0; (node = OrderedSelectBox.cache[id][i]); i++) {
            node.displayed = 1;
            for (var j = 0; (token = tokens[j]); j++) {
                if (node.text.toLowerCase().indexOf(token) == -1) {
                    node.displayed = 0;
                }
            }
        }
        OrderedSelectBox.redisplay(id);
    },
    delete_from_cache: function(id, value) {
        var node, delete_index = null;
        for (var i = 0; (node = OrderedSelectBox.cache[id][i]); i++) {
            if (node.value == value) {
                delete_index = i;
                break;
            }
        }
        var j = OrderedSelectBox.cache[id].length - 1;
        for (var i = delete_index; i < j; i++) {
            OrderedSelectBox.cache[id][i] = OrderedSelectBox.cache[id][i+1];
        }
        OrderedSelectBox.cache[id].length--;
    },
    add_to_cache: function(id, option) {

        var order = 0;
        if( option.getAttribute('data-sort-value') ) {
          order = parseInt( option.getAttribute('data-sort-value') );
        }

        OrderedSelectBox.cache[id].push({value: option.value, text: option.text, displayed: 1, order: order });

        // Re-order on sort-order-value (every time)
        OrderedSelectBox.cache[id].sort(function(a, b){
          return a.order - b.order;
        });
    },
    cache_contains: function(id, value) {
        // Check if an item is contained in the cache
        var node;
        for (var i = 0; (node = OrderedSelectBox.cache[id][i]); i++) {
            if (node.value == value) {
                return true;
            }
        }
        return false;
    },
    move: function(from, to) {
        var from_box = document.getElementById(from);
        var to_box = document.getElementById(to);
        var option;

        // Remove sort-order-value before move:
        for (var i = 0; (option = OrderedSelectBox.cache[to][i]); i++) {
          option.order = 0;
        }

        for (var i = 0; (option = from_box.options[i]); i++) {
            if (option.selected && OrderedSelectBox.cache_contains(from, option.value)) {
                OrderedSelectBox.add_to_cache(to, option);
                OrderedSelectBox.delete_from_cache(from, option.value);
            }
        }
        OrderedSelectBox.redisplay(from);
        OrderedSelectBox.redisplay(to);
    },
    move_all: function(from, to) {
        var from_box = document.getElementById(from);
        var to_box = document.getElementById(to);
        var option;

        for (var i = 0; (option = from_box.options[i]); i++) {
            if (OrderedSelectBox.cache_contains(from, option.value)) {
                OrderedSelectBox.add_to_cache(to, option);
                OrderedSelectBox.delete_from_cache(from, option.value);
            }
        }
        OrderedSelectBox.redisplay(from);
        OrderedSelectBox.redisplay(to);
    },
    sort: function(id) {
        OrderedSelectBox.cache[id].sort( function(a, b) {
            a = a.text.toLowerCase();
            b = b.text.toLowerCase();
            try {
                if (a > b) return 1;
                if (a < b) return -1;
            }
            catch (e) {
                // silently fail on IE 'unknown' exception
            }
            return 0;
        } );
    },
    orderUp: function(id) {
      $('#' + id).find('option:selected').each(function(){
          $(this).insertBefore($(this).prev());
      });

    },
    orderDown: function(id) {

      $('#' + id).find('option:selected').each(function(){
       $(this).insertAfter($(this).next());
      });

    },
    select_all: function(id) {
        var box = document.getElementById(id);
        for (var i = 0; i < box.options.length; i++) {
            box.options[i].selected = 'selected';
        }
    }
};

// Overwrite dissmissAddAnotherPopup so the added item gets inserted in our OrderedSelectBox
if (window.showAddAnotherPopup) {
    var django_dismissAddAnotherPopup = window.dismissAddAnotherPopup;
    window.dismissAddAnotherPopup = function (win, newId, newRepr) {
        // newId and newRepr are expected to have previously been escaped by
        // django.utils.html.escape.
        newId = html_unescape(newId);
        newRepr = html_unescape(newRepr);
        var name = windowname_to_id(win.name);
        var elem = document.getElementById(name);
        if (elem) {
            var elemName = elem.nodeName.toUpperCase();
            if (elemName == 'SELECT') {
                var o = new Option(newRepr, newId);
                elem.options[elem.options.length] = o;
                o.selected = true;
            } else if (elemName == 'INPUT') {
                if (elem.className.indexOf('vManyToManyRawIdAdminField') != -1 && elem.value) {
                    elem.value += ',' + newId;
                } else {
                    elem.value = newId;
                }
            }
        } else {
            var toId = name + "_to";
            elem = document.getElementById(toId);
            var o = new Option(newRepr, newId);
            OrderedSelectBox.add_to_cache(toId, o);
            OrderedSelectBox.redisplay(toId);
        }
        win.close();
    };
}
