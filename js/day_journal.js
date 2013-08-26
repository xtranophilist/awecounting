function DayJournal(data) {
    var self = this;
    self.sales_tax = ko.observable();
    for (var k in data)
        self[k] = data[k];

    $.ajax({
        url: '/ledger/accounts/' + self.date + '.json',
        dataType: 'json',
        async: false,
        success: function (data) {
            self.accounts = data;
        }
    });

    $.ajax({
        url: '/inventory/accounts/' + self.date + '.json',
        dataType: 'json',
        async: false,
        success: function (data) {
            self.inventory_accounts = data;
        }
    });

//    $.ajax({
//        url: '/inventory/items/json/',
//        dataType: 'json',
//        async: false,
//        success: function(data) {
//            self.items = data;
//        }
//    });

    self.lotto_changed = function (row) {
        var selected_account = $.grep(self.accounts, function (i) {
            return i.id == row.particular();
        })[0];
        if (typeof selected_account == 'undefined')
            return;
        $.each(self.cash_sales.rows(), function (key, value) {
            if (value.account_id() == selected_account.id) {
                row.disp(value.amount());
                return false;
            }
        });
    }

    self.account_changed = function (row, event) {
        var selected_account = $.grep(self.accounts, function (i) {
            return i.id == row.account_id();
        })[0];
        if (typeof selected_account == 'undefined')
            return;
        if (typeof row.tax_rate == 'function')
            row.tax_rate(selected_account.tax_rate);
        if (typeof row.opening == 'function')
            row.opening(selected_account.opening);
    }

    self.account_cr_changed = function (row, event) {
        var selected_account = $.grep(self.accounts, function (i) {
            return i.id == row.account_cr_id();
        })[0];
        if (typeof selected_account == 'undefined')
            return;
        if (typeof row.tax_rate == 'function')
            row.tax_rate(selected_account.tax_rate);
        if (typeof row.opening == 'function')
            row.opening(selected_account.opening);
    }

    self.inventory_account_changed = function (row) {
        var selected_account = $.grep(self.inventory_accounts, function (i) {
            return i.id == row.account_id();
        })[0];
        if (typeof selected_account == 'undefined')
            return;
        row.opening(selected_account.opening);
    }

    self.accounts_by_category = function (categories, is_or) {
        var filtered_accounts = [];
        for (var i in self.accounts) {
            var account_categories = self.accounts[i].categories
            if (typeof categories === 'string') {
                if ($.inArray(categories, account_categories) !== -1) {
                    filtered_accounts.push(self.accounts[i]);
                }
            } else if (typeof is_or != 'undefined') {
                if (intersection(categories, account_categories).length) {
                    filtered_accounts.push(self.accounts[i]);
                }
            } else {
                if (compare_arrays(categories, account_categories)) {
                    filtered_accounts.push(self.accounts[i]);
                }
            }
        }
        return filtered_accounts;
    };

    self.account_by_id = function (id) {
        var account = $.grep(self.accounts, function (i) {
            return i.id == id;
        });
        return account[0];
    }

    var validate = function (msg, rows, tr_wrapper_id) {
        console.log(tr_wrapper_id);
        var selection = $("#" + tr_wrapper_id + " > tr");
        selection.each(function (index) {
            $(selection[index]).addClass('invalid-row');
        });
        for (var i in msg['saved']) {
            rows[i].id = msg['saved']['' + i + ''];
            $(selection[i]).removeClass('invalid-row');
        }
        var model = self[tr_wrapper_id.toUnderscore()];
        var saved_size = Object.size(msg['saved']);
        if (saved_size == rows.length)
            model.message('Saved!');
        else if (saved_size == 0) {
            model.message('No rows saved!');
            model.status('error');
        }
        else if (saved_size < rows.length) {
            var message = saved_size.toString() + ' row' + ((saved_size == 1) ? '' : 's') + ' saved! ';
            message += (rows.length - saved_size).toString() + ' row' + ((rows.length - saved_size == 1) ? ' is' : 's are') + ' incomplete!';
            model.message(message);
            model.status('error');
        }
    }

    var validate_with_extra_row = function (msg, rows, tr_wrapper_id, extra_row_id) {
        var selection = $("#" + tr_wrapper_id + " > tr");
        selection.each(function (index) {
            $(selection[index]).addClass('invalid-row');
        });
        for (var i in msg['saved']) {
            if (i == '0') {
                $('#' + extra_row_id).removeClass('invalid-row');
            } else {
                rows[i - 1].id = msg['saved'][i];
                $(selection[i]).removeClass('invalid-row');
            }
        }
        var model = self[tr_wrapper_id.toUnderscore()];
        var saved_size = Object.size(msg['saved']);
        var rows_size = rows.length + 1
        if (saved_size == rows_size)
            model.message('Saved!');
        else if (saved_size == 0) {
            model.message('No rows saved!');
            model.status('error');
        }
        else if (saved_size < rows_size) {
            var message = saved_size.toString() + ' row' + ((saved_size == 1) ? '' : 's') + ' saved! ';
            message += (rows_size - saved_size).toString() + ' row' + ((rows_size - saved_size == 1) ? ' is' : 's are') + ' incomplete!';
            model.message(message);
            model.status('error');
        }
    }

    var key_to_options = function (key) {
        return {
            rows: data[key],
            save_to_url: '/day/save/' + key + '/',
            properties: {day_journal_date: self.date},
            onSaveSuccess: function (msg, rows) {
                validate(msg, rows, key.toDash());
            }
        };
    }

    var key_to_options_with_extra_row = function (key, extra_row, extra_row_model) {
        var properties = {}
        properties['day_journal_date'] = self.date;
        if (self[extra_row])
            properties[extra_row] = new extra_row_model(self[extra_row][0]);
        return {
            rows: data[key],
            save_to_url: '/day/save/' + key + '/',
            properties: properties,
            onSaveSuccess: function (msg, rows) {
                validate_with_extra_row(msg, rows, key.toDash(), extra_row.toDash());

            }
        };
    }

    self.cash_sales = new TableViewModel(key_to_options('cash_sales'), CashSalesRow);

    self.cash_purchase = new TableViewModel(key_to_options('cash_purchase'), CashRow);

    self.cash_receipt = new TableViewModel(key_to_options('cash_receipt'), CashRow);

    self.cash_payment = new TableViewModel(key_to_options('cash_payment'), CashRow);

    self.credit_sales = new TableViewModel(key_to_options('credit_sales'), CreditSalesRow);

    self.credit_purchase = new TableViewModel(key_to_options('credit_purchase'), CreditRow);

    self.credit_income = new TableViewModel(key_to_options('credit_income'), CreditRow);

    self.credit_expense = new TableViewModel(key_to_options('credit_expense'), CreditRow);

    self.summary_lotto = new TableViewModel(key_to_options('summary_lotto'), LottoRow);

    self.summary_sales_tax = new TableViewModel(key_to_options('summary_sales_tax'), SummaryTaxRow);
    self.summary_sales_tax.rows()[0].register(self.sales_tax);

    self.summary_equivalent = new TableViewModel(key_to_options_with_extra_row('summary_equivalent', 'summary_cash', SummaryCashModel), SummaryEquivalentRow);

    self.summary_transfer = new TableViewModel(key_to_options('summary_transfer'), SummaryTransferRow);

    self.summary_inventory = new TableViewModel(key_to_options('summary_inventory'), SummaryEquivalentRow);

    self.card_sales = new TableViewModel(key_to_options('card_sales'), CardSalesRow);

}

function SummaryCashModel(data) {
    var self = this;

    self.opening = function (all_accounts) {
//        var cash_account = all_accounts.filter(function(element, index, array){
//            if (element.name == 'Cash Account')
//                return element;
//        })[0];
//        return cash_account.current_balance;
        return 100;
    };

    self.inward = function (root) {
        var total = 0;
        $.each(root.cash_sales.rows(), function () {
            if (isAN(this.amount()))
                total += parseFloat(this.amount());
        });
        $.each(root.cash_receipt.rows(), function () {
            if (isAN(this.amount()))
                total += parseFloat(this.amount());
        });
        return rnum(total);
    };

    self.outward = function (root) {
        var total = 0;
        $.each(root.cash_purchase.rows(), function () {
            if (isAN(this.amount()))
                total += parseFloat(this.amount());
        });
        $.each(root.cash_payment.rows(), function () {
            if (isAN(this.amount()))
                total += parseFloat(this.amount());
        });
        return rnum(total);
    };

    self.closing = function (root) {
        return rnum(self.opening(root.accounts) + self.inward(root) - self.outward(root));
    };

    self.difference = function (root) {
        return rnum(self.actual() - self.closing(root));
    };

    self.actual = ko.observable();

    for (var k in data) {
        self[k] = ko.observable(data[k]);
    }
}

function LottoRow(row) {
    var self = this;

    self.particular = ko.observable();
    self.disp = ko.observable();
    self.reg = ko.observable();

    self.diff = function () {
        return rnum(parseFloat(self.disp()) - parseFloat(self.reg()));
    };

    for (var k in row)
        self[k] = ko.observable(row[k]);
}

function CashRow(row) {
    var self = this;

    self.account_id = ko.observable();
    self.amount = ko.observable();

    for (var k in row)
        self[k] = ko.observable(row[k]);

}

function CashSalesRow(row) {
    var self = this;

    self.account_id = ko.observable();
    self.tax_rate = ko.observable();
    self.amount = ko.observable();
    self.tax = function(){
        return rnum( parseFloat(self.amount()) * parseFloat(self.tax_rate()) / 100);
    }

    for (var k in row)
        self[k] = ko.observable(row[k]);

}

function CreditRow(row) {
    var self = this;

    self.account_cr_id = ko.observable();
    self.account_dr_id = ko.observable();
    self.amount = ko.observable();

    for (var k in row)
        self[k] = ko.observable(row[k]);

}

function CreditSalesRow(row) {
    var self = this;

    self.account_cr_id = ko.observable();
    self.account_dr_id = ko.observable();
    self.tax_rate = ko.observable();
    self.amount = ko.observable();
    self.tax = function(){
        return rnum( parseFloat(self.amount()) * parseFloat(self.tax_rate()) / 100);
    }

    for (var k in row)
        self[k] = ko.observable(row[k]);

}

function SummaryTaxRow(row) {
    var self = this;

    self.register = ko.observable();
    self.accounts = function(root){
        var total = 0;
        $.each(root.cash_sales.rows(), function () {
            if (isAN(this.tax()))
                total += parseFloat(this.tax());
        });
        $.each(root.credit_sales.rows(), function () {
            if (isAN(this.tax()))
                total += parseFloat(this.tax());
        });
        return rnum(total);
    }

    self.difference = function(root){
        return rnum(self.register() - self.accounts(root));
    }

    for (var k in row)
        self[k] = ko.observable(row[k]);

}

function SummaryEquivalentRow(row) {
    var self = this;

    self.account_id = ko.observable()

    self.opening = ko.observable();

    self.inward = ko.observable(0).extend({ numeric: 2 });
    self.outward = ko.observable(0).extend({ numeric: 2 });

    self.closing = ko.computed(function () {
        var closing = parseFloat(self.opening()) + parseFloat(self.inward()) - parseFloat(self.outward());
        return isNaN(closing) ? '' : closing;
    });

    self.actual = ko.observable();

    self.difference = function () {
        return rnum(self.actual() - self.closing());
    };

    for (var k in row)
        self[k] = ko.observable(row[k]);

}

function SummaryUtilityModel(data) {
    var self = this;

    self.amount = ko.observable();

    for (var k in data) {
        self[k] = ko.observable(data[k]);
    }

}

function SummaryTransferRow(row) {
    var self = this;

    self.transfer_type = ko.observable();
    self.cash = ko.observable();
    self.cheque = ko.observable();
    self.card = ko.observable();

    for (var k in row) {
        self[k] = ko.observable(row[k]);
    }

}

function CardSalesRow(row) {
    var self = this;

    self.amount = ko.observable();
    self.commission_out = ko.observable();

    self.net = function(){
        return rnum(empty_to_zero(self.amount()) - empty_to_zero(self.commission_out()));
    }

    for (var k in row)
        self[k] = ko.observable(row[k]);

}