$(document).ready(function () {
    $(document).ready(function () {
        $('.date-picker').datepicker();
    });
    vm = new WorkTimeVoucherVM(ko_data);
    ko.applyBindings(vm);
});


function WorkTimeVoucherVM(data) {
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
    self.from_date = ko.observable();
    self.to_date = ko.observable();
    self.days = ko.observableArray();
    self.rows = ko.observableArray();

    for (var k in data) {
        if (data[k])
            self[k] = ko.observable(data[k]);
    }

    self.rows = ko.observableArray(ko.utils.arrayMap(self.rows, function (item) {
        return new WorkTimeVoucherRowVM(item, self.days());
    }));

    self.date_changed = function () {
        if (!self.from_date() || !self.to_date())
            return;
        var date = new Date(self.from_date());
        while (date <= new Date(self.to_date())) {
            self.days.push(new DateM(date));
            date.setDate(date.getDate() + 1);
        }
//        self.rows = ko.observableArray(ko.utils.arrayMap(self.rows(), function (item) {
//            return new WorkTimeVoucherRowVM({}, self.days());
//        }));
    }

    self.date_changed();

    self.add_row = function () {
        self.rows.push(new WorkTimeVoucherRowVM({}, self.days()));
    };

    self.save = function (item, event) {
        if (get_form(event).checkValidity()) {
            $.ajax({
                type: "POST",
                url: '/payroll/attendance-voucher/save/',
                data: ko.toJSON(self),
                success: function (msg) {
                    if (typeof (msg.error_message) != 'undefined') {
                        $('#message').html(msg.error_message);
                    }
                    else {
                        $('#message').html('Saved!');
                        if (msg.id)
                            self.id = msg.id;
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


}

function WorkTimeVoucherRowVM(data, days) {
    var self = this;

    self.employee = ko.observable();
    self.work_days = ko.observableArray();

    for (var k in data) {
        if (data[k])
            self[k] = ko.observable(data[k]);
    }

    for (var k in days) {
        var day = days[k];
        self.work_days().push(new WorkDayVM({}, day))
    }
}

function WorkDayVM(data, day) {
    var self = this;

    self.in_time = ko.observable();
    self.out_time = ko.observable();

    for (var k in data) {
        if (data[k])
            self[k] = ko.observable(data[k]);
    }

    self.work_time = ko.computed(function () {
        var in_time = self.in_time();
        var out_time = self.out_time();
        if (!in_time || !out_time)
            return;
        var in_hour = parseInt(in_time.split(':')[0]);
        var in_minute = parseInt(in_time.split(':')[1]);
        var out_hour = parseInt(out_time.split(':')[0]);
        var out_minute = parseInt(out_time.split(':')[1]);
        if (out_minute < in_minute) {
            out_minute += 60;
            out_hour -= 1;
        }
        var diff_hour = out_hour - in_hour;
        if (diff_hour < 0)
            diff_hour += 24;
        return diff_hour + ':' + (out_minute - in_minute);
//        return '12:10';
    }, this);


    self.day = day;
}

function DateM(date) {
    var self = this;

    self.weekday = get_weekday(date);
    self.date = date.toUTCString();

}
