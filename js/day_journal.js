function DayJournal(data){
    var self = this;
    for (var k in data)
        self[k]=data[k];
    console.log(data);
    self.day_cash_sales = DayCashSales(data.day_cash_sales);
}


function DayCashSales(data){
    var self = this;
    for (var k in data)
        self[k]=data[k];
    self.item = '';
    self.quantity = ko.observable();
    self.rate = ko.observable();
    self.amount = ko.observable(0);


    self.rows = ko.observableArray(ko.utils.arrayMap(data.particulars, function(item) {
        return new DayCashSalesRow(item);
    }));

    self.addRow = function() {
        var new_item_index = self.rows().length+1;
        self.rows.push(new DayCashSalesRow({ sn: new_item_index }));
    };

    self.removeRow = function(row) {
        for (var i = row.sn(); i < self.rows().length; i++) {
            self.rows()[i].sn(self.rows()[i].sn()-1);
        };
        self.rows.remove(row);
    };

}

function DayCashSalesRow(row){
    var self = this;
    for (var k in row)
        self[k] = row[k];
    self.show_items = function(data, event){
        event.preventDefault();
        get_target(event).parent().find('.item-complete-box').trigger('focus').trigger('keyup');
    }
}