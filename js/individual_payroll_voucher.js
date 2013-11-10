$(document).ready(function () {
    $(document).ready(function () {
        $('.date-picker').datepicker();
    });
    vm = new IndividualPayrollVoucherVM(ko_data);
    ko.applyBindings(vm);
    $('.change-on-ready').trigger('change');
});


function IndividualPayrollVoucherVM(data) {
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
    self.employee = ko.observable();

    self.days_worked = ko.observable();
    self.hours_worked = ko.observable();
    self.ot_hours_worked = ko.observable();

    self.day_rate = ko.observable();
    self.hour_rate = ko.observable();
    self.ot_hour_rate = ko.observable();

    self.employee_changed = function (data) {
        var selected_item = $.grep(self.employees, function (i) {
            return i.id == data.employee();
        })[0];
        if (!selected_item) return;
        self.days_worked(selected_item.unpaid_days);
        self.hours_worked(selected_item.unpaid_hours);
        self.ot_hours_worked(selected_item.unpaid_ot_hours);
    }

    self.day_amount = function () {
        return round2(self.days_worked() * self.day_rate());
    }

    self.hour_amount = function () {
        return round2(self.hours_worked() * self.hour_rate());
    }

    self.ot_hour_amount = function () {
        return round2(self.ot_hours_worked() * self.ot_hour_rate());
    }

    self.total = function () {
        return self.day_amount() + self.hour_amount() + self.ot_hour_amount();
    }


    for (var k in data) {
        if (data[k])
            self[k] = ko.observable(data[k]);
    }

    self.inclusions = new TableViewModel({rows: data.inclusions}, IndividualPayrollVoucherRowVM);

    self.deductions = new TableViewModel({rows: data.deductions}, IndividualPayrollVoucherRowVM);

    self.validate = function () {
        self.message('');
        if (!self.employee()) {
            self.message('"Employee" is required!')
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
                url: '/payroll/individual-voucher/save/',
                data: data,
                success: function (msg) {
                    if (typeof (msg.error_message) != 'undefined') {
                        self.message(msg.error_message);
                        self.state('error');
                    }
                    else {
                        self.message('Saved!');
                        self.state('success');
                        if (msg.id) {
                            self.id(msg.id);
                            self.status('Unapproved');
                        }
                        if (msg.redirect_to) {
                            window.location = msg.redirect_to;
                        }
                        $("#table-body-inclusions > tr").each(function (i) {
                            $($("#table-body-inclusions > tr")[i]).addClass('invalid-row');
                        });
                        $("#table-body-deductions > tr").each(function (i) {
                            $($("#table-body-deductions > tr")[i]).addClass('invalid-row');
                        });
                        for (var i in msg.rows1) {
                            self.inclusions.rows()[i].id = msg.rows1[i];
                            $($("#table-body-inclusions > tr")[i]).removeClass('invalid-row');
                        }
                        for (var i in msg.rows2) {
                            self.deductions.rows()[i].id = msg.rows2[i];
                            $($("#table-body-deductions > tr")[i]).removeClass('invalid-row');
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

    self.approve = function (item, event) {
            $.ajax({
                type: "POST",
                url: '/payroll/individual-voucher/approve/',
                data: ko.toJSON(self),
                success: function (msg) {
                    if (typeof (msg.error_message) != 'undefined') {
                        self.message(msg.error_message);
                        self.state('error');
                    }
                    else {
                        self.message('Approved!');
                        self.state('success');
                        self.status('Approved');
                        if (msg.id)
                            self.id(msg.id);
                    }
                }
            });
    }

}

function IndividualPayrollVoucherRowVM(data) {

    var self = this;

    self.account = ko.observable();
    self.amount = ko.observable();

    for (var k in data)
        if (data[k])
            self[k] = ko.observable(data[k]);

}