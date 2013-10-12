function init_select2(element, callback) {
    if ($(element).data('add-url')) {
        var drop_class = '.drop-' + $(element).data('field').toLowerCase().replace(' ', '-');
        $('.drop-' + $(element).data('field').toLowerCase()).find('.appended-link').remove();
        var el = jQuery('<a/>', {
            class: 'appended-link',
            href: $(element).data('add-url'),
            title: 'Add New ' + $(element).data('field'),
            text: 'Add New ' + $(element).data('field'),
            'data-toggle': 'modal'
        }).appendTo(drop_class);
        el.on('click', function (e) {
            el.parent().toggle();
            window.last_active_select = element;
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
        });
    }
}

function return_name(obj) {
    return obj.name;
}

//Triggers on document-ready
$(document).ready(function () {
    $('.select2').select2({'dropdownAutoWidth': true});

    $('.delete-warn').click(function (e) {
        if (confirm('Are you sure you want to delete?')) {
            return true;
        } else return false;
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
            $target.html(data);
        }
    });

    event.preventDefault();
}

on_form_submit = function (event) {
    alert('1');
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

function get_target(e) {
    return $((e.currentTarget) ? e.currentTarget : e.srcElement); //for IE <9 compatibility
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
    self.status = ko.observable('standby');


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

    }


    if (typeof(options.save_to_url) != 'undefined') {
        self.save = function (model, e) {
            self.status('waiting');
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
                    self.status('success');
                    self.deleted_rows = [];
                },
                error: function (XMLHttpRequest, textStatus, errorThrown) {
                    self.message('Saving Failed!');
                    self.status('error');
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