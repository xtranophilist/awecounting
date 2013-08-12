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

    var cash_sales_options = {
        rows: data.cash_sales,
        save_to_url : '/day/save/cash_sales/',
        properties : {day_journal_date : self.date},
        onSaveSuccess : function(msg, rows){
            $("#cash-sales > tr").each(function (index) {
                $($("#cash-sales > tr")[index]).addClass('invalid-row');
            });
            for (var i in msg){
                rows[i].id = msg[i];
                $($("#cash-sales > tr")[i]).removeClass('invalid-row');
            }
        }
    };

    var cash_purchase_options = {
        rows: data.cash_purchase,
        save_to_url : '/day/save/cash_purchase/',
        properties : {day_journal_date : self.date},
        onSaveSuccess : function(msg, rows){
            $("#cash-purchase > tr").each(function (index) {
                $($("#cash-purchase > tr")[index]).addClass('invalid-row');
            });
            for (var i in msg){
                rows[i].id = msg[i];
                $($("#cash-purchase > tr")[i]).removeClass('invalid-row');
            }
        }
    };

    var cash_receipt_options = {
        rows: data.cash_receipt,
        save_to_url : '/day/save/cash_receipt/',
        properties : {day_journal_date : self.date},
        onSaveSuccess : function(msg, rows){
            $("#cash-receipt > tr").each(function (index) {
                $($("#cash-receipt > tr")[index]).addClass('invalid-row');
            });
            for (var i in msg){
                rows[i].id = msg[i];
                $($("#cash-receipt > tr")[i]).removeClass('invalid-row');
            }
        }
    };

    var cash_payment_options = {
        rows: data.cash_payment,
        save_to_url : '/day/save/cash_payment/',
        properties : {day_journal_date : self.date},
        onSaveSuccess : function(msg, rows){
            $("#cash-payment > tr").each(function (index) {
                $($("#cash-payment > tr")[index]).addClass('invalid-row');
            });
            for (var i in msg){
                rows[i].id = msg[i];
                $($("#cash-payment > tr")[i]).removeClass('invalid-row');
            }
        }
    };

    var summary_cash_options = {
        rows: data.cash_payment,
        save_to_url : '/day/save/cash_payment/',
        properties : {day_journal_date : self.date},
        onSaveSuccess : function(msg, rows){
            $("#summary-cash > tr").each(function (index) {
                $($("#summary-cash > tr")[index]).addClass('invalid-row');
            });
            for (var i in msg){
                rows[i].id = msg[i];
                $($("#summary-cash > tr")[i]).removeClass('invalid-row');
            }
        }
    };

    self.cash_sales = new TableViewModel(cash_sales_options, CashSalesRow);

    self.cash_purchase = new TableViewModel(cash_purchase_options, CashSalesRow);

    self.cash_receipt = new TableViewModel(cash_receipt_options, DayCashReceiptRow);

    self.cash_payment = new TableViewModel(cash_payment_options, DayCashReceiptRow);

    self.summary_cash = new TableViewModel(summary_cash_options, DaySummaryCashRow);

    self.recordItem = function(item, event){
        item.item_id = get_target(event).data('selected');
    }

    self.recordAccount = function(item, event){
        item.account_id = get_target(event).data('selected');
    }
}

function CashSalesRow(row){
    var self = this;

    self.sales_ledger = ko.observable();
    self.amount = ko.observable(0);

    for (var k in row)
        self[k] = ko.observable(row[k]);

}

function DayCashReceiptRow(row){
    var self = this;

    self.account = ko.observable();
    self.amount = ko.observable(0);

    self.account_id = '';

    for (var k in row)
        self[k] = ko.observable(row[k]);

}

function DaySummaryCashRow(row){
    var self = this;

    self.opening = ko.observable(1000);
    self.inward = ko.computed(function(){
            return 2000;
        }
    );
    self.outward = ko.observable(0);
    self.closing = ko.observable();
    self.actual = ko.observable();
    self.difference = ko.observable();

    for (var k in row)
        self[k] = ko.observable(row[k]);

}