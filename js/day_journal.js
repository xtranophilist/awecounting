$(document).ready(function () {
    vm = new DayJournal(ko_data);
    ko.applyBindings(vm);
    $('.change-on-ready').trigger('change');


    if (window.location.hash != "") {
        $('a[href="' + window.location.hash + '"]').click();
    }
    $(document).on("click", ".delete-attachment", function (e) {
        e.preventDefault();
        var $this = $(this);
        if (confirm("Are you sure you want to delete this attachment?")) {
            var uri = build_attachment_url($this.data("type"), $this.data('id'));
            $.post(uri.url, uri.params)
                .done(function (res) {
                    if (res.success) {
                        $this.parent('.span3').fadeOut(300, function () {
                            $(this).remove();
                        });
                    } else {
                        alert("There has been error while processing your request. Please try again!");
                    }
                });
        } else {
            return false;
        }
    });

    function build_attachment_url(type, id) {
        return {url: "/day/delete_attachment/", params: {type: type, id: id}};
    }

    var add_file_view = $('.attach_file_field').first();

    $('.add_file').click(function () {
        var _parent = $(this).parent('p');
        var clone = add_file_view.clone();
        clone.append('<button type="button" class="btn btn-danger pull-right remove-file-attach">X</button>')
        clone.find('input').val("");
        _parent.before(clone);
    });

    $(document).on('click', '.remove-file-attach', function () {
        $(this).parent('.attach_file_field').slideUp(400, function () {
            $(this).remove()
        });
    });

    $('.attachment-form').submit(function (e) {
        e.preventDefault();
        if (window.FormData) {
            var file_ips = $(this).find('input[type="file"]');
            var text_ips = $(this).find('.captions');
            var formdata = new FormData();
            $.each(text_ips, function () {
                formdata.append("captions", this.value);
            });
            $.each(file_ips, function () {
                formdata.append("attachments", this.files[0]);
            });
            var $this = $(this);
            var type = $this.data("type");
            formdata.append("type", type);
            formdata.append("day", $('#attachment_tabbable').data("journal-day"));
            $.ajax({
                url: "/day/save_attachments/",
                type: "POST",
                data: formdata,
                processData: false,
                contentType: false,
                success: function (res) {
                    var str = "";
                    $.each(res, function () {
                        str += '<div class="span3"> <a target="_blank" href="' + this.link + '">' + this.caption + '</a><button class="close delete-attachment" data-type="' + type + '" data-id="' + this.id + '"><span class="icon-trash"></span></button></div>';
                    });
                    $this.find('.row-fluid').append(str);
                    $this.find('.attach_file_field').find("input").val("").end().not(':first').remove();
                },
                error: function () {
                    alert("There has been error while processing your request. Please try again!");
                }
            });

        } else {
            alert("Your browser is too old. Please upgrade to modern browsers like Chrome or Firefox.")
        }
    });

});

function DayJournal(data) {
    var self = this;
    self.sales_tax = ko.observable();
    self.state = ko.observable();

    for (var k in data)
        self[k] = data[k];

    self.voucher_no = ko.observable();
    if (data['voucher_no']) {
        self.voucher_no(data['voucher_no']);
    }

    self.status = ko.observable();
    if (data['status']) {
        self.status(data['status']);
    }

    self.lotto_sales_dispenser_amount = ko.observable();
    if (isAN(data['lotto_sales_dispenser_amount'])) {
        self.lotto_sales_dispenser_amount(parseFloat(data['lotto_sales_dispenser_amount']));
    }

    self.lotto_sales_register_amount = ko.observable();
    if (data['lotto_sales_register_amount']) {
        self.lotto_sales_register_amount(parseFloat(data['lotto_sales_register_amount']));
    }

    self.scratch_off_sales_register_amount = ko.observable();
    if (data['scratch_off_sales_register_amount']) {
        self.scratch_off_sales_register_amount(parseFloat(data['scratch_off_sales_register_amount']));
    }

    self.register_sales_amount = ko.observable();
    if (data['register_sales_amount']) {
        self.register_sales_amount(parseFloat(data['register_sales_amount']));
    }

    self.register_sales_tax = ko.observable();
    if (data['register_sales_tax']) {
        self.register_sales_tax(parseFloat(data['register_sales_tax']));
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

    self.lotto_sales_dispenser_tax = ko.observable(parseFloat(self.account_by_name('Lotto Sales').tax_rate) * empty_to_zero(self.lotto_sales_dispenser_amount()) / 100);

    self.lotto_sales_register_tax = function () {
        return rnum(parseFloat(self.account_by_name('Lotto Sales').tax_rate) * round2(parseFloat(self.lotto_sales_register_amount())) / 100);
    }

    self.scratch_off_sales_register_tax = function () {
        return rnum(parseFloat(self.account_by_name('Scratch Off Sales').tax_rate) * round2(parseFloat(self.scratch_off_sales_register_amount())) / 100);
    }

    self.scratch_off_total = function () {
        if (isAN(self.lotto_detail.scratch_off_sales_manual()))
            return parseFloat(self.lotto_detail.scratch_off_sales_manual());
        else
            return self.lotto_detail.get_total('sales');
    }

    self.actual_sales_amount = function () {
        var total_scratch = self.scratch_off_total();
        if (total_scratch == 0 && self.scratch_off_sales_register_amount()) {
            total_scratch = empty_to_zero(self.scratch_off_sales_register_amount());
        }
        return rnum(self.cash_sales.get_total('amount') + empty_to_zero(self.lotto_sales_dispenser_amount()) + total_scratch + self.summary_transfer.total());
    }

    self.actual_sales_tax = function () {
        var scratch_off_tax = self.scratch_off_sales_dispenser_tax();
        if (scratch_off_tax == 0) {
            scratch_off_tax = self.scratch_off_sales_register_tax();
        }
        return rnum(self.cash_sales.get_total('tax') + parseFloat(self.lotto_sales_dispenser_tax()) + scratch_off_tax);
    }

    self.sales_summary_cash = function () {
        return self.actual_sales_amount() - empty_to_zero(self.card_sales.rows()[0].amount()) - self.cash_equivalent_sales.get_total('amount');
    }

//    self.register_sales_amount = function () {
//        return rnum(self.cash_sales.get_total('amount') + parseFloat(self.lotto_sales_register_amount()) + parseFloat(self.scratch_off_sales_register_amount()));
//    }
//
//    self.register_sales_tax = function () {
//        return rnum(self.cash_sales.get_total('tax') + self.lotto_sales_register_tax() + self.scratch_off_sales_register_tax());
//    }

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
        return rnum(self.scratch_off_total() * self.account_by_name('Scratch Off Sales').tax_rate / 100);
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

    self.inventory_account_by_id = function (id) {
        var account = $.grep(self.inventory_accounts, function (i) {
            return i.id == id;
        });
        return account[0];
    }

    self.get_unit = function (id) {
        var account = $.grep(self.inventory_accounts, function (i) {
            return i.id == id;
        });
        return account[0].unit || '';
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
                self.status('Unapproved');
            },
            error: function (XMLHttpRequest, textStatus, errorThrown) {
                $('#lotto-sales-message').html('Saving Failed');
                $('#lotto-sales-message').addClass('error');
            }
        });
    }

    self.save_sales_register = function () {
        self.day_journal_date = self.date;
        $.ajax({
            type: "POST",
            url: '/day/save_sales_register/',
            data: ko.toJSON(self),
            success: function (msg) {
                $('#sales-register-message').html('Saved!');
                $('#sales-register-message').addClass('success');
                self.status('Unapproved');
            },
            error: function (XMLHttpRequest, textStatus, errorThrown) {
                $('#sales-register-message').html('Saving Failed');
                $('#sales-register-message').addClass('error');
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
        if (typeof (msg.error_message) != 'undefined') {
            model.message(msg.error_message);
            model.state('error');
        }
        else {
            var saved_size = Object.size(msg['saved']);
            if (saved_size == rows.length) {
                model.message('Saved!');
                self.status('Unapproved');
            }
            else if (saved_size == 0) {
                model.message('No rows saved!');
                model.state('error');
            }
            else if (saved_size < rows.length) {
                var message = saved_size.toString() + ' row' + ((saved_size == 1) ? '' : 's') + ' saved! ';
                message += (rows.length - saved_size).toString() + ' row' + ((rows.length - saved_size == 1) ? ' is' : 's are') + ' incomplete!';
                model.message(message);
                model.state('error');
                self.status('Unapproved');
            }
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

    var summary_transfer_options = key_to_options('summary_transfer');
    summary_transfer_options.auto_add_first = false;
    self.summary_transfer = new TableViewModel(summary_transfer_options, SummaryTransferRow);
    if (self.summary_transfer.hasNoRows()) {
        var accounts = self.accounts_by_category('Transfer and Remittance');
        for (var i in accounts) {
            self.summary_transfer.rows.push(new SummaryTransferRow({'transfer_type': accounts[i].id}))
        }
    }

    self.summary_transfer.total = function () {
        return self.summary_transfer.get_total('cash') + self.summary_transfer.get_total('card') + self.summary_transfer.get_total('cheque');
    }

    self.summary_sales_tax = new TableViewModel(key_to_options('summary_sales_tax'), SummaryTaxRow);
    self.summary_sales_tax.rows()[0].register(self.sales_tax);

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
        self.last_lotto_detail = self.last_lotto_detail.sort(function (a, b) {
            return a.sn - b.sn;
        })
        if (self.last_lotto_detail) {
            if (Object.size(self.last_lotto_detail)) {
                for (var i in self.last_lotto_detail) {
                    var detail = self.last_lotto_detail[i];
                    self.lotto_detail.rows.push(new LottoDetailRow({'rate': detail.rate, 'pack_count': detail.pack_count, 'day_open': detail.day_close, 'day_close': detail.day_close}))
                }
            }
            else {
                self.lotto_detail.addRow(new LottoDetailRow());
            }
        }
    }
    self.lotto_detail.scratch_off_sales_manual = ko.observable();
    if (isAN(data['scratch_off_sales_manual'])) {
        self.lotto_detail.scratch_off_sales_manual(parseFloat(data['scratch_off_sales_manual']));
    }

    self.vendor_payout = new TableViewModel(key_to_options('vendor_payout'), VendorPayoutVM);

    self.other_payout = new TableViewModel(key_to_options('other_payout'), OtherPayoutVM);

    self.summary_lotto = new SummaryLotto(self);

    self.approve = function () {
        $.ajax({
            type: "POST",
            url: '/day/approve/',
            data: ko.toJSON(self),
            success: function (msg) {
                if (typeof (msg.error_message) != 'undefined') {
                    bs_alert.error(msg.error_message);
                }
                else {
                    bs_alert.success('Approved!')
                    self.status('Approved');
                    self.state('success');
                }
//                $('#lotto-sales-message').html('Saved!');
//                $('#lotto-sales-message').addClass('success');
            },
            error: function (XMLHttpRequest, textStatus, errorThrown) {
                console.log(XMLHttpRequest);
//                $('#lotto-sales-message').html('Saving Failed');
//                $('#lotto-sales-message').addClass('error');
            }
        });
    }

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
        return rnum(((self.pack_count() * self.addition()) + (day_close - self.day_open())) * self.rate());
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
//    self.tax = ko.observable(rnum(parseFloat(self.amount()) * parseFloat(vm.account_by_id(self.account_id()).tax_rate) / 100));
//    self.tax = ko.observable();

//    self.amount.subscribe(function () {
//        self.tax(rnum(parseFloat(self.amount()) * parseFloat(vm.account_by_id(self.account_id()).tax_rate) / 100));
//    });

    self.tax = function () {
        if (self.account_id()) {
            return rnum(parseFloat(self.amount()) * parseFloat(vm.account_by_id(self.account_id()).tax_rate) / 100);
        }
        return '';
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

//    self.opening = function (root) {
//        return root.inventory_account_by_id(self.account_id()).opening;
//    }

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
        total += root.actual_sales_amount();

//        $.each(root.summary_transfer.rows(), function () {
//            if (isAN(this.cash()))
//                total += parseFloat(this.cash());
//        });
        if (root.card_sales.rows()[0].amount()) {
            total -= parseFloat(root.card_sales.rows()[0].amount());
        }
        total -= root.cash_equivalent_sales.get_total('amount');
        return rnum(total);
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
//        $.each(root.card_sales.rows(), function () {
//            if (isAN(this.amount()))
//                total += parseFloat(this.amount());
//        });
//        $.each(root.cash_equivalent_sales.rows(), function () {
//            if (isAN(this.amount()))
//                total += parseFloat(this.amount());
//        });
//        $.each(root.cheque_purchase.rows(), function () {
//            if (isAN(this.net()))
//                total += parseFloat(this.net());
//        });
//        if (isAN(root.summary_bank.rows()[0].deposit()))
//            total += parseFloat(root.summary_bank.rows()[0].deposit());
        $.each(root.vendor_payout.rows(), function () {
            if (isAN(this.amount()) && this.paid()) {
                var account = root.account_by_id(this.paid());
                for (var i in account.categories) {
                    var category = account.categories[i];
                    if (category == 'Cash Account') {
                        total += parseFloat(this.amount());
                    }
                }
            }
        });

        $.each(root.other_payout.rows(), function () {
            if (isAN(this.amount()) && this.paid()) {
                var account = root.account_by_id(this.paid());
                for (var i in account.categories) {
                    var category = account.categories[i];
                    if (category == 'Cash Account') {
                        total += parseFloat(this.amount());
                    }
                }
            }
        });

        return rnum(total);
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
        { name: 'Old Bill Payment', id: 'old'},
        { name: 'Account Settlement', id: 'settlement'},
        { name: 'Advance Payment', id: 'payment'}
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