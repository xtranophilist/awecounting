function init_select2(element, callback) {
    if ($(element).data('add-url')) {
        var drop_class = '.drop-' + $(element).data('field').toLowerCase().replace(/ /g, '-');
        $(drop_class).find('.appended-link').remove();
        jQuery('<a/>', {
            class: 'appended-link',
            href: $(element).data('add-url'),
            title: 'Add New ' + $(element).data('field'),
            text: 'Add New ' + $(element).data('field'),
            'data-toggle': 'modal'
        }).appendTo(drop_class).on('click', [element], appended_link_clicked);
    }
}

appended_link_clicked = function (e) {
    get_target(e).parent().toggle();
    window.last_active_select = e.data[0];
    e.preventDefault();
    var url = $(this).attr('href');
    if (url.indexOf('#') == 0) {
        $(url).modal('open');
    } else {
        var old_forms = $('form');
        $.get(url,function (data) {
            $('#modal').html(data).modal();
        }).success(function () {
                var new_forms = $('form').not(old_forms).get();
                $(new_forms).submit({url: url}, override_form);
                $('#modal').on('shown', function () {
                    $('input:text:visible:first', this).focus();
                });
            });
    }
    return false;
}

function return_name(obj) {
    return obj.name;
}

//Triggers on document-ready
$(document).ready(function () {
    $('.change-on-ready').trigger('change');

    $('.select2').each(function () {
        var element = this;
        var drop_class = 'drop-' + $(element).attr('name')
        var options_dict = {'dropdownCssClass': drop_class, 'dropdownAutoWidth': true, 'width': 'resolve'}
        if ($(element).hasClass('placehold'))
            options_dict['placeholderOption'] = 'first';
        $(element).select2(options_dict);
        if ($(element).data('add-url')) {
            if ($(element).data('field'))
                var field_name = $(element).data('field');
            else
                var field_name = $(element).attr('name').replace(/_/g, ' ').toTitleCase();
            jQuery('<a/>', {
                class: 'appended-link',
                href: $(element).data('add-url'),
                title: 'Add New ' + field_name,
                text: 'Add New ' + field_name,
                'data-toggle': 'modal'
            }).appendTo('.' + drop_class).on('click', [element], appended_link_clicked);
        }


    });

    $('.btn-danger').click(function (e) {
        if (confirm('Are you sure you want to delete?')) {
            return true;
        } else return false;
    });


//    $('#modal').on('shown',function () {
//        $('#modal').off('wheel.modal mousewheel.modal');
//        $('body').on('wheel.modal mousewheel.modal', function () {
//            return false;
//        });
//    }).on('hidden', function () {
//            $('body').off('wheel.modal mousewheel.modal');
//        });
    $('.col-box a').click(function (e) {
        e.preventDefault();
        $(this).parent('.col-box-header').siblings('.col-box-body').slideToggle();
        $(this).find('.status-handle').toggleClass('icon-chevron-down');
    });
});

override_form = function (event) {
    var $form = $(this);
    var $target = $('#modal');
    var action = $form.attr('action');
    if (typeof action == 'undefined') {
        action = event.data.url;
    }

    $.ajax({
        type: $form.attr('method'),
        url: action,
        data: $form.serialize(),

        success: function (data, status) {
            //write the reply
            $target.html(data);
            //form sent by callback is also overwritten to submit via ajax
            $target.find('form').submit({url: action}, override_form);
        }
    });

    event.preventDefault();
}

on_form_submit = function (event) {
    var $form = $(this);
    var $target = $($form.attr('data-target'));

    $.ajax({
        type: $form.attr('method'),
        url: $form.attr('action'),
        data: $form.serialize(),

        success: function (data, status) {
            $target.html(data);
        }
    });

    event.preventDefault();
}

//Useful Functions

function compare_arrays(arr1, arr2) {
    return $(arr1).not(arr2).length == 0 && $(arr2).not(arr1).length == 0;
}

function intersect_safe(a, b) {
    var ai = 0, bi = 0;
    var result = new Array();

    while (ai < a.length && bi < b.length) {
        if (a[ai] < b[bi]) {
            ai++;
        }
        else if (a[ai] > b[bi]) {
            bi++;
        }
        else /* they're equal */
        {
            result.push(a[ai]);
            ai++;
            bi++;
        }
    }

    return result;
}

function intersection(arr1, arr2) {
    var temp = [];

    for (var i in arr1) {
        var element = arr1[i];

        if (arr2.indexOf(element) > -1) {
            temp.push(element);
        }
    }

    return temp;
}

function rnum(o) {
    return isNaN(o) ? '' : o;
}

function isAN(n) {
    if (n == '')
        return false;
    if (n == null)
        return false;
    return !isNaN(n);
}

function empty_or_undefined(o) {
    if (o == '' || typeof o == 'undefined')
        return true;
    return false;
}

function empty_to_zero(o) {
    if (o == '' || typeof o == 'undefined')
        return 0;
    return o;
}

function round2(n) {
    return isAN(n) ? Math.round(n * 100) / 100 : '';
}

function round2z(n) {
    return isAN(n) ? Math.round(parseFloat(n) * 100) / 100 : 0;
}

function get_target(e) {
    return $((e.currentTarget) ? e.currentTarget : e.srcElement); //for IE <9 compatibility
}

function get_form(e) {
    return $(get_target(e)).closest('form')[0];
}

Object.size = function (obj) {
    var size = 0, key;
    for (key in obj) {
        if (obj.hasOwnProperty(key)) size++;
    }
    return size;
};

//String

//Converts underscored or dashed string to camelCase
String.prototype.toCamelCase = function () {
    return this.replace(/[-_\s]+(.)?/g, function (match, c) {
        return c ? c.toUpperCase() : "";
    });
}

//Converts camelCased or dashed string into an underscored_one
String.prototype.toUnderscore = function () {
    return this.replace(/([a-z\d])([A-Z]+)/g, '$1_$2').replace(/[-\s]+/g, '_').toLowerCase();
}

//Converts underscored or camelCased string into an dashed-one
String.prototype.toDash = function () {
    return this.replace(/([A-Z])/g, '-$1').replace(/[-_\s]+/g, '-').toLowerCase();
}

String.prototype.toTitleCase = function () {
    var smallWords = /^(a|an|and|as|at|but|by|en|for|if|in|of|on|or|the|to|vs?\.?|via)$/i;

    return this.replace(/([^\W_]+[^\s-]*) */g, function (match, p1, index, title) {
        if (index > 0 && index + p1.length !== title.length &&
            p1.search(smallWords) > -1 && title.charAt(index - 2) !== ":" &&
            title.charAt(index - 1).search(/[^\s-]/) < 0) {
            return match.toLowerCase();
        }

        if (p1.substr(1).search(/[A-Z]|\../) > -1) {
            return match;
        }

        return match.charAt(0).toUpperCase() + match.substr(1);
    });
};

//Fixes

$(document).on('mouseup mousedown', '[contenteditable]', function () {
    this.focus();
});

//setup ajax requests to include csrf token
$.ajaxSetup({
    beforeSend: function (xhr, settings) {
        function getCookie(name) {
            var cookieValue = null;
            if (document.cookie && document.cookie != '') {
                var cookies = document.cookie.split(';');
                for (var i = 0; i < cookies.length; i++) {
                    var cookie = jQuery.trim(cookies[i]);
                    // Does this cookie string begin with the name we want?
                    if (cookie.substring(0, name.length + 1) == (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }

        if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
            // Only send the token to relative URLs i.e. locally.
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        }
    }
});

//Reusable KO Models

function TableViewModel(options, row_model) {

    var self = this;

    if (typeof(options.properties) != 'undefined') {
        /** @namespace options.properties */
        for (var k in options.properties)
            self[k] = options.properties[k];
    }

    self.message = ko.observable();
    self.state = ko.observable('standby');

    if (typeof row_model != 'undefined') {
        self.rows = ko.observableArray(ko.utils.arrayMap(options.rows, function (item) {
            return new row_model(item);
        }));

        //if there are any rows
        if (self.rows().length) {
            //if row has a sn() field, sort it
            if (typeof self.rows()[0].sn != 'undefined') {
                self.rows().sort(function (l, r) {
                    return l.sn() > r.sn() ? 1 : -1
                });
            }
        }

        self.deleted_rows = ko.observableArray();

        self.hasNoRows = ko.computed(function () {
            return self.rows().length === 0;
        });

        self.addRow = function () {
            var new_item_index = self.rows().length + 1;
            self.rows.push(new row_model());
        };

        self.removeRow = function (row) {
            self.rows.remove(row);
            self.deleted_rows.push(row);
        };

        if (self.hasNoRows()) {
            self.addRow();
        }

        self._initial_rows = self.rows().slice(0);

        self.reset = function () {
            self.rows(self._initial_rows);
        }

        self.get_total = function (field) {
            var total = 0;
            self.rows().forEach(function (i) {
                var f = i[field];
                if (typeof f != 'function')
                    throw new Error(field + ' isn\'t a property of row model ' + row_model.name + '!')
                if (isAN(parseFloat(f())))
                    total += parseFloat(f());
            });
            return total;
        }
    }

    if (typeof(options.save_to_url) != 'undefined') {
        self.save = function (model, e) {
            self.state('waiting');
            var el = get_target(e);
            $.ajax({
                type: "POST",
                url: options.save_to_url,
                data: ko.toJSON(self),
                success: function (msg) {
                    self.message('Saved!');
                    if (typeof(options.onSaveSuccess) != 'undefined') {
                        options.onSaveSuccess(msg, self.rows());
                    }
                    self.state('success');
                    self.deleted_rows = [];
                },
                error: function (XMLHttpRequest, textStatus, errorThrown) {
                    self.message('Saving Failed!');
                    self.state('error');
                }
            });
        }
    }
    else {
        self.save = function () {
            throw new Error("'save_to_url' option not passed to TableViewModel or save() not implemented!");
        }
    }
}

function days_between(first, second) {

    // Copy date parts of the timestamps, discarding the time parts.
    var one = new Date(first.getFullYear(), first.getMonth(), first.getDate());
    var two = new Date(second.getFullYear(), second.getMonth(), second.getDate());

    // Do the math.
    var millisecondsPerDay = 1000 * 60 * 60 * 24;
    var millisBetween = two.getTime() - one.getTime();
    var days = millisBetween / millisecondsPerDay;

    // Round down.
    return Math.floor(days);
}

function get_weekday(date) {
    var weekday = new Array(7);
    weekday[0] = "Sunday";
    weekday[1] = "Monday";
    weekday[2] = "Tuesday";
    weekday[3] = "Wednesday";
    weekday[4] = "Thursday";
    weekday[5] = "Friday";
    weekday[6] = "Saturday";
    return weekday[date.getDay()];
}

function hms_to_s(t) { // h:m:s
    var a = t.split(/\D+/);
    return (a[0] * 60 + +a[1]) * 60 + +a[2]
}

(function () {
    if (typeof Object.defineProperty === 'function') {
        try {
            Object.defineProperty(Array.prototype, 'sortBy', {value: sb});
        } catch (e) {
        }
    }
    if (!Array.prototype.sortBy) Array.prototype.sortBy = sb;

    function sb(f) {
        for (var i = this.length; i;) {
            var o = this[--i];
            this[i] = [].concat(f.call(o, o, i), o);
        }
        this.sort(function (a, b) {
            for (var i = 0, len = a.length; i < len; ++i) {
                if (a[i] != b[i]) return a[i] < b[i] ? -1 : 1;
            }
            return 0;
        });
        for (var i = this.length; i;) {
            this[--i] = this[i][this[i].length - 1];
        }
        return this;
    }
})();