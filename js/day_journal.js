function DayJournal(data){
    var self = this;
    for (var k in data)
        self[k]=data[k];
    $.ajax({
        url: '/inventory/items/json/',
        dataType: 'json',
        async: false,
        success: function(data) {
            self.items = data;
        }
    });
    data.day_cash_sales.journal_date = self.date;


    self.updateItem = function(item, event){
        var key = $(event.currentTarget).data('selected');
        if(key){
            var selected_item = $.grep(self.items, function(e){ return e.id == key; })[0];
            item.item = selected_item.name;
        }
    }

    data.day_cash_sales.required = ['item', 'amount']


    self.day_cash_sales = new TableViewModel(data.day_cash_sales, DayCashSalesRow, '/journal/day/save/day_cash_sales/');
}

function DayCashSalesRow(row){
    var self = this;

    for (var k in row)
        self[k] = row[k];

    self.item = '';
    self.quantity = ko.observable();
    self.amount = ko.observable(0);

    self.rate = ko.computed(function(){
        var rate =  self.amount()/self.quantity();
        return isNaN(rate) ? '' : rate;
    });

    self.show_items = function(data, event){
        event.preventDefault();
        get_target(event).parent().find('.item-complete-box').trigger('focus').trigger('keyup');
    }
}