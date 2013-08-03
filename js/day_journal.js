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
    self.day_cash_sales = new TableViewModel(data.day_cash_sales, DayCashSalesRow);
}


function TableViewModel(data, row_model){
    var self = this;
    for (var k in data)
        self[k]=data[k];

    self.rows = ko.observableArray(ko.utils.arrayMap(data.rows, function(item) {
        return new row_model(item);
    }));

    self.hasNoRows = ko.computed(function(){
    return self.rows().length === 0;
  });

    self.addRow = function() {
        var new_item_index = self.rows().length+1;
        self.rows.push(new row_model());
    };

    self.removeRow = function(row) {
        self.rows.remove(row);
    };

    if (self.hasNoRows){
        self.addRow();
    }

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