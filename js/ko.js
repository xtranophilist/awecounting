
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

    var __construct = function() {
        var uber = {render: $.fn.typeahead.Constructor.prototype.render};
        $.extend($.fn.typeahead.Constructor.prototype, { render: function(items) { uber.render.call(this, items); this.$menu.append('<li class="nostyle"><a href="#item_new_form" class="btn" onclick="$(\'#item_new_form\').modal(\'show\')">Add a new item</a></li>'); return this; }});
    }();

    var self = this;


    self.to = ko.observable('').extend({ required: "Please enter a first name" });

    for (var k in data)
        self[k]=data[k];



    self.particulars = ko.observableArray(ko.utils.arrayMap(data.particulars, function(item) {
        return new ParticularViewModel(item);
    }));

    self.addParticular = function() {
        self.particulars.push(new ParticularViewModel());
    };
    self.removeParticular = function(particular) {
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
        var act = self.quantity() * self.unit_price();
        var amt = act - ((self.discount() * act)/100);
        return amt;
    });

    self.show_items = function(data, event){
        event.preventDefault();
        var item_arr = ["Ahmedabad","Akola","Asansol","Aurangabad","Bangaluru","Baroda","Belgaon","Berhumpur","Calicut","Chennai","Chapra","Cherapunji"];
        var target = (event.currentTarget) ? event.currentTarget : event.srcElement; //for IE <9 compatibility
        $(target).parent().find('.item-complete-box').typeahead({source: item_arr}).trigger('focus').trigger('keyup');
    }
}