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


    self.date_changed = function () {
        if (!self.from_date() || !self.to_date())
            return;
        var the_date = new Date(self.from_date());
        while (the_date <= new Date(self.to_date())) {
            var new_date = new DateM(the_date);
            var match = $.grep(self.days(), function (i) {
                return i.yyyy_mm_dd() == new_date.yyyy_mm_dd();
            })[0];
            if (!match) {
                self.days.push(new_date);
                for (var i = 0; i < self.rows().length; i++) {
                    var row = self.rows()[i];
                    row.work_days.push(new WorkDayVM({}, new_date))
                }
            }
            the_date.setDate(the_date.getDate() + 1);
        }
        for (var i = 0; i < self.days().length; i++) {
            var day = self.days()[i];
            var date1 = new Date(day.yyyy_mm_dd());
            if (date1 < new Date(self.from_date()) || date1 > new Date(self.to_date())) {
                self.days.remove(day);
                for (var j = 0; j < self.rows().length; j++) {
                    var row = self.rows()[j];
                    for (var k = 0; k < row.work_days().length; k++) {
                        var work_day = row.work_days()[k];
                        var work_date = new Date(work_day.day.date_string);
                        if (date1.getTime() == work_date.getTime()) {
                            row.work_days.remove(work_day);
                        }
                    }
                }

            }
        }

    }

    self.date_changed();

    self.rows = ko.observableArray(ko.utils.arrayMap(self.rows(), function (item) {
        return new WorkTimeVoucherRowVM(item, self.days());
    }));

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
                        $("#work-time-table > tr").each(function (i) {
                            $($("#work-time-table > tr")[i]).addClass('invalid-row');
                        });
                        for (var i in msg.rows) {
                            self.rows()[i].id = msg.rows[i]['id'];
                            $($("#work-time-table > tr")[i]).removeClass('invalid-row');
                            for (var j in msg.rows[i]['days']) {
                                self.rows()[i].work_days()[j].id = msg.rows[i]['days'][j];
                            }
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
    self.work_days = ko.observableArray();
    self.employee = ko.observable();

    if (data.employee)
        self.employee = ko.observable(data.employee);

    if (data.id)
        self.id = ko.observable(data.id);

    for (var k in days) {
        var day = days[k];
        if (data.work_days) {
            var selected_item = $.grep(data.work_days, function (i) {
                return i.day == day.yyyy_mm_dd();
            })[0];
            if (selected_item)
                self.work_days().push(new WorkDayVM(selected_item, day))
        }
        else
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
    }, this);


    self.day = day;
}

function DateM(date) {
    var self = this;

    self.date = date;
    self.weekday = get_weekday(date);
    self.date_string = date.toUTCString();
    self.day = date.getDate();
    self.month = date.getMonth() + 1; //Months are zero based
    self.year = date.getFullYear();

    self.yyyy_mm_dd = ko.computed(function () {
        var month = self.month;
        var day = self.day;
        if (month < 10)
            month = '0' + month;
        if (day < 10)
            day = '0' + day;
        return self.year + '-' + month + '-' + day;
    }, this);
}