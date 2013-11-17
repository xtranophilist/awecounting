$(document).ready(function () {
    $('#inv-date').datepicker().data('datepicker');
    $('#due-date').datepicker({relative_to: '#inv-date'});
    vm = new InvoiceViewModel(ko_data);
    ko.applyBindings(vm);
});

function TaxOptions(name, id) {
    this.name = name;
    this.id = id;
}


function InvoiceViewModel(data) {
    var self = this;

    self.tax_options = ko.observableArray([
        new TaxOptions('Tax Inclusive', 'inclusive'),
        new TaxOptions('Tax Exclusive', 'exclusive'),
        new TaxOptions('No Tax', 'no')
    ]);

    $.ajax({
        url: '/inventory/items/json/',
        dataType: 'json',
        async: false,
        success: function (data) {
            self.items = data;
        }
    });

    $.ajax({
        url: '/ledger/party/customers.json',
        dataType: 'json',
        async: false,
        success: function (data) {
            self.customers = data;
        }
    });

    $.ajax({
        url: '/tax/schemes/json/',
        dataType: 'json',
        async: false,
        success: function (data) {
            self.tax_schemes = data;
        }
    });

    self.tax_scheme_by_id = function (id) {
        var scheme = $.grep(self.tax_schemes, function (i) {
            return i.id == id;
        });
        return scheme[0];
    }

    self.party = ko.observable();
    self.description = ko.observable();

    for (var k in data)
        self[k] = data[k];

    self.tax = ko.observable(data['tax']);

    self.message = ko.observable('');
    self.state = ko.observable('standby');

    self.status = ko.observable(data['status']);

    self.id = ko.observable(data['id']);

    self.party_address = ko.observable('');

    var invoice_options = {
        rows: data.particulars
    };

    self.particulars = new TableViewModel(invoice_options, ParticularViewModel);

//    self.addParticular = function() {
//        var new_item_index = self.particulars().length+1;
//        self.particulars.push(new ParticularViewModel({ sn: new_item_index }));
//    };
//
//    self.removeParticular = function(particular) {
//        for (var i = particular.sn(); i < self.particulars().length; i++) {
//            self.particulars()[i].sn(self.particulars()[i].sn()-1);
//        };
//        self.particulars.remove(particular);
//    };

    self.validate = function () {
        self.message('');
        bs_alert.clear();
        if (!self.party) {
            bs_alert.error('"To" field is required!');
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
            $.ajax({
                type: "POST",
                url: '/voucher/invoice/save/',
                data: ko.toJSON(self),
                success: function (msg) {
                    if (typeof (msg.error_message) != 'undefined') {
                        bs_alert.error(msg.error_message);
                    }
                    else {
                        bs_alert.success('Saved!');
                        if (msg.id) {
                            self.id(msg.id);
                            self.status('Unapproved');
                        }
                        self.state('success');
                        if (msg.redirect_to) {
                            window.location = msg.redirect_to;
                            return;
                        }
                        $("#particulars-body > tr").each(function (i) {
                            $($("#particulars-body > tr")[i]).addClass('invalid-row');
                        });
                        for (var i in msg.rows) {
                            self.particulars.rows()[i].id = msg.rows[i];
                            $($("#particulars-body > tr")[i]).removeClass('invalid-row');
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
                url: '/voucher/invoice/approve/',
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
                }
            });
        }
        else
            return true;
    }

    self.cancel = function (item, event) {
        $.ajax({
            type: "POST",
            url: '/voucher/invoice/cancel/',
            data: ko.toJSON(self),
            success: function (msg) {
                if (typeof (msg.error_message) != 'undefined') {
                    bs_alert.error(msg.error_message);
                }
                else {
                    bs_alert.success('Cancelled!');
                    self.status('Cancelled');
                    self.state('success');
                    if (msg.id)
                        self.id(msg.id);
                }
            }
        });
    }

    self.save_and_continue = function (item, event) {
        if (!self.validate())
            return false;
        if (get_form(event).checkValidity()) {
            $.ajax({
                type: "POST",
                url: '/voucher/invoice/save_and_continue/',
                data: ko.toJSON(self),
                success: function (msg) {
                    if (typeof (msg.error_message) != 'undefined') {
                        bs_alert.error(msg.error_message);
                    }
                    else {
                        bs_alert.success('Saved!');
                        if (msg.id)
                            self.id(msg.id);
                        $("#particulars-body > tr").each(function (i) {
                            $($("#particulars-body > tr")[i]).addClass('invalid-row');
                        });
                        for (var i in msg.rows) {
                            self.particulars.rows()[i].id = msg.rows[i];
                            $($("#particulars-body > tr")[i]).removeClass('invalid-row');
                        }
                    }
                }
            });
        }
        else
            return true;
    }


    self.sub_total = function () {
        var sum = 0;
        self.particulars.rows().forEach(function (i) {
            sum += i.amount();
        });
        return round2(sum);
    }

    self.tax_amount = function () {
        var sum = 0;
        if (self.tax() == 'inclusive') {
            self.particulars.rows().forEach(function (i) {
                if (typeof i.tax_scheme() != 'undefined') {
                    var tax_percent = self.tax_scheme_by_id(i.tax_scheme()).percent;
                    var tax_amount = i.amount() * (tax_percent / (100 + tax_percent));
                    sum += tax_amount;
                }
            });
        } else if (self.tax() == 'exclusive') {
            self.particulars.rows().forEach(function (i) {
                var tax_percent = self.tax_scheme_by_id(i.tax_scheme()).percent;
                var tax_amount = i.amount() * (tax_percent / 100);
                sum += tax_amount;
            });
        }
        return round2(sum);
    }

    self.total_amount = 0;

    self.grand_total = function () {
        if (self.tax() == 'exclusive') {
            self.total_amount = self.sub_total() + self.tax_amount();
        }
        self.total_amount = round2(self.sub_total());
        return self.total_amount;
    }

    self.total_amount = 0;

    self.itemChanged = function (row) {
        var selected_item = $.grep(self.items, function (i) {
            return i.id == row.item_id();
        })[0];
        if (!selected_item) return;
        if (!row.description())
            row.description(selected_item.description);
//        if (!row.unit_price())
//            row.unit_price(selected_item.sales_price);
        if (!row.tax_scheme())
            row.tax_scheme(selected_item.tax_scheme);
    }

    self.customer_changed = function (vm) {
        var selected_obj = $.grep(self.customers, function (i) {
            return i.id == vm.party;
        })[0];
        self.party_address(selected_obj.address);
//        if (!selected_item) return;
//        if (!row.description())
//            row.description(selected_item.description);
//        if (!row.unit_price())
//            row.unit_price(selected_item.sales_price);
//        if (!row.tax_scheme())
//            row.tax_scheme(selected_item.tax_scheme);
    }

}

function ParticularViewModel(particular) {

    var self = this;
    //default values
    self.item_id = ko.observable();
    self.description = ko.observable();
    self.unit_price = ko.observable(0);
    self.quantity = ko.observable(1);
    self.discount = ko.observable(0).extend({ numeric: 2 });
    self.tax_scheme = ko.observable();

    for (var k in particular)
        self[k] = ko.observable(particular[k]);

    if (self.discount() == null)
        self.discount(0);

    self.amount = ko.computed(function () {
        var wo_discount = self.quantity() * self.unit_price();
        var amt = wo_discount - ((self.discount() * wo_discount) / 100);

        return amt;
    });

}

