function DayJournal(data) {
    var self = this;
    self.sales_tax = ko.observable();



    for (var k in data)
        self[k] = data[k];

    self.voucher_no = ko.observable();
    if (data['voucher_no']) {
        self.voucher_no(data['voucher_no']);
    }

    self.lotto_sales_dispenser_amount = ko.observable();
    if (data['lotto_sales_dispenser_amount']) {
        self.lotto_sales_dispenser_amount(data['lotto_sales_dispenser_amount']);
    }

    self.lotto_sales_register_amount = ko.observable();
    if (data['lotto_sales_register_amount']) {
        self.lotto_sales_register_amount(data['lotto_sales_register_amount']);
    }

    self.scratch_off_sales_register_amount = ko.observable();
    if (data['scratch_off_sales_register_amount']) {
        self.scratch_off_sales_register_amount(data['scratch_off_sales_register_amount']);
    }

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

    self.account_by_name = function (name) {
        var account = $.grep(self.accounts, function (i) {
            return i.name == name;
        });
        return account[0];
    }

    self.lotto_sales_dispenser_tax = ko.observable(parseFloat(self.account_by_name('Lotto Sales').tax_rate) * round2(parseFloat(self.lotto_sales_dispenser_amount())) / 100);

    self.lotto_sales_register_tax = function () {
        return rnum(parseFloat(self.account_by_name('Lotto Sales').tax_rate) * round2(parseFloat(self.lotto_sales_register_amount())) / 100);
    }

    self.scratch_off_sales_register_tax = function () {
        return rnum(parseFloat(self.account_by_name('Scratch Off Sales').tax_rate) * round2(parseFloat(self.scratch_off_sales_register_amount())) / 100);
    }

    self.actual_sales_amount = function () {
        return rnum(self.cash_sales.get_total('amount') + parseFloat(self.lotto_sales_dispenser_amount()) + self.lotto_detail.get_total('sales'));
    }

    self.actual_sales_tax = function () {
        return rnum(self.cash_sales.get_total('tax') + parseFloat(self.lotto_sales_dispenser_tax()) + self.scratch_off_sales_dispenser_tax());
    }

    self.register_sales_amount = function () {
        return rnum(self.cash_sales.get_total('amount') + parseFloat(self.lotto_sales_register_amount()) + parseFloat(self.scratch_off_sales_register_amount()));
    }

    self.register_sales_tax = function () {
        return rnum(self.cash_sales.get_total('tax') + self.lotto_sales_register_tax() + self.scratch_off_sales_register_tax());
    }

    self.diff_sales_amount = function () {
        return rnum(self.actual_sales_amount() - self.register_sales_amount());
    }

    self.diff_sales_tax = function () {
        return rnum(self.actual_sales_tax() - self.register_sales_tax());
    }

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

    self.accounts_except_category = function (categories, is_or) {
        var filtered_accounts = [];
        for (var i in self.accounts) {
            var account_categories = self.accounts[i].categories
            if (typeof categories === 'string') {
                if ($.inArray(categories, account_categories) == -1) {
                    filtered_accounts.push(self.accounts[i]);
                }
            } else if (typeof is_or != 'undefined') {
                if (!intersection(categories, account_categories).length) {
                    filtered_accounts.push(self.accounts[i]);
                }
            } else {
                if (!compare_arrays(categories, account_categories)) {
                    filtered_accounts.push(self.accounts[i]);
                }
            }
        }
        return filtered_accounts;
    };

    self.sales_sans_lotto = function () {
        var sales_accounts = self.accounts_by_category('Sales');
        var accounts = [];
        for (var i in sales_accounts) {
            if (sales_accounts[i].name != 'Lotto Sales' && sales_accounts[i].name != 'Scratch Off Sales')
                accounts.push(sales_accounts[i]);
        }
        return accounts;
    }


    self.lotto_sales_dispenser_amount.subscribe(function () {
        var tax_rate = parseFloat(self.account_by_name('Lotto Sales').tax_rate);
        self.lotto_sales_dispenser_tax(rnum(parseFloat(self.lotto_sales_dispenser_amount()) * tax_rate / 100));
    })

    self.scratch_off_sales_dispenser_tax = function () {
        return rnum(self.lotto_detail.get_total('sales') * self.account_by_name('Scratch Off Sales').tax_rate / 100);
    }

    self.inventory_accounts_by_category = function (category) {
        var filtered_accounts = [];
        for (var i in self.inventory_accounts) {
            if (self.inventory_accounts[i].category == category)
                filtered_accounts.push(self.inventory_accounts[i]);
        }
        return filtered_accounts;
    };

    self.account_by_id = function (id) {
        var account = $.grep(self.accounts, function (i) {
            return i.id == id;
        });
        return account[0];
    }

    self.save_lotto_sales_as_per_dispenser = function () {
        self.day_journal_date = self.date;
        $.ajax({
            type: "POST",
            url: '/day/save_lotto_sales_as_per_dispenser/',
            data: ko.toJSON(self),
            success: function (msg) {
                $('#lotto-sales-message').html('Saved!');
                $('#lotto-sales-message').addClass('success');
            },
            error: function (XMLHttpRequest, textStatus, errorThrown) {
                $('#lotto-sales-message').html('Saving Failed');
                $('#lotto-sales-message').addClass('error');
            }
        });
    }


    var validate = function (msg, rows, tr_wrapper_id) {
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
            model.state('error');
        }
        else if (saved_size < rows.length) {
            var message = saved_size.toString() + ' row' + ((saved_size == 1) ? '' : 's') + ' saved! ';
            message += (rows.length - saved_size).toString() + ' row' + ((rows.length - saved_size == 1) ? ' is' : 's are') + ' incomplete!';
            model.message(message);
            model.state('error');
        }
    }

    var key_to_options = function (key) {
        return {
            rows: data[key],
            save_to_url: '/day/save/' + key + '/',
            properties: {day_journal_date: self.date, voucher_no: self.voucher_no},
            onSaveSuccess: function (msg, rows) {
                validate(msg, rows, key.toDash());
            }
        };
    }

    var cash_sales_options = key_to_options('cash_sales');
    cash_sales_options.auto_add_first = false;
    self.cash_sales = new TableViewModel(cash_sales_options, CashSalesRow);
    if (self.cash_sales.hasNoRows()) {
        var accounts = self.sales_sans_lotto();
        for (var i in accounts) {
            self.cash_sales.rows.push(new CashSalesRow({'account_id': accounts[i].id}))
        }
    }


    self.summary_sales_tax = new TableViewModel(key_to_options('summary_sales_tax'), SummaryTaxRow);
    self.summary_sales_tax.rows()[0].register(self.sales_tax);

    self.summary_transfer = new TableViewModel(key_to_options('summary_transfer'), SummaryTransferRow);

    self.summary_inventory = new TableViewModel(key_to_options('summary_inventory'), InventoryRow);

    self.inventory_fuel = new TableViewModel(key_to_options('inventory_fuel'), InventoryRow);

    self.card_sales = new TableViewModel(key_to_options('card_sales'), CardSalesRow);

    var cash_equivalent_sales_options = key_to_options('cash_equivalent_sales');
    cash_equivalent_sales_options.auto_add_first = false;
    self.cash_equivalent_sales = new TableViewModel(cash_equivalent_sales_options, CashEquivalentSalesRow);
    if (self.cash_equivalent_sales.hasNoRows()) {
        var accounts = self.accounts_by_category('Cash Equivalent Account')
        for (var i in accounts) {
            self.cash_equivalent_sales.rows.push(new CashEquivalentSalesRow({'account': accounts[i].id}))
        }
    }

    self.summary_cash = new TableViewModel(key_to_options('summary_cash'), SummaryCashRow);
    self.summary_cash.rows()[0].actual(self.cash_actual);

    var lotto_detail_options = key_to_options('lotto_detail');
    lotto_detail_options.auto_add_first = false;
    self.lotto_detail = new TableViewModel(lotto_detail_options, LottoDetailRow);
    if (self.lotto_detail.hasNoRows()) {
        $.ajax({
            url: '/day/last_lotto_detail/' + self.date + '.json',
            dataType: 'json',
            async: false,
            success: function (data) {
                self.last_lotto_detail = data;
            }
        });
        if (self.last_lotto_detail) {
            for (var i in self.last_lotto_detail) {
                var detail = self.last_lotto_detail[i];
                self.lotto_detail.rows.push(new LottoDetailRow({'rate': detail.rate, 'pack_count': detail.pack_count, 'day_open': detail.day_close}))
            }
        }
    }

    self.vendor_payout = new TableViewModel(key_to_options('vendor_payout'), VendorPayoutVM);

    self.other_payout = new TableViewModel(key_to_options('other_payout'), OtherPayoutVM);

    self.summary_lotto = new SummaryLotto(self);

}

function LottoDetailRow(row) {

    var self = this;

    self.rate = ko.observable();
    self.pack_count = ko.observable();
    self.day_open = ko.observable();
    self.day_close = ko.observable();
    self.addition = ko.observable(0);
    self.sales = function () {
        var day_close = self.day_close();
        if (day_close == 0) {
            day_close = self.pack_count();
        }
        return round2(((self.pack_count() * self.addition()) + (day_close - self.day_open())) * self.rate());
    }

    for (var k in row) {
        if (row[k] != null)
            self[k] = ko.observable(row[k]);
    }
}

function CashSalesRow(row) {
    var self = this;

    self.account_id = ko.observable();
    self.tax_rate = ko.observable();
    self.amount = ko.observable();
    self.tax = function () {
        return round2(parseFloat(self.amount()) * parseFloat(self.tax_rate()) / 100);
    }

    for (var k in row) {
        if (row[k] != null)
            self[k] = ko.observable(row[k]);
    }

}

function SummaryTaxRow(row) {
    var self = this;

    self.register = ko.observable();
    self.accounts = function (root) {
        var total = 0;
        $.each(root.cash_sales.rows(), function () {
            if (isAN(this.tax()))
                total += parseFloat(this.tax());
        });
//        $.each(root.credit_sales.rows(), function () {
//            if (isAN(this.tax()))
//                total += parseFloat(this.tax());
//        });
        return rnum(total);
    }

    self.difference = function (root) {
        return rnum(self.register() - self.accounts(root));
    }

    for (var k in row) {
        if (row[k] != null)
            self[k] = ko.observable(row[k]);
    }

}

function InventoryRow(row) {
    var self = this;

    self.account_id = ko.observable()

    self.opening = ko.observable();

    self.purchase = ko.observable();
    self.sales = ko.observable();

    self.closing = ko.computed(function () {
        return rnum(parseFloat(self.opening()) + parseFloat(self.purchase()) - parseFloat(self.sales()));
    });

    self.actual = ko.observable();

    self.difference = function () {
        return rnum(self.actual() - self.closing());
    };

    for (var k in row) {
        if (row[k] != null)
            self[k] = ko.observable(row[k]);
    }

}

function SummaryTransferRow(row) {
    var self = this;

    self.transfer_type = ko.observable();
    self.cash = ko.observable();
    self.cheque = ko.observable();
    self.card = ko.observable();

    for (var k in row) {
        if (row[k] != null)
            self[k] = ko.observable(row[k]);
    }

}

function CardSalesRow(row) {
    var self = this;

    self.amount = ko.observable();
    self.commission_out = ko.observable();

    self.net = function () {
        return rnum(empty_to_zero(self.amount()) - empty_to_zero(self.commission_out()));
    }

    for (var k in row) {
        if (row[k] != null)
            self[k] = ko.observable(row[k]);
    }

}

function CashEquivalentSalesRow(row) {
    var self = this;

    self.account = ko.observable();
    self.amount = ko.observable();

    for (var k in row) {
        if (row[k] != null)
            self[k] = ko.observable(row[k]);
    }

}

function SummaryCashRow(row) {
    var self = this;

    self.opening = function (root) {
        var cash_account = root.accounts.filter(function (element, index, array) {
            if (element.name == 'Cash Account')
                return element;
        })[0];
        return round2(cash_account.opening);
    };

    self.inward = function (root) {
        var total = 0;
        $.each(root.cash_sales.rows(), function () {
            if (isAN(this.amount()))
                total += parseFloat(this.amount());
        });
//        $.each(root.cash_receipt.rows(), function () {
//            if (isAN(this.amount()))
//                total += parseFloat(this.amount());
//        });
        $.each(root.summary_transfer.rows(), function () {
            if (isAN(this.cash()))
                total += parseFloat(this.cash());
        });
//        if (isAN(root.summary_bank.rows()[0].withdrawal()))
//            total += parseFloat(root.summary_bank.rows()[0].withdrawal());
        return round2(total);
    };

    self.outward = function (root) {
        var total = 0;
//        $.each(root.cash_purchase.rows(), function () {
//            if (isAN(this.amount()))
//                total += parseFloat(this.amount());
//        });
//        $.each(root.cash_payment.rows(), function () {
//            if (isAN(this.amount()))
//                total += parseFloat(this.amount());
//        });
        $.each(root.card_sales.rows(), function () {
            if (isAN(this.amount()))
                total += parseFloat(this.amount());
        });
        $.each(root.cash_equivalent_sales.rows(), function () {
            if (isAN(this.amount()))
                total += parseFloat(this.amount());
        });
//        $.each(root.cheque_purchase.rows(), function () {
//            if (isAN(this.net()))
//                total += parseFloat(this.net());
//        });
//        if (isAN(root.summary_bank.rows()[0].deposit()))
//            total += parseFloat(root.summary_bank.rows()[0].deposit());
        return round2(total);
    };

    self.closing = function (root) {
        return round2(self.opening(root) + self.inward(root) - self.outward(root));
    };

    self.actual = ko.observable();

    self.difference = function (root) {
        return round2(self.actual() - self.closing(root));
    };


    for (var k in row) {
        if (row[k] != null)
            self[k] = ko.observable(row[k]);
    }
}

function SummaryLotto(root) {
    var self = this;
    self.disp = function () {
        var total = 0;
        $.each(root.lotto_detail.rows(), function () {
            if (isAN(this.sales()))
                total += this.sales();
        });
        return total;
    }
    self.reg = function () {
        var total = 0;
        $.each(root.cash_sales.rows(), function () {
            if (typeof this.account_id() != 'undefined') {
                if (root.account_by_id(this.account_id()).name == 'Lotto Sales') {
                    total += this.amount();
                }
            }
        });
        return total;
    }
    self.diff = function () {
        return round2(self.disp() - self.reg());
    };
}

function VendorPayoutVM(row) {
    var self = this;

    self.vendor = ko.observable();
    self.amount = ko.observable();
    self.purchase_ledger = ko.observable();
    self.remarks = ko.observable();
    self.paid = ko.observable();
    self.type = ko.observable();

    self.types = [
        { name: 'New Purchase', id: 'new'},
        { name: 'Old Bill Payment', id: 'old'}
    ];

    for (var k in row) {
        if (row[k] != null)
            self[k] = ko.observable(row[k]);
    }
}

function OtherPayoutVM(row) {
    var self = this;

    self.paid_to = ko.observable();
    self.amount = ko.observable();
    self.remarks = ko.observable();
    self.paid = ko.observable();

    for (var k in row) {
        if (row[k] != null)
            self[k] = ko.observable(row[k]);
    }
}