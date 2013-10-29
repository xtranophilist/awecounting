$(document).ready(function () {
    $(document).ready(function () {
        $('.date-picker').datepicker();
    });
    vm = new AttendanceVoucherVM(ko_data);
    ko.applyBindings(vm);
});


function AttendanceVoucherVM(data) {
    var self = this;

    $.ajax({
        url: '/payroll/employees.json',
        dataType: 'json',
        async: false,
        success: function (data) {
            self.employees = data;
        }
    });

    self.id = ko.observable();
    self.message = ko.observable();
    self.state = ko.observable('standby');
    self.voucher_no = ko.observable();
    self.date = ko.observable();
    self.employee = ko.observable();
    self.from_date = ko.observable();
    self.to_date = ko.observable();
    self.total_working_days = ko.observable();
    self.full_present_day = ko.observable();
    self.half_present_day = ko.observable(0);
    self.early_late_attendance_day = ko.observable(0);
    self.total_present_day = ko.observable();
    self.total_absent_day = ko.observable();
    self.total_ot_hours = ko.observable();

    for (var k in data) {
        if (data[k])
            self[k] = ko.observable(data[k]);
    }

    self.validate = function () {
        self.message('');
        if (!self.employee()) {
            self.message('Employee field is required!')
            self.state('error');
            return false;
        }
        return true;
    }

    self.total_present_day = function () {
        return round2(parseFloat(self.full_present_day()) + (parseFloat(self.half_present_day()) * parseFloat(self.half_multiplier())) +
            (parseFloat(self.early_late_attendance_day()) * parseFloat(self.early_late_multiplier())));
    }

    self.total_absent_day = function () {
        return round2(self.total_working_days() - self.total_present_day());
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