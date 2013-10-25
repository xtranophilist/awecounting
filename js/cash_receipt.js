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

    self.party = ko.observable();
    self.receipt_on = ko.observable();
    self.party_address = ko.observable();
    self.reference = ko.observable();
    self.current_balance = ko.observable();
    self.amount = ko.observable();
    self.table_vm = ko.observable({'rows': function(){}, 'get_total': function(){}});

    self.party_changed = function (vm) {
        var selected_obj = $.grep(self.parties, function (i) {
            return i.id == vm.party();
        })[0];
        self.party_address(selected_obj.address);
        self.current_balance(selected_obj.customer_balance);
    }


    self.load_related_invoices = function () {
        if (self.party()) {
            $.ajax({
                url: '/voucher/invoice/party/' + self.party() + '.json',
                dataType: 'json',
                async: false,
                success: function (data) {
                    self.invoices = data;
                    var options = {
                        rows: self.invoices
                    };
                    self.table_vm(new TableViewModel(options, CashReceiptRowVM));
                }
            });
        }

    }


//    var validate = function(msg, rows, tr_wrapper_id){
//        var selection = $("#" + tr_wrapper_id + " > tr");
//        selection.each(function (index) {
//            $(selection[index]).addClass('invalid-row');
//        });
//        for (var i in msg['saved']){
//            rows[i].id = msg['saved'][''+i+''];
//            $(selection[i]).removeClass('invalid-row');
//        }
//        var model = self[tr_wrapper_id.toUnderscore()];
//        var saved_size = Object.size(msg['saved']) ;
//        if(saved_size==rows.length)
//            model.message('Saved!');
//        else if(saved_size==0){
//            model.message('No rows saved!');
//            model.status('error');
//        }
//        else if(saved_size<rows.length){
//            var message = saved_size.toString() +' row' + ((saved_size==1)?'':'s') + ' saved! ';
//            message += (rows.length-saved_size).toString() +' row' + ((rows.length-saved_size==1)?' is':'s are') + ' incomplete!';
//            model.message(message);
//            model.status('error');
//        }
//    }
//
//    var key_to_options = function(key){
//        return {
//            rows: data['rows'],
//            save_to_url : '/payroll/save/',
//            properties : {id : self.id},
//            onSaveSuccess : function(msg, rows){
//                self.payroll_entry.id = msg.id;
//                validate(msg, rows, key.toDash());
//            }
//        };
//    }
//

}


function CashReceiptRowVM(row) {
    var self = this;

    self.payment = ko.observable(0);
    self.discount = ko.observable(0);

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
