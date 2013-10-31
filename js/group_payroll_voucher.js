$(document).ready(function () {
    $(document).ready(function () {
        $('.date-picker').datepicker();
    });
    vm = new GroupPayrollVoucherVM(ko_data);
    ko.applyBindings(vm);
});


function GroupPayrollVoucherVM(data) {
    var self = this;

    $.ajax({
        url: '/payroll/employees.json',
        dataType: 'json',
        async: false,
        success: function (data) {
            self.employees = data;
        }
    });

    $.ajax({
        url: '/ledger/payheads.json',
        dataType: 'json',
        async: false,
        success: function (data) {
            self.accounts = data;
        }
    });

    self.id = ko.observable();
    self.message = ko.observable();
    self.state = ko.observable('standby');
    self.voucher_no = ko.observable();
    self.date = ko.observable();

    self.employee_changed = function (row) {
        var selected_item = $.grep(self.employees, function (i) {
            return i.id == row.employee();
        })[0];
        console.log(selected_item);
//        if (!selected_item) return;
//        if (!row.description())
//            row.description(selected_item.description);
//        if (!row.unit_price())
//            row.unit_price(selected_item.sales_price);
//        if (!row.tax_scheme())
//            row.tax_scheme(selected_item.tax_scheme);
    }


    for (var k in data) {
        if (data[k])
            self[k] = ko.observable(data[k]);
    }

    var options = {rows: data.rows}

    self.table_vm = new TableViewModel(options, GroupPayrollVoucherRowVM);

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
                url: '/payroll/attendance-voucher/save/',
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

}

function GroupPayrollVoucherRowVM(data) {

    var self = this;

    self.employee = ko.observable();
    self.present_days = ko.observable();
    self.present_hours = ko.observable();
    self.present_ot_hours = ko.observable();
    self.rate_day = ko.observable();
    self.rate_hour = ko.observable();
    self.rate_ot_hour = ko.observable();
    self.payroll_tax = ko.observable();
    self.pay_head = ko.observable();

    self.amount = function () {
        return;
    }

    self.net = function () {
        return;
    }

}