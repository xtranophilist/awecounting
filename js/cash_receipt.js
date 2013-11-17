$(document).ready(function () {
    $(document).ready(function () {
        $('.date-picker').datepicker();
    });
    vm = new CashReceiptVM(ko_data);
    ko.applyBindings(vm);
});


function CashReceiptVM(data) {
    var self = this;

    $.ajax({
        url: '/ledger/party/customers.json',
        dataType: 'json',
        async: false,
        success: function (data) {
            self.parties = data;
        }
    });

    self.id = ko.observable('');
    self.message = ko.observable();
    self.state = ko.observable('standby');
    self.party = ko.observable();
    self.receipt_on = ko.observable();
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
        self.current_balance(selected_obj.customer_balance);
//        if (self.table_vm()){
//            self.table_vm().rows(null);
//        }
    }

    self.load_related_invoices = function () {
        if (self.party()) {
            $.ajax({
                url: '/voucher/invoice/party/' + self.party() + '.json',
                dataType: 'json',
                async: false,
                success: function (data) {
                    if (data.length) {
                        self.invoices = data;
                        for (k in self.rows()) {
                            var row = self.rows()[k];
                            $.each(self.invoices, function (i, o) {
                                if (o.id == row.id) {
                                    o.payment = row.receipt;
                                    o.discount = row.discount;
                                }
                            });
                        }
                        var options = {
                            rows: self.invoices
                        };
                        self.table_vm(new TableViewModel(options, CashReceiptRowVM));
                        bs_alert.success('Invoices loaded!');
                        self.state('success');
                    }
                    else {
                        bs_alert.warning('No pending invoices found for the customer!');
                        self.state('error');
                    }
                }
            });
        }

    }

    if (self.rows().length) {
        self.load_related_invoices();
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
            self.state('error');
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
                url: '/voucher/cash-receipt/save/',
                data: data,
                success: function (msg) {
                    if (typeof (msg.error_message) != 'undefined') {
                        self.message(msg.error_message);
                        self.state('error');
                    }
                    else {
                        self.message('Saved!');
                        self.state('success');
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
                url: '/voucher/cash-receipt/approve/',
                data: ko.toJSON(self),
                success: function (msg) {
                    if (typeof (msg.error_message) != 'undefined') {
                        self.message(msg.error_message);
                        self.state('error');
                    }
                    else {
                        self.message('Approved!');
                        self.state('success');
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


function CashReceiptRowVM(row) {
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
