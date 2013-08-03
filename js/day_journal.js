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

    var day_cash_sales_options = {
        rows: data.day_cash_sales,
        save_to_url : '/journal/day/save/day_cash_sales/',
        properties : {journal_date : self.date},
        onSaveSuccess : function(msg, rows){
            for (var i in msg){
                rows[i].id = msg[i];
            }
        }
    };

    self.day_cash_sales = new TableViewModel(day_cash_sales_options, DayCashSalesRow);

    self.recordItem = function(item, event){
        item.item_id = get_target(event).data('selected');
    }
}

function DayCashSalesRow(row){
    var self = this;

    for (var k in row)
        self[k] = ko.observable(row[k]);

    self.item = ko.observable();
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