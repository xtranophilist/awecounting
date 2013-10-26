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

    $.ajax({
        url: '/ledger/fixed-assets.json',
        dataType: 'json',
        async: false,
        success: function (data) {
            self.fixed_assets = data;
        }
    });

    self.id = ko.observable('hey');
    self.message = ko.observable();
    self.status = ko.observable('standby');
    self.from_account = ko.observable();
    self.voucher_no = ko.observable();
    self.party_address = ko.observable();
    self.date = ko.observable();
    self.reference = ko.observable();

    for (var k in data) {
        self[k] = ko.observable(data[k]);
    }

    var options = {
        rows: data.rows
    };

    self.table_vm = new TableViewModel(options, FixedAssetRowVM);

    var options2 = {
        rows: data.additional_details
    }

    self.additional_details = new TableViewModel(options2, AdditionalDetailVM);

    self.account_changed = function (vm) {
        var selected_obj = $.grep(self.from_accounts, function (i) {
            return i.id == vm.from_account();
        })[0];
        self.party_address(selected_obj.address);
    }

    self.validate = function () {
        if (!self.from_account()) {
            self.message('"From" field is required!')
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
                url: '/voucher/fixed-asset/save/',
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
                url: '/voucher/fixed-asset/approve/',
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

    self.asset_ledger = ko.observable();
    self.description = ko.observable();
    self.amount = ko.observable();

    for (var k in row) {
        self[k] = ko.observable(row[k]);
    }

}

function AdditionalDetailVM(row) {
    var self = this;

    self.assets_code = ko.observable();
    self.assets_type = ko.observable();
    self.vendor_name = ko.observable();
    self.vendor_address = ko.observable();
    self.amount = ko.observable();
    self.useful_life = ko.observable();
    self.description = ko.observable();
    self.warranty_period = ko.observable();
    self.maintenance = ko.observable();

    for (var k in row) {
        self[k] = ko.observable(row[k]);
    }

}