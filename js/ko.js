$(document).on('mouseup mousedown', '[contenteditable]',function(){
  this.focus();
});

function compare_by_sn(a,b) {
  if (a.sn() < b.sn())
     return -1;
  if (a.sn() > b.sn())
    return 1;
  return 0;
}

ko.bindingHandlers.typeahead = {
            init: function (element, valueAccessor) {
                $(element).attr("autocomplete", "off")
                .typeahead({
                    'source': ko.utils.unwrapObservable(valueAccessor())
                });
            }
        };

ko.bindingHandlers.editableText = {
    init: function(element, valueAccessor) {
        $(element).on('blur', function() {
            var observable = valueAccessor();
            observable( $(this).text() );
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

function setBinding(id, value) {
    var el = document.getElementById(id);
    if (el) {
        el.setAttribute('data-bind', value);
    }
}

function InvoiceViewModel(data){

    var self = this;

    self.items = ["Ahmedabad","Akola","Asansol","Aurangabad","Bangaluru","Baroda","Belgaon","Berhumpur","Calicut","Chennai","Chapra","Cherapunji"];

    for (var k in data)
        self[k]=data[k];

    self.particulars = ko.observableArray(ko.utils.arrayMap(data.particulars, function(item) {
        return new ParticularViewModel(item);
    }));

    self.activate_ui = function(){

        // Typeahead
        var uber = {render: $.fn.typeahead.Constructor.prototype.render};
        $.extend($.fn.typeahead.Constructor.prototype, { render: function(items) { uber.render.call(this, items); this.$menu.append('<li class="nostyle"><a href="#item_new_form" class="btn" onclick="$(\'#item_new_form\').modal(\'show\')">Add a new item</a></li>'); return this; }});

        var fixHelper = function(e, ui) {
        ui.children().each(function() {
        $(this).width($(this).width());
        });
        return ui;
        };

        // Drag and sort
        var startIndex = -1;
        var sortable_setup = {
          helper: fixHelper, 
          handle: '.drag_handle',
          start: function (event, ui) {
            // item index when the dragging starts
            startIndex = ui.item.index();
          },
          stop: function(event, ui){
            // get the new location item index
            var newIndex = ui.item.index();

            var prev_model = self.particulars()[startIndex];
            var curr_model = self.particulars()[newIndex];

            var prev_sn = prev_model.sn();
            var curr_sn = curr_model.sn();

            prev_model.sn(curr_sn);
            curr_model.sn(prev_sn);

            var particulars = self.particulars();
            var sorted_particulars = particulars.sort(compare_by_sn);
    
            self.particulars([]);
            self.particulars(sorted_particulars);

          }
        };

        $("#voucher_table tbody").sortable(sortable_setup).disableSelection();
    }

    self.activate_ui();

    self.addParticular = function() {
        var new_item_index = self.particulars().length+1;
        self.particulars.push(new ParticularViewModel({ sn: new_item_index }));
    };
    self.removeParticular = function(particular) {
        for (var i = particular.sn(); i < self.particulars().length; i++) {
          self.particulars()[i].sn(self.particulars()[i].sn()-1);
        };
        self.particulars.remove(particular);
    };
    self.save = function(){
        console.log(self);
    }

    self.grand_total = function(){
        var sum = 0;
        self.particulars().forEach(function(i){
            sum += i.amount();
        });
        return sum;
    }

}

function ParticularViewModel(particular){

    var self = this;
    //default values
    self.item_name = '';
    self.description = '';
    self.unit_price= ko.observable(0);
    self.quantity = ko.observable(1).extend({ numeric: 2 });
    self.discount = ko.observable(0).extend({ numeric: 2 });
    for(var k in particular)
        self[k] = ko.observable(particular[k]);

    self.amount = ko.computed(function(){
        var wo_discount = self.quantity() * self.unit_price();
        var amt = wo_discount - ((self.discount() * wo_discount)/100);
        return amt;
    });

    self.show_items = function(data, event){
        event.preventDefault();
        var target = (event.currentTarget) ? event.currentTarget : event.srcElement; //for IE <9 compatibility
        $(target).parent().find('.item-complete-box').trigger('focus').trigger('keyup');
    }
}