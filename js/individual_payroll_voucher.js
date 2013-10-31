$(document).ready(function () {
    $(document).ready(function () {
        $('.date-picker').datepicker();
    });
    vm = new GroupPayrollVoucherVM(ko_data);
    ko.applyBindings(vm);
    $('.change-on-ready').trigger('change');
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
        if (!selected_item) return;

        row.present_days(selected_item.unpaid_days);
        row.present_hours(selected_item.unpaid_hours);
        row.present_ot_hours(selected_item.unpaid_ot_hours);
    }


    for (var k in data) {
        if (data[k])
            self[k] = ko.observable(data[k]);
    }

    var options = {rows: data.rows}

    self.table_vm = new TableViewModel(options, GroupPayrollVoucherRowVM);

    self.save = function (item, event) {
        if (get_form(event).checkValidity()) {
            if ($(get_target(event)).data('continue')) {
                self.continue = true;
            }
            var data = ko.toJSON(self);
            $.ajax({
                type: "POST",
                url: '/payroll/group-voucher/save/',
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
                        $("#table-body > tr").each(function (i) {
                            $($("#table-body > tr")[i]).addClass('invalid-row');
                        });
                        for (var i in msg.rows) {
                            self.table_vm.rows()[i].id = msg.rows[i];
                            $($("#table-body > tr")[i]).removeClass('invalid-row');
                        }
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

    for (var k in data)
        if (data[k])
            self[k] = ko.observable(data[k]);

    self.amount = function () {
        return round2z(self.present_days()) * round2z(self.rate_day()) + round2z(self.present_hours()) * round2z(self.rate_hour()) + round2z(self.present_ot_hours()) * round2z(self.rate_ot_hour());
    }

    self.net = function () {
        return self.amount() - round2z(self.payroll_tax());
    }

}