$(document).ready(function () {
    $(document).ready(function () {
        $('.date-picker').datepicker();
    });
    vm = new FixedAssetVM(ko_data);
    ko.applyBindings(vm);
});


function FixedAssetVM(data) {
    var self = this;

    $.ajax({
        url: '/ledger/cash-and-vendors.json',
        dataType: 'json',
        async: false,
        success: function (data) {
            self.from_accounts = data;
        }
    });

    self.id = ko.observable('hey');
    self.message = ko.observable();
    self.status = ko.observable('standby');
    self.party = ko.observable();
    self.payment_on = ko.observable();
    self.party_address = ko.observable();
    self.reference = ko.observable();
    self.current_balance = ko.observable();
    self.amount = ko.observable();
    self.table_vm = ko.observable({'rows': function () {
    }, 'get_total': function () {
    }});

    for (var k in data) {
        self[k] = ko.observable(data[k]);
    }

    self.party_changed = function (vm) {
        var selected_obj = $.grep(self.parties, function (i) {
            return i.id == vm.party();
        })[0];
        self.party_address(selected_obj.address);
        self.current_balance(selected_obj.supplier_balance);
    }

    self.load_purchase_vouchers = function () {
        if (self.party()) {
            $.ajax({
                url: '/voucher/purchase/party/' + self.party() + '.json',
                dataType: 'json',
                async: false,
                success: function (data) {
                    if (data.length) {
                        self.invoices = data;
                        for (k in self.rows()) {
                            var row = self.rows()[k];
                            $.each(self.invoices, function (i, o) {
                                if (o.id == row.id) {
                                    o.payment = row.payment;
                                    o.discount = row.discount;
                                }
                            });
                        }
                        var options = {
                            rows: self.invoices
                        };
                        self.table_vm(new TableViewModel(options, CashPaymentRowVM));
                        self.message('Purchase Vouchers loaded!');
                        self.status('success');
                    }
                    else {
                        self.message('No pending purchase vouchers found for the supplier!');
                        self.status('error');
                    }
                }
            });
        }

    }

    if (self.rows().length) {
        self.load_purchase_vouchers();
    }

    self.total_payment = ko.computed(function () {
        return self.table_vm().get_total('payment');
    }, self);

    self.total_discount = ko.computed(function () {
        return self.table_vm().get_total('discount');
    }, self);

    self.validate = function () {
        if (!self.party()) {
            self.message('"Party" field is required!')
            self.status('error');
            return false;
        }
        return true;
    }

    self.save = function (item, event) {
        if (!self.validate())
            return false;
        if (get_form(event).checkValidity()) {
            if ($(get_target(event)).data('continue')) {
                self.continue = true;
            }
            var data = ko.toJSON(self);
            $.ajax({
                type: "POST",
                url: '/voucher/cash-payment/save/',
                data: data,
                success: function (msg) {
                    if (typeof (msg.error_message) != 'undefined') {
                        self.message(msg.error_message);
                        self.status('error');
                    }
                    else {
                        self.message('Saved!');
                        self.status('success');
                        if (msg.id)
                            self.id(msg.id);
                        if (msg.redirect_to) {
                            window.location = msg.redirect_to;
                        }
                    }
                }
            });
        }
        else
            return true;
    }

    self.approve = function (item, event) {
        if (!self.validate())
            return false;
        if (get_form(event).checkValidity()) {
            $.ajax({
                type: "POST",
                url: '/voucher/cash-payment/approve/',
                data: ko.toJSON(self),
                success: function (msg) {
                    if (typeof (msg.error_message) != 'undefined') {
                        self.message(msg.error_message);
                        self.status('error');
                    }
                    else {
                        self.message('Approved!');
                        self.status('success');
                        if (msg.id)
                            self.id(msg.id);
                    }
                }
            });
        }
        else
            return true;
    }
}


function FixedAssetRowVM(row) {
    var self = this;

    self.payment = ko.observable();
    self.discount = ko.observable();

    for (var k in row) {
        self[k] = ko.observable(row[k]);
    }

    self.overdue_days = function () {
        if (self.due_date()) {
            var diff = days_between(new Date(self.due_date()), new Date());
            if (diff >= 0)
                return diff;
        }
        return '';
    }

}
