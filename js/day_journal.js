function DayJournal(data){
    var self = this;
    for (var k in data)
        self[k]=data[k];

    $.ajax({
        url: '/ledger/accounts/'+self.date+'.json',
        dataType: 'json',
        async: false,
        success: function(data) {
            self.accounts = data;
        }
    });

    $.ajax({
        url: '/inventory/accounts/'+self.date+'.json',
        dataType: 'json',
        async: false,
        success: function(data) {
            self.inventory_accounts = data;
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

    self.lotto_changed = function(row){
        var selected_account = $.grep(self.accounts, function(i){
            return i.id == row.particular();
        })[0];
        if (typeof selected_account == 'undefined')
            return;
        $.each(self.cash_sales.rows(), function(key, value){
            if (value.account_id() == selected_account.id){
                row.disp(value.amount());
                return false;
            }
        });
    }

    self.account_changed = function(row){
        var selected_account = $.grep(self.accounts, function(i){
            return i.id == row.account_id();
        })[0];
        if (typeof selected_account == 'undefined')
            return;
        row.opening(selected_account.opening);
    }

    self.inventory_account_changed = function(row){
        var selected_account = $.grep(self.inventory_accounts, function(i){
            return i.id == row.account_id();
        })[0];
        if (typeof selected_account == 'undefined')
            return;
        row.opening(selected_account.opening);
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
                if (intersection(tags, account_tags).length){
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

    self.account_by_id = function(id){
        var account = $.grep(self.accounts, function(i){
            return i.id == id;
        });
        return account[0];
    }

    var validate = function(msg, rows, tr_wrapper_id){
        console.log(tr_wrapper_id);
        var selection = $("#" + tr_wrapper_id + " > tr");
        selection.each(function (index) {
            $(selection[index]).addClass('invalid-row');
        });
        for (var i in msg['saved']){
            rows[i].id = msg['saved'][''+i+''];
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

    var bank_validate = function(msg, rows, tr_wrapper_id, i){
        var selection = $('#' + tr_wrapper_id + '-' + i + ' > tr');
        selection.each(function (index) {
            $(selection[index]).addClass('invalid-row');
        });
        for (var i in msg['saved']){
            rows[i].id = msg['saved'][''+i+''];
            $(selection[i]).removeClass('invalid-row');
        }
        var model = self[tr_wrapper_id.toUnderscore()]()[i];
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

    var validate_with_extra_row = function(msg, rows, tr_wrapper_id, extra_row_id){
        var selection = $("#" + tr_wrapper_id + " > tr");
        selection.each(function (index) {
            $(selection[index]).addClass('invalid-row');
        });
        for (var i in msg['saved']){
            if (i=='0'){
                $('#'+extra_row_id).removeClass('invalid-row');
            }else{
                rows[i-1].id = msg['saved'][i];
                $(selection[i]).removeClass('invalid-row');
            }
        }
        var model = self[tr_wrapper_id.toUnderscore()];
        var saved_size = Object.size(msg['saved']) ;
        var rows_size = rows.length + 1
        if(saved_size==rows_size)
            model.message('Saved!');
        else if(saved_size==0){
            model.message('No rows saved!');
            model.status('error');
        }
        else if(saved_size<rows_size){
            var message = saved_size.toString() +' row' + ((saved_size==1)?'':'s') + ' saved! ';
            message += (rows_size-saved_size).toString() +' row' + ((rows_size-saved_size==1)?' is':'s are') + ' incomplete!';
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

    var key_to_options_with_extra_row = function(key, extra_row, extra_row_model){
        var properties = {}
        properties['day_journal_date'] = self.date;
        if (self[extra_row])
            properties[extra_row] = new extra_row_model(self[extra_row][0]);
        return {
            rows: data[key],
            save_to_url : '/day/save/' + key + '/',
            properties: properties,
            onSaveSuccess : function(msg, rows){
                validate_with_extra_row(msg, rows, key.toDash(), extra_row.toDash());

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

    self.summary_bank = new TableViewModel(key_to_options('summary_bank'), BankRow);

    self.summary_lotto = new TableViewModel(key_to_options('summary_lotto'), LottoRow);

    self.summary_sales_tax = new TableViewModel(key_to_options('summary_sales_tax'), CashRow);

    self.summary_equivalent = new TableViewModel(key_to_options_with_extra_row('summary_equivalent', 'summary_cash', SummaryCashModel), SummaryEquivalentRow);

    self.summary_transfer = new TableViewModel(key_to_options_with_extra_row('summary_transfer', 'summary_utility', SummaryUtilityModel), SummaryTransferRow);

    self.summary_inventory = new TableViewModel(key_to_options('summary_inventory'), SummaryEquivalentRow);

    //adding new bank accounts if they don't already exist for the current day journal
    for (var i in self.accounts_by_tag('Bank')){
        var account = self.accounts_by_tag('Bank')[i];
        var exists = false;
        for (var j in self.bank_detail){
            var detail = self.bank_detail[j];
            if (detail.bank_account == account.id){
                exists = true;
            }
        }
        if (!exists){
            self.bank_detail.push({bank_account: account.id, rows: []});
        }
    }

    var i=0;
    self.bank_detail = ko.observableArray(ko.utils.arrayMap(self.bank_detail, function(item) {
        var options = bank_key_to_option(i++);
        return new TableViewModel(options, BankDetailRow);
    }));


    function bank_key_to_option(i){
        return {
            rows: data.bank_detail[i].rows,
            save_to_url : '/day/save/bank_detail/' + self.bank_detail[i].bank_account + '/',
            properties : {
                day_journal_date : self.date,
                title: self.account_by_id(self.bank_detail[i].bank_account).name,
                bank_account_id : self.bank_detail[i].bank_account,
                id : self.bank_detail[i].id
            },
            onSaveSuccess : function(msg, rows){
                bank_validate(msg, rows, 'bank-detail', i);
            }
        };
    }

}

function BankDetailRow(row){

    var self = this;

    self.account_id = ko.observable();
    self.type = ko.observable();
    self.amount = ko.observable();

    for (var k in row){
            self[k] = ko.observable(row[k]);
    }

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
            if (!isNaN(this.amount()))
                total += parseInt(this.amount());
        });
        $.each(root.cash_receipt.rows(), function(){
            if (!isNaN(this.amount()))
                total += parseInt(this.amount());
        });
        return total;
    };

    self.outward = function(root){
        var total = 0;
        $.each(root.cash_purchase.rows(), function(){
            if (!isNaN(this.amount()))
                total += parseInt(this.amount());
        });
        $.each(root.cash_payment.rows(), function(){
            if (!isNaN(this.amount()))
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

    self.actual = ko.observable();

    for (var k in data){
        self[k] = ko.observable(data[k]);
    }
}

function BankRow(row){
    var self = this;

    self.bank_account = ko.observable();
    self.cheque_deposit = ko.observable();
    self.cash_deposit = ko.observable();

    for (var k in row)
        self[k] = ko.observable(row[k]);
}

function LottoRow(row){
    var self = this;

    self.particular = ko.observable();
    self.disp = ko.observable();
    self.reg = ko.observable();

    self.diff = function(){
        var diff =  parseInt(self.disp()) - parseInt(self.reg());
        return isNaN(diff)?'':diff;
    };

    for (var k in row)
        self[k] = ko.observable(row[k]);
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

function SummaryUtilityModel(data){
    var self = this;

    self.amount = ko.observable();

    for (var k in data){
        self[k] = ko.observable(data[k]);
    }

}

function SummaryTransferRow(row){
    var self = this;

    self.transfer_type = ko.observable();
    self.inward = ko.observable();
    self.outward = ko.observable();

    for (var k in row){
        self[k] = ko.observable(row[k]);
    }

}