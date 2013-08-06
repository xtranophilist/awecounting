function DayJournal(data){
    var self = this;
    for (var k in data)
        self[k]=data[k];

    $.ajax({
        url: '/ledger/accounts/json/',
        dataType: 'json',
        async: false,
        success: function(data) {
            self.accounts = data;
        }
    });

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
            $("#day-cash-sales > tr").each(function (index) {
                $($("#day-cash-sales > tr")[index]).addClass('invalid-row');
            });
            for (var i in msg){
                rows[i].id = msg[i];
                $($("#day-cash-sales > tr")[i]).removeClass('invalid-row');
            }
        }
    };

    var day_cash_purchase_options = {
        rows: data.day_cash_purchase,
        save_to_url : '/journal/day/save/day_cash_purchase/',
        properties : {journal_date : self.date},
        onSaveSuccess : function(msg, rows){
            $("#day-cash-purchase > tr").each(function (index) {
                $($("#day-cash-purchase > tr")[index]).addClass('invalid-row');
            });
            for (var i in msg){
                rows[i].id = msg[i];
                $($("#day-cash-purchase > tr")[i]).removeClass('invalid-row');
            }
        }
    };

    var day_cash_receipt_options = {
        rows: data.day_cash_receipt,
        save_to_url : '/journal/day/save/day_cash_receipt/',
        properties : {journal_date : self.date},
        onSaveSuccess : function(msg, rows){
            $("#day-cash-receipt > tr").each(function (index) {
                $($("#day-cash-receipt > tr")[index]).addClass('invalid-row');
            });
            for (var i in msg){
                rows[i].id = msg[i];
                $($("#day-cash-receipt > tr")[i]).removeClass('invalid-row');
            }
        }
    };

    var day_cash_payment_options = {
        rows: data.day_cash_payment,
        save_to_url : '/journal/day/save/day_cash_payment/',
        properties : {journal_date : self.date},
        onSaveSuccess : function(msg, rows){
            $("#day-cash-payment > tr").each(function (index) {
                $($("#day-cash-payment > tr")[index]).addClass('invalid-row');
            });
            for (var i in msg){
                rows[i].id = msg[i];
                $($("#day-cash-payment > tr")[i]).removeClass('invalid-row');
            }
        }
    };



    self.day_cash_sales = new TableViewModel(day_cash_sales_options, DayCashSalesRow);

    self.day_cash_purchase = new TableViewModel(day_cash_purchase_options, DayCashSalesRow);

    self.day_cash_receipt = new TableViewModel(day_cash_receipt_options, DayCashReceiptRow);

    self.day_cash_payment = new TableViewModel(day_cash_payment_options, DayCashReceiptRow);

    self.recordItem = function(item, event){
        item.item_id = get_target(event).data('selected');
    }

    self.recordAccount = function(item, event){
        item.account_id = get_target(event).data('selected');
    }
}

function DayCashSalesRow(row){
    var self = this;

    self.item = ko.observable();
    self.quantity = ko.observable();
    self.amount = ko.observable(0);

    for (var k in row)
        self[k] = ko.observable(row[k]);

    self.rate = ko.computed(function(){
        var rate =  self.amount()/self.quantity();
        return isNaN(rate) ? '' : Math.round(rate*100)/100;
    });

    self.show_items = function(data, event){
        event.preventDefault();
        get_target(event).parent().find('.item-complete-box').trigger('focus').trigger('keyup');
    }
}

function DayCashReceiptRow(row){
    var self = this;

    self.account = ko.observable();
    self.amount = ko.observable(0);

    self.account_id = '';

    for (var k in row)
        self[k] = ko.observable(row[k]);

    self.show_items = function(data, event){
        event.preventDefault();
        get_target(event).parent().find('.item-complete-box').trigger('focus').trigger('keyup');
    }
}