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
    self.day_cash_sales = new TableViewModel(data.day_cash_sales, DayCashSalesRow, '/journal/day_cash_sales/save');
}


function TableViewModel(data, row_model, save_to_url){
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

    self._initial_rows = $.extend(true, {}, self.rows());

    if (typeof(save_to_url) != 'undefined'){
        self.save = function(model, e){
            var el = get_target(e);
            el.on('mouseover', function() {
                el.html('Save')
            });
            el.html('Saving');
            $.ajax({
                type: "POST",
                url: save_to_url,
                data: ko.toJSON(self),
                success: function(msg){
                    el.html('Save');
                },
                error: function(XMLHttpRequest, textStatus, errorThrown) {
                    el.html("Saving Failed!");
                }
            });

        }
    }
    else{
        self.save= function(){
            throw new Error("'save_to_url' not passed to TableViewModel or save() not implemented!");
        }
    }


    self.reset= function(){
        console.log(self.rows());
        console.log(self._initial_rows[0]);
        self.rows(self._initial_rows);
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