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

function setBinding(id, value) {
    var el = document.getElementById(id);
    if (el) {
        el.setAttribute('data-bind', value);
    }
}

function InvoiceViewModel(data){
    var self = this;
    for (var k in data)
        self[k]=data[k]
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
    self.quantity = ko.observable(1);
    self.discount = ko.observable(0);
    for(var k in particular)
        self[k] = ko.observable(particular[k]);

    self.amount = ko.computed(function(){
        var act = self.quantity() * self.unit_price();
        var amt = act - ((self.discount() * act)/100);
        return amt;
    });
}