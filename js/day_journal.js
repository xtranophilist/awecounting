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

    self.accountChanged = function(row){
        var selected_account = $.grep(self.accounts, function(i){
            return i.id == row.account_id();
        })[0];
        if (typeof selected_account == 'undefined')
            return;
        row.opening(selected_account.current_balance);
    }

    self.accounts_by_tag = function(tags, is_or){
        var filtered_accounts = [];
        for (var i in self.accounts){
            var account_tags = self.accounts[i].tags
            if( typeof tags === 'string' ) {
                if ($.inArray(tags, account_tags) !== -1){
                    filtered_accounts.push(self.accounts[i]);
                }
            }else if(typeof is_or != 'undefined'){
                if (intersect_safe(tags, account_tags).length){
                    filtered_accounts.push(self.accounts[i]);
                }
            }else{
                if (compare_arrays(tags, account_tags)){
                    filtered_accounts.push(self.accounts[i]);
                }
            }
        }
        return filtered_accounts;
    };

    var validate = function(msg, rows, tr_wrapper_id){
        var selection = $("#" + tr_wrapper_id + " > tr");
        selection.each(function (index) {
            $(selection[index]).addClass('invalid-row');
        });
        for (var i in msg['saved']){
            rows[i].id = msg[i];
            $(selection[i]).removeClass('invalid-row');
        }
        var model = self[tr_wrapper_id.toUnderscore()];
        var saved_size = Object.size(msg['saved']) ;
        if(saved_size==rows.length)
            model.message('Saved!');
        else if(saved_size==0){
            model.message('No rows saved!');
            model.status('error');
        }
        else if(saved_size<rows.length){
            var message = saved_size.toString() +' row' + ((saved_size==1)?'':'s') + ' saved! ';
            message += (rows.length-saved_size).toString() +' row' + ((rows.length-saved_size==1)?' is':'s are') + ' incomplete!';
            model.message(message);
            model.status('error');
        }
    }

    var key_to_options = function(key){
        return {
            rows: data[key],
            save_to_url : '/day/save/' + key + '/',
            properties : {day_journal_date : self.date},
            onSaveSuccess : function(msg, rows){
                validate(msg, rows, key.toDash());
            }
        };
    }

    self.cash_sales = new TableViewModel(key_to_options('cash_sales'), CashRow);

    self.cash_purchase = new TableViewModel(key_to_options('cash_purchase'), CashRow);

    self.cash_receipt = new TableViewModel(key_to_options('cash_receipt'), CashRow);

    self.cash_payment = new TableViewModel(key_to_options('cash_payment'), CashRow);

    self.credit_sales = new TableViewModel(key_to_options('credit_sales'), CreditRow);

    self.credit_purchase = new TableViewModel(key_to_options('credit_purchase'), CreditRow);

    self.credit_income = new TableViewModel(key_to_options('credit_income'), CreditRow);

    self.credit_expense = new TableViewModel(key_to_options('credit_expense'), CreditRow);

    var summary_cash_and_equivalent_options = {
        rows: data['summary_equivalent'],
        save_to_url : '/day/save/' + 'summary_cash_and_equivalent' + '/',
        properties : {day_journal_date : self.date, summary_cash: new SummaryCashModel(self.summary_cash)},
        onSaveSuccess : function(msg, rows){
            validate(msg, rows, 'summary-cash-and-equivalent');

        }
    };

    self.summary_cash_and_equivalent = new TableViewModel(summary_cash_and_equivalent_options, SummaryEquivalentRow);
}

function SummaryCashModel(data){
    var self = this;

    self.opening = function(all_accounts){
        var cash_account = all_accounts.filter(function(element, index, array){
            if (element.name == 'Cash Account')
                return element;
        })[0];
        return cash_account.current_balance;
    };

    self.inward = function(root){
        var total = 0;
        $.each(root.cash_sales.rows(), function(){
            total += parseInt(this.amount());
        });
        $.each(root.cash_receipt.rows(), function(){
            total += parseInt(this.amount());
        });
        return total;
    };

    self.outward = function(root){
        var total = 0;
        $.each(root.cash_purchase.rows(), function(){
            total += parseInt(this.amount());
        });
        $.each(root.cash_payment.rows(), function(){
            total += parseInt(this.amount());
        });
        return total;
    };

    self.closing = function(root){
        return self.opening(root.accounts) + self.inward(root) - self.outward(root);
    };

    self.difference = function(root){
        return self.actual() - self.closing(root);
    };

    self.actual = ko.observable(0);

    for (var k in data)
        self[k] = ko.observable(data[k]);
}

function CashRow(row){
    var self = this;

    self.account_id = ko.observable();
    self.amount = ko.observable();

    for (var k in row)
        self[k] = ko.observable(row[k]);

}

function CreditRow(row){
    var self = this;

    self.account_cr_id = ko.observable();
    self.account_dr_id = ko.observable();
    self.amount = ko.observable();

    for (var k in row)
        self[k] = ko.observable(row[k]);

}

function SummaryEquivalentRow(row){
    var self = this;

    self.account_id = ko.observable()

    self.opening = ko.observable();

    self.inward = ko.observable(0).extend({ numeric: 2 });
    self.outward = ko.observable(0).extend({ numeric: 2 });

    self.closing = ko.computed(function(){
        var closing = parseInt(self.opening()) + parseInt(self.inward()) - parseInt(self.outward());
        return isNaN(closing)?'':closing;
    });

    self.actual = ko.observable();

    self.difference = function(){
        var diff =  self.actual() - self.closing();
        return isNaN(diff)?'':diff;
    };

    for (var k in row)
        self[k] = ko.observable(row[k]);

}