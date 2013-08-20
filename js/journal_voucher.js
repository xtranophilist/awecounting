function JournalVoucher(data){
    var self = this;

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
            save_to_url : '/voucher/journal/save',
            properties : {id : self.id},
            onSaveSuccess : function(msg, rows){
                validate(msg, rows, key.toDash());
            }
        };
    }

    self.journal_voucher = new TableViewModel(key_to_options('journal_voucher'), JournalVoucherRow);
}

function JournalVoucherRow(row){
    var self = this;

    self.dr_account_id = ko.observable();
    self.cr_account_id = ko.observable();
    self.dr_amount = ko.observable();
    self.cr_amount = ko.observable();

    for (var k in row){
        self[k] = ko.observable(row[k]);
    }

}