$(document).ready(function () {
    $('.date-picker').datepicker().data('datepicker');
    ko.applyBindings(new JournalVoucher(ko_data));
});


function JournalVoucher(data) {
    var self = this;

    self.date = '';

    for (var k in data)
        self[k] = data[k];

    $.ajax({
        url: '/ledger/accounts/json/',
        dataType: 'json',
        async: false,
        success: function (data) {
            self.accounts = data;
        }
    });

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
            model.status('error');
        }
        else if (saved_size < rows.length) {
            var message = saved_size.toString() + ' row' + ((saved_size == 1) ? '' : 's') + ' saved! ';
            message += (rows.length - saved_size).toString() + ' row' + ((rows.length - saved_size == 1) ? ' is' : 's are') + ' incomplete!';
            model.message(message);
            model.status('error');
        }
    }

    var key_to_options = function (key) {
        return {
            rows: data['rows'],
            save_to_url: '/voucher/journal/save/',
            properties: {id: self.id},
            onSaveSuccess: function (msg, rows) {
                validate(msg, rows, key.toDash());
            }
        };
    }

    self.journal_voucher = new TableViewModel(key_to_options('journal_voucher'), JournalVoucherRow);

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

    self.journal_voucher.cr_total = function () {
        var total = 0.00;
        $.each(self.journal_voucher.rows(), function () {
            if (isAN(this.cr_amount())) {
                total += parseFloat(this.cr_amount());
            }
        });
        return total.toFixed(2);
    }

    self.journal_voucher.dr_total = function () {
        var total = 0.00;
        $.each(self.journal_voucher.rows(), function () {
            if (isAN(this.dr_amount()))
                total += parseFloat(this.dr_amount());
        });
        return total.toFixed(2);
    }

    self.add_row = function (element, viewModel) {
        $(element).blur();
        var type;
        var dr_amount;
        var cr_amount;
        var diff = self.journal_voucher.dr_total() - self.journal_voucher.cr_total()
        if (diff > 0) {
            type = 'Cr';
            dr_amount = 0;
            cr_amount = diff;
        } else {
            type = 'Dr';
            cr_amount = 0;
            dr_amount = (-1) * diff;
        }

        if ($(element).closest("tr").is(":nth-last-child(2)") && self.journal_voucher.dr_total() != self.journal_voucher.cr_total())
            self.journal_voucher.rows.push(new JournalVoucherRow({type: type, cr_amount: cr_amount, dr_amount: dr_amount}));
    }

    self.journal_voucher.cr_equals_dr = function () {
        return self.journal_voucher.dr_total() === self.journal_voucher.cr_total();
    }

    self.journal_voucher.total_row_class = function () {
        if (self.journal_voucher.dr_total() === self.journal_voucher.cr_total())
            return 'valid-row';
        return 'invalid-row';
    }

    self.journal_voucher.save = function () {

        self.journal_voucher.status('waiting');

        var valid = true;
        var message = '';
        var rows = self.journal_voucher.rows();
        var selection = $("#journal-voucher > tr");

        if (!self.journal_voucher.cr_equals_dr()) {
            message += 'Total Dr and Cr amounts don\'t tally!';
            valid = false;
        }

        if (!self.date) {
            message += 'Date field is required!';
            valid = false;
        }

        self.journal_voucher.message(message);
        if (!valid) {
            self.journal_voucher.status('error');
            return false;
        }
        $.ajax({
            type: "POST",
            url: '/voucher/journal/save/',
            data: ko.toJSON(self),
            success: function (msg) {
                self.journal_voucher.message('Saved!');
                self.deleted_rows = [];
                self.journal_voucher.status('success');

            },
            error: function (XMLHttpRequest, textStatus, errorThrown) {
                self.journal_voucher.message('Saving Failed!');
                self.journal_voucher.status('error');
            }
        });


    }
}

function JournalVoucherRow(row) {
    var self = this;

    self.type = ko.observable('Dr');
    self.account = ko.observable();
    self.description = ko.observable();
    self.dr_amount = ko.observable();
    self.cr_amount = ko.observable();

    self.is_dr = function () {
        if (self.type() == 'Dr')
            return true;
        return false;
    }

    self.is_cr = function () {
        if (self.type() == 'Cr')
            return true;
        return false;
    }

    self.type_changed = function (e) {
//        console.log(self.type());
    }

    for (var k in row) {
        if (row[k] != null)
            self[k] = ko.observable(row[k]);
    }

}