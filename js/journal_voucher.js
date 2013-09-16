$(document).ready(function () {
    $('.date-picker').datepicker().data('datepicker');
});


function JournalVoucher(data){
    var self = this;

    self.date = '';

    for (var k in data)
        self[k]=data[k];

    $.ajax({
        url: '/ledger/accounts/json',
        dataType: 'json',
        async: false,
        success: function(data) {
            self.accounts = data;
        }
    });

    var validate = function(msg, rows, tr_wrapper_id){
        var selection = $("#" + tr_wrapper_id + " > tr");
        selection.each(function (index) {
            $(selection[index]).addClass('invalid-row');
        });
        for (var i in msg['saved']){
            rows[i].id = msg['saved'][''+i+''];
            $(selection[i]).removeClass('invalid-row');
        }
        var model = self[tr_wrapper_id.toUnderscore()];
        var saved_size = Object.size(msg['saved']) ;
        if(saved_size==rows.length)
            model.message('Saved!');
        else if(saved_size==0){
            model.message('No rows saved!');
            model.status('error');
        }
        else if(saved_size<rows.length){
            var message = saved_size.toString() +' row' + ((saved_size==1)?'':'s') + ' saved! ';
            message += (rows.length-saved_size).toString() +' row' + ((rows.length-saved_size==1)?' is':'s are') + ' incomplete!';
            model.message(message);
            model.status('error');
        }
    }

    var key_to_options = function(key){
        return {
            rows: data['rows'],
            save_to_url : '/voucher/journal/save/',
            properties : {id : self.id},
            onSaveSuccess : function(msg, rows){
                validate(msg, rows, key.toDash());
            }
        };
    }

    self.journal_voucher = new TableViewModel(key_to_options('journal_voucher'), JournalVoucherRow);

    self.journal_voucher.cr_total = function(){
        var total = 0;
        $.each(self.journal_voucher.rows(), function(){
            if (isAN(this.cr_amount())){
                total += this.cr_amount();
            }
        });
        return total;
    }

    self.journal_voucher.dr_total = function(){
        var total = 0;
        $.each(self.journal_voucher.rows(), function(){
            if (isAN(this.dr_amount()))
                total += this.dr_amount();
        });
        return total;
    }

    self.journal_voucher.cr_equals_dr = function(){
        return self.journal_voucher.dr_total() === self.journal_voucher.cr_total();
    }

    self.journal_voucher.total_row_class = function(){
        if (self.journal_voucher.dr_total() === self.journal_voucher.cr_total())
            return 'valid-row';
        return 'invalid-row';
    }

    self.journal_voucher.save = function(){

        self.journal_voucher.status('waiting');

        var valid = true;
        var message = '';
        var rows = self.journal_voucher.rows();
        var selection = $("#journal-voucher > tr");

        var error_messages = {
            1 : 'You can\'t enter both Dr and Cr Accounts in same row!',
            2 : 'You can\'t enter Cr amount while selecting Dr account!',
            3 : 'You can\'t enter Dr amount while selecting Cr account!',
            4 : 'Either Dr or Cr account is required in a row!',
            5 : 'You can\'t enter both Dr and Cr amounts in same row!',
            6 : 'Either Dr or Cr amount is required in a row!'
        };

        var errors = {}; //row: [errors]

        for (var i=0; i<rows.length; i++){



            var row_valid = true;
            $(selection[i]).removeClass('invalid-row');
            var row = rows[i];
            errors[i] = [];
            if (row.dr_account_id() && row.cr_account_id()){
//                message += 'Row ' + (i+1) + ':  ';
                errors[i].push(1);
                row_valid = false;
            }
            if (row.dr_account_id() && row.cr_amount()){
//                message += 'Row ' + (i+1) + ':  ';
                errors[i].push(2);
                row_valid = false;
            }
            if (row.cr_account_id() && row.dr_amount()){
//                message += 'Row ' + (i+1) + ':  ';
                errors[i].push(3);
                row_valid = false;
            }
            if (!row.dr_account_id() && !row.cr_account_id()){
//                message += 'Row ' + (i+1) + ':  ';
                errors[i].push(4);
                row_valid = false;
            }
            if (row.dr_amount() && row.cr_amount()){
//                message += 'Row ' + (i+1) + ':  ';
                errors[i].push(5);
                row_valid = false;
            }
            if (empty_or_undefined(row.dr_amount()) && empty_or_undefined(row.cr_amount())){
//                message += 'Row ' + (i+1) + ':  ';
                errors[i].push(6);
                row_valid = false;
            }
            if (!row_valid){
                valid = false;
                $(selection[i]).addClass('invalid-row');
            }
        }

        for ( var r in errors){
            var row_errors = errors[r];
            message += 'Row ' + (parseInt(r)+1) + ': ';
            for (var i in row_errors){
                message += error_messages[row_errors[i]] + ' ';
            }
            // TODO
//            message += '<br>';
        }

        if (!self.journal_voucher.cr_equals_dr()){
            message += 'Total Dr and Cr amounts don\'t tally!';
            valid = false;
        }

        if (!self.date){
            message += 'Date field is required!';
            valid = false;
        }

        self.journal_voucher.message(message);
        if (!valid){
            self.journal_voucher.status('error');
            return false;
        }
        $.ajax({
            type: "POST",
            url: '/voucher/journal/save/',
            data: ko.toJSON(self),
            success: function(msg){
                self.journal_voucher.message('Saved!');
                self.deleted_rows  = [];
                self.journal_voucher.status('success');

            },
            error: function(XMLHttpRequest, textStatus, errorThrown) {
                self.journal_voucher.message('Saving Failed!');
                self.journal_voucher.status('error');
            }
        });


    }
}

function JournalVoucherRow(row){
    var self = this;

    self.dr_account_id = ko.observable();
    self.cr_account_id = ko.observable();
    self.dr_amount = ko.observable();
    self.cr_amount = ko.observable();

    for (var k in row){
        if (row[k] != null)
            self[k] = ko.observable(row[k]);
    }

}