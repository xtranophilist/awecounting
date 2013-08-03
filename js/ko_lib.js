//Custom Bindings
ko.bindingHandlers.typeahead = {
    init: function (element, valueAccessor) {
        $(element).attr("autocomplete", "off")
            .typeahead({
                minLength: 0,
                source: function(query, process) {
                    objects = [];
                    map = {};
                    var data = ko.utils.unwrapObservable(valueAccessor());
                    $.each(data, function(i, object) {
                        map[object.name] = object;
                        objects.push(object.name);
                    });
                    process(objects);
                },
                updater: function(selection){
                    invoice_view_instance.updateParticular(this.$element[0].getAttribute('data-index'), map[selection]);
                    return selection;
                }
            });
    }
};


ko.bindingHandlers.editableText = {
    init: function(element, valueAccessor) {
        $(element).attr('contenteditable', true);
        $(element).on('blur', function() {
            var observable = valueAccessor();
            if (typeof (observable) == 'function'){
                observable( $(this).text() );
            }
        });
    },
    update: function(element, valueAccessor) {
        var value = ko.utils.unwrapObservable(valueAccessor());
        $(element).text(value);
    }
};

ko.bindingHandlers.numeric = {
    init: function(element, valueAccessor) {
        $(element).on('keydown', function(event) {

            // Allow: backspace, delete, tab, escape, and enter
            if ( event.keyCode == 46 || event.keyCode == 8 || event.keyCode == 9 || event.keyCode == 27 || event.keyCode == 13 ||
                // Allow: Ctrl combinations
                (event.ctrlKey === true) ||
                //Allow decimal symbol (.)
                (event.keyCode === 190) ||
                // Allow: home, end, left, right
                (event.keyCode >= 35 && event.keyCode <= 39)) {
                // let it happen, don't do anything
                return;
            }
            else {
                // Ensure that it is a number and stop the keypress
                if (event.shiftKey || (event.keyCode < 48 || event.keyCode > 57) && (event.keyCode < 96 || event.keyCode > 105 )) {
                    event.preventDefault();
                }
            }
        });
    },
    update: function(element, valueAccessor) {
    }
};

//Custom Observable Extensions
ko.extenders.numeric = function(target, precision) {
    //create a writeable computed observable to intercept writes to our observable
    var result = ko.computed({
        read: target,  //always return the original observables value
        write: function(newValue) {
            var current = target(),
                roundingMultiplier = Math.pow(10, precision),
                newValueAsNum = isNaN(newValue) ? current : parseFloat(+newValue),
                valueToWrite = Math.round(newValueAsNum * roundingMultiplier) / roundingMultiplier;

            //only write if it changed
            if (valueToWrite !== current) {
                target(valueToWrite);
            } else {
                //if the rounded value is the same, but a different value was written, force a notification for the current field
                if (newValue !== current) {
                    target.notifySubscribers(valueToWrite);
                }
            }
        }
    });

    //initialize with current value to make sure it is rounded appropriately
    result(target());

    //return the new computed observable
    return result;
};

ko.bindingHandlers.bind = {
    init: function(element, valueAccessor) {
        element = $(element);
        var config = {
            template: element.html()
        };
        element.data('bind.config', config);
// Why reset data-bind attributes? Because the point of this
// binding is so that nested bindings apply to the value, not
// to the current model. This prevents Knockout from continuing
// to apply the current model to nested elements. Remember, the
// nested bindings are still captured by `config.template` above.
        element.find('[data-bind]').attr('data-bind', '');
    },
    update: function(element, valueAccessor) {
        element = $(element);
        var config = element.data('bind.config');
        var model = ko.utils.unwrapObservable(valueAccessor());
        if (model) {
            element.html(config.template);
// Save and unset the data-bind attribute so we can apply
// the new model to the element instead of its children
// individually.
            var bindings = element.attr('data-bind');
            element.attr('data-bind', '');
            ko.applyBindings(model, element[0]);
// Reset the element's data-bind attribute.
            element.attr('data-bind', bindings);
        }
        else
            element.empty();
    }
};

//Other useful KO-related functions
function setBinding(id, value) {
    var el = document.getElementById(id);
    if (el) {
        el.setAttribute('data-bind', value);
    }
}

