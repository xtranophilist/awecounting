$(document).ready(function () {
    $('#inv-date').datepicker().data('datepicker');
    $('#due-date').datepicker({relative_to: '#inv-date'});
});


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

    self.message = ko.observable('');

    var invoice_options = {
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

    self.save = function(item, event){
        $.ajax({
            type: "POST",
            url: '/voucher/invoice/save/',
            data: ko.toJSON(self),
            success: function(msg){
                if (typeof (msg.error_message) != 'undefined'){
                    $('#message').html(msg.error_message);
                }
                else{
                    $('#message').html('Saved!');
                    console.log(msg);
                    if (msg.id)
                        self.id = msg.id;
                    $("#particulars-body > tr").each(function (i) {
                        $($("#particulars-body > tr")[i]).addClass('invalid-row');
                    });
                    for (var i in msg.rows){
                        self.particulars.rows()[i].id = msg.rows[i];
                        $($("#particulars-body > tr")[i]).removeClass('invalid-row');
                    }
                }
            }
//            error: function(XMLHttpRequest, textStatus, errorThrown) {
//                $('#message').html(XMLHttpRequest.responseText.message);
//            }
        });
    }

    self.grand_total = function(){
        var sum = 0;
        self.particulars.rows().forEach(function(i){
            sum += i.amount();
        });
        return sum;
    }

    self.itemChanged = function(row){
        var selected_item = $.grep(self.items, function(i){
            return i.id == row.item_id();
        })[0];
        if (!selected_item) return;
        if (!row.description())
            row.description(selected_item.description);
        if (!row.unit_price())
            row.unit_price(selected_item.sales_price);
        if (!row.tax_scheme())
            row.tax_scheme(selected_item.tax_scheme);
    }

}

function ParticularViewModel(particular){

    var self = this;
    //default values
    self.item_id = ko.observable();
    self.description = ko.observable('');
    self.unit_price= ko.observable(0);
    self.quantity = ko.observable(1).extend({ numeric: 2 });
    self.discount = ko.observable(0).extend({ numeric: 2 });
    self.tax_scheme = ko.observable();

    for(var k in particular)
        self[k] = ko.observable(particular[k]);

    if (self.discount()==null)
        self.discount(0);

    self.amount = ko.computed(function(){
        var wo_discount = self.quantity() * self.unit_price();
        var amt = wo_discount - ((self.discount() * wo_discount)/100);
        return amt;
    });

}

