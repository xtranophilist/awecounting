function InvoiceViewModel(data){

    var self = this;

    $.ajax({
      url: '/inventory/items/json/',
      dataType: 'json',
      async: false,
      success: function(data) {
        self.items = data;
      }
    });

    for (var k in data)
        self[k]=data[k];

//    self.rows = ko.observableArray(ko.utils.arrayMap(data.particulars, function(item) {
//        return new ParticularViewModel(item);
//    }));

    invoice_options = {
      rows: data.particulars
    };

    self.particulars = new TableViewModel(invoice_options, ParticularViewModel);


//    self.addParticular = function() {
//        var new_item_index = self.particulars().length+1;
//        self.particulars.push(new ParticularViewModel({ sn: new_item_index }));
//    };
//
//    self.removeParticular = function(particular) {
//        for (var i = particular.sn(); i < self.particulars().length; i++) {
//            self.particulars()[i].sn(self.particulars()[i].sn()-1);
//        };
//        self.particulars.remove(particular);
//    };
//
    self.save = function(item, event){

        $.post('/voucher/invoice/save/', ko.toJSON(self), function(){  el.html('Save'); });
    }

    self.grand_total = function(){
        var sum = 0;
        self.particulars.rows().forEach(function(i){
            sum += i.amount();
        });
        return sum;
    }

//    self.updateParticular = function(item, event){
//        var key = $(event.currentTarget).data('selected');
//        if(key){
//            var selected_item = $.grep(self.items, function(e){ return e.id == key; })[0];
//            var model = self.particulars()[item.sn()-1];
//            model.description(selected_item.description);
//            model.unit_price(selected_item.sales_price);
//            model.item_name = selected_item.name;
//        }
//    }

}

function ParticularViewModel(particular){

    var self = this;
    //default values
    self.item_id = ko.observable('');
    self.description = ko.observable('');
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
        get_target(event).parent().find('.item-complete-box').trigger('focus').trigger('keyup');
    }
}

